"""
Comparison Tool
Compares two or more destinations on key attributes such as cost, climate, activities, and travel time.
"""
from langchain.tools import tool


@tool
def comparison_tool(destinations: str) -> str:
    """
    Compare multiple travel destinations on cost, climate, activities, and suitability.
    Input should be a comma-separated list of destination names.
    Use this when the user wants to decide between destinations.
    """
    # TODO: implement destination comparison using RAG retrieval + structured output
    raise NotImplementedError("comparison_tool is not yet implemented")
