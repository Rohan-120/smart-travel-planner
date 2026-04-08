"""
Travel Retrieval Tool
RAG-based retrieval from FAISS — fetches relevant travel info from ingested documents.
Role-based access is enforced before retrieval using role_access_policies.
"""
from langchain.tools import tool


@tool
def travel_retrieval_tool(query: str) -> str:
    """
    Retrieve relevant travel information from the FAISS vector store.
    Use this tool when the user asks about destinations, hotels, or travel guides.
    """
    # TODO: implement FAISS similarity search with role-based document filtering
    raise NotImplementedError("travel_retrieval_tool is not yet implemented")
