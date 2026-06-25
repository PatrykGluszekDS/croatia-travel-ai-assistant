import json

from database import get_packages_by_destination


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

    return f"Unknown tool: {name}"