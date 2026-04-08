"""
Document Ingestion Service
Handles: PDF reading → text splitting → OpenAI embedding → FAISS storage → PostgreSQL metadata registration.
"""


def ingest_document(file_path: str, document_name: str, category: str, uploaded_by: int):
    """
    Full ingestion pipeline for a travel document.
    1. Read and split PDF into chunks
    2. Embed chunks via OpenAI
    3. Store vectors in FAISS index on disk
    4. Register document metadata and chunks in PostgreSQL
    """
    # TODO: implement ingestion pipeline
    raise NotImplementedError("ingest_document is not yet implemented")


def search_documents(query: str, role: str, top_k: int = 5) -> list[str]:
    """
    Perform a similarity search in FAISS, filtered by role_access_policies.
    Returns the top_k most relevant chunk texts.
    """
    # TODO: implement FAISS search with role-based filtering
    raise NotImplementedError("search_documents is not yet implemented")
