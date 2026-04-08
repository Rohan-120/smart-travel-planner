"""
External Travel Tool
Fetches real-time travel data such as flight prices, hotel availability, and weather.
"""
from langchain.tools import tool


@tool
def external_travel_tool(query: str) -> str:
    """
    Fetch real-time travel data including flight prices, hotel rates, and weather.
    Use this when the user needs live pricing or availability information.
    """
    # TODO: integrate with external travel APIs (e.g., Amadeus, OpenWeather)
    raise NotImplementedError("external_travel_tool is not yet implemented")
