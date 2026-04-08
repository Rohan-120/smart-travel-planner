"""
Budget Optimization Tool
Recommends the best travel plans that fit within a specified budget.
"""
from langchain.tools import tool


@tool
def budget_optimizer_tool(destination: str, budget: int, days: int) -> str:
    """
    Suggest the best travel plan for a destination within a given budget and trip duration.
    Use this when the user specifies a budget constraint and wants optimized recommendations.
    """
    # TODO: implement budget-aware planning using preferences and RAG context
    raise NotImplementedError("budget_optimizer_tool is not yet implemented")
