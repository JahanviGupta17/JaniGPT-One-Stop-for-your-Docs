from sqlmodel import select, Session
from main.db.models import Document, DocChunk

def create_document(session: Session, filename: str, content_type: str, size: int) -> Document:
    doc = Document(filename=filename, content_type=content_type, size=size)
    session.add(doc)
    session.commit()
    session.refresh(doc)
    return doc

def add_chunk(session: Session, doc_id: int, chunk_id: str, text: str, token_count: int = None):
    chunk = DocChunk(doc_id=doc_id, chunk_id=chunk_id, text=text, token_count=token_count)
    session.add(chunk)
    session.commit()
    return chunk
