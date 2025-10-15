from fastapi import APIRouter, Depends
from main.db.session import get_session
from main.db.models import Document
from sqlmodel import Session, select
from schemas import DocMetadata

router = APIRouter(tags=["docs"])

@router.get("/documents", response_model=list[DocMetadata])
def list_documents(session: Session = Depends(get_session)):
    docs = session.exec(select(Document)).all()
    return [{"doc_id": d.id, "filename": d.filename, "num_chunks": d.num_chunks} for d in docs]
