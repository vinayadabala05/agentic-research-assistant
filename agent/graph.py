"""LangGraph agent with tool calling."""

from __future__ import annotations

import os
from typing import Annotated, Literal, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from agent.prompts import SYSTEM_PROMPT
from agent.tools import get_all_tools

load_dotenv()


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def _build_llm():
    provider = os.getenv("LLM_PROVIDER", "groq").lower().strip()

    if provider == "openai":
        from langchain_openai import ChatOpenAI

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not set. Copy .env.example to .env and add your key.")
        return ChatOpenAI(model="gpt-4o-mini", temperature=0)

    from langchain_groq import ChatGroq

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Get a free key at https://console.groq.com and put it in .env"
        )
    return ChatGroq(model="llama-3.3-70b-versatile", temperature=0)


def build_agent():
    tools = get_all_tools()
    llm = _build_llm().bind_tools(tools)
    tool_node = ToolNode(tools)

    def chatbot(state: AgentState):
        msgs = state["messages"]
        if not msgs or not isinstance(msgs[0], SystemMessage):
            msgs = [SystemMessage(content=SYSTEM_PROMPT)] + list(msgs)
        response = llm.invoke(msgs)
        return {"messages": [response]}

    def route(state: AgentState) -> Literal["tools", "end"]:
        last = state["messages"][-1]
        if isinstance(last, AIMessage) and last.tool_calls:
            return "tools"
        return "end"

    graph = StateGraph(AgentState)
    graph.add_node("chatbot", chatbot)
    graph.add_node("tools", tool_node)
    graph.set_entry_point("chatbot")
    graph.add_conditional_edges("chatbot", route, {"tools": "tools", "end": END})
    graph.add_edge("tools", "chatbot")

    return graph.compile()


def run_query(question: str) -> dict:
    """Run one question and return answer + tool names used."""
    agent = build_agent()
    result = agent.invoke({"messages": [HumanMessage(content=question)]})
    messages = result["messages"]

    tools_used: list[str] = []
    final_text = ""
    for m in messages:
        if isinstance(m, AIMessage):
            if m.tool_calls:
                for tc in m.tool_calls:
                    name = tc.get("name") if isinstance(tc, dict) else getattr(tc, "name", None)
                    if name:
                        tools_used.append(name)
            if m.content:
                final_text = m.content if isinstance(m.content, str) else str(m.content)

    return {
        "question": question,
        "answer": final_text.strip(),
        "tools_used": tools_used,
    }
