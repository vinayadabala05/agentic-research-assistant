#!/usr/bin/env python3
"""Run a small evaluation set against the agent."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from agent.graph import run_query

CASES_PATH = Path(__file__).resolve().parent / "cases.json"


def main() -> None:
    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    passed = 0
    failed = 0

    print(f"Running {len(cases)} eval cases...\n")

    for case in cases:
        case_id = case["id"]
        question = case["question"]
        expected_tool = case.get("expected_tool")
        expected_contains = case.get("expected_contains", "").lower()

        try:
            result = run_query(question)
        except Exception as exc:
            failed += 1
            print(f"[FAIL] {case_id}: agent error -> {exc}")
            continue

        tools = result["tools_used"]
        answer = (result["answer"] or "").lower()

        tool_ok = True
        if expected_tool:
            tool_ok = expected_tool in tools

        text_ok = expected_contains in answer if expected_contains else True

        if tool_ok and text_ok:
            passed += 1
            print(f"[PASS] {case_id}")
        else:
            failed += 1
            reasons = []
            if not tool_ok:
                reasons.append(f"expected tool '{expected_tool}', got {tools}")
            if not text_ok:
                reasons.append(f"answer missing '{case.get('expected_contains')}'")
            print(f"[FAIL] {case_id}: {'; '.join(reasons)}")
            print(f"       answer: {result['answer'][:200]}")

    total = passed + failed
    print(f"\nResult: {passed}/{total} passed, {failed} failed")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
