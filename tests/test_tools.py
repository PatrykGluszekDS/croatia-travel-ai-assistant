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


def test_call_tool_get_destination_overview():
    initialize_database()

    arguments = json.dumps({"destination": "Krk"})

    result = call_tool("get_destination_overview", arguments)

    assert "Krk" in result
    assert "Best season" in result


def test_call_tool_get_activities_for_destination():
    initialize_database()

    arguments = json.dumps({"destination": "Istria"})

    result = call_tool("get_activities_for_destination", arguments)

    assert "Istria" in result
    assert "Activity" in result


def test_call_tool_get_transport_options():
    initialize_database()

    arguments = json.dumps({"destination": "Split"})

    result = call_tool("get_transport_options", arguments)

    assert "Split" in result
    assert "Transport type" in result