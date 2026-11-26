#!/usr/bin/env python3
"""CLI entrypoint for the tool-using research agent."""

from __future__ import annotations

import sys

from agent.graph import run_query


def main() -> None:
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
    else:
        question = input("Ask a question: ").strip()

    if not question:
        print("No question provided.")
        sys.exit(1)

    print(f"\nQuestion: {question}\n")
    try:
        result = run_query(question)
    except Exception as exc:
        print(f"Error: {exc}")
        sys.exit(1)

    tools = ", ".join(result["tools_used"]) if result["tools_used"] else "(none)"
    print(f"Tools used: {tools}")
    print(f"Answer: {result['answer']}\n")


if __name__ == "__main__":
    main()
