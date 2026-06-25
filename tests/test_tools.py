import json

from database import initialize_database
from tools import call_tool


def test_call_tool_get_travel_packages_by_destination():
    initialize_database()

    arguments = json.dumps({"destination": "Split"})

    result = call_tool("get_travel_packages_by_destination", arguments)

    assert "Split" in result
    assert "Estimated price" in result


def test_call_tool_search_travel_packages():
    initialize_database()

    arguments = json.dumps({"travel_style": "romantic"})

    result = call_tool("search_travel_packages", arguments)

    assert "Dubrovnik" in result


def test_call_tool_unknown_tool():
    result = call_tool("unknown_tool", "{}")

    assert "Unknown tool" in result