"""
Itinerary Generator Tool
Generates day-by-day travel plans based on destination, dates, and user preferences.
"""
from langchain.tools import tool


@tool
def itinerary_generator_tool(destination: str, days: int, preferences: str = "") -> str:
    """
    Generate a detailed day-by-day itinerary for a given destination and duration.
    Use this when the user wants a travel plan or itinerary.
    """
    # TODO: implement LLM-driven itinerary generation using user preferences and RAG context
    raise NotImplementedError("itinerary_generator_tool is not yet implemented")
