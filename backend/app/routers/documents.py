"""
Documents Router
Handles document upload, ingestion (PDF → chunks → FAISS), and metadata management.
"""
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/documents", tags=["documents"])


def get_db():
    from database import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def list_documents(db: Session = Depends(get_db)):
    """List all active documents in the registry."""
    from models import Document
    return db.query(Document).filter(Document.is_active == "TRUE").all()


@router.post("/upload")
def upload_document(
    file: UploadFile = File(...),
    category: str = "guide",
    db: Session = Depends(get_db)
):
    """
    Upload and ingest a travel document (PDF).
    Splits into chunks, embeds via OpenAI, stores in FAISS, and registers metadata in PostgreSQL.
    """
    # TODO: implement PDF ingestion pipeline via services/document_service.py
    raise NotImplementedError("Document upload is not yet implemented")


@router.delete("/{document_id}")
def deactivate_document(document_id: int, db: Session = Depends(get_db)):
    """Soft-delete a document by marking it inactive."""
    from models import Document
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    doc.is_active = "FALSE"
    db.commit()
    return {"message": f"Document {document_id} deactivated"}
