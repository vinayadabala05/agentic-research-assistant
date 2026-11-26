"""Reusable tools the agent can call."""

from __future__ import annotations

import ast
import operator
from datetime import datetime, timezone
from pathlib import Path

from langchain_core.tools import tool

NOTES_PATH = Path(__file__).resolve().parent.parent / "data" / "notes.txt"

_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
}


def _eval_node(node: ast.AST) -> float:
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval_node(node.operand))
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval_node(node.left), _eval_node(node.right))
    raise ValueError("Only simple arithmetic expressions are allowed")


@tool
def calculator(expression: str) -> str:
    """Evaluate a simple math expression. Supports +, -, *, /. Example: 12 * 8"""
    try:
        tree = ast.parse(expression.strip(), mode="eval")
        result = _eval_node(tree)
        if result == int(result):
            return str(int(result))
        return str(round(result, 6))
    except Exception as exc:
        return f"Calculator error: {exc}"


@tool
def get_current_time() -> str:
    """Return the current UTC date and time."""
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%d %H:%M:%S UTC")


@tool
def search_notes(query: str) -> str:
    """Search the local company notes for relevant information about policies, support, products, or APIs."""
    if not NOTES_PATH.exists():
        return "Notes file not found."

    text = NOTES_PATH.read_text(encoding="utf-8")
    query_l = query.lower().strip()
    keywords = [k for k in query_l.replace("?", "").split() if len(k) > 2]

    chunks = [c.strip() for c in text.split("\n\n") if c.strip()]
    scored = []
    for chunk in chunks:
        lower = chunk.lower()
        score = sum(1 for k in keywords if k in lower)
        if score:
            scored.append((score, chunk))

    if not scored:
        return "No strong match. Full notes:\n" + text[:800]

    scored.sort(key=lambda x: x[0], reverse=True)
    top = [c for _, c in scored[:3]]
    return "\n\n".join(top)


def get_all_tools():
    return [calculator, get_current_time, search_notes]
