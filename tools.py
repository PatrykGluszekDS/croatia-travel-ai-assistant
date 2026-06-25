import json

from database import get_packages_by_destination, search_travel_packages


TOOLS = [
    {
        "type": "function",
        "name": "get_travel_packages_by_destination",
        "description": (
            "Get travel package information for a specific Croatian destination "
            "from the local SQLite database. Use this when the user asks about "
            "available packages, prices, duration, travel style, or details for a destination."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "destination": {
                    "type": "string",
                    "description": "The Croatian destination, for example Split, Dubrovnik, Krk, Zadar, or Istria.",
                }
            },
            "required": ["destination"],
            "additionalProperties": False,
        },
    },
    {
    "type": "function",
    "name": "search_travel_packages",
    "description": (
        "Search the local SQLite database for Croatian travel packages using optional filters. "
        "Use this when the user asks for packages by travel style, budget, duration, region, "
        "or when they ask to see available packages without naming one exact destination."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "destination": {
                "type": "string",
                "description": "Destination name, for example Split, Dubrovnik, Krk, Zadar, or Istria.",
            },
            "region": {
                "type": "string",
                "description": "Croatian region, for example Dalmatia, Kvarner, or Istria.",
            },
            "travel_style": {
                "type": "string",
                "description": "Travel style, for example romantic, food and wine, hidden gems, relaxed island, culture and beaches.",
            },
            "max_price_eur": {
                "type": "integer",
                "description": "Maximum estimated package price in EUR.",
            },
            "duration_days": {
                "type": "integer",
                "description": "Exact package duration in days.",
            },
        },
        "additionalProperties": False,
    },
}
]


def call_tool(name, arguments):
    """
    Execute a tool requested by the model.

    Parameters:
    - name: tool/function name chosen by the model
    - arguments: JSON string with function arguments

    Returns:
    - string result that will be sent back to the model
    """

    args = json.loads(arguments)

    if name == "get_travel_packages_by_destination":
        destination = args["destination"]
        return get_packages_by_destination(destination)

    if name == "search_travel_packages":
        return search_travel_packages(
            destination=args.get("destination"),
            region=args.get("region"),
            travel_style=args.get("travel_style"),
            max_price_eur=args.get("max_price_eur"),
            duration_days=args.get("duration_days"),
        )

    return f"Unknown tool: {name}"