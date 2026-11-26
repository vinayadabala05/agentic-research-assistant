"""Offline tests for tools (no API key required)."""

from agent.tools import calculator, get_current_time, search_notes


def test_calculator_multiply():
    assert calculator.invoke({"expression": "12 * 8"}) == "96"


def test_calculator_divide():
    assert calculator.invoke({"expression": "100 / 4"}) == "25"


def test_get_current_time_has_utc():
    result = get_current_time.invoke({})
    assert "UTC" in result


def test_search_notes_refund():
    result = search_notes.invoke({"query": "refund policy days"})
    assert "14" in result
