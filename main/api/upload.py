from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from main.db.crud import create_document, add_chunk
from main.db.session import get_session
from sqlmodel import Session
from main.core.processor import Processor
import uuid
from schemas import UploadResponse

router = APIRouter(tags=["upload"])

# Singleton processor
processor = Processor()

@router.post("/pdf", response_model=UploadResponse)
async def upload_pdfs(files: list[UploadFile] = File(...), session: Session = Depends(get_session)):
    uploaded = []

    for f in files:
        try:
            content = await f.read()
            if not content:
                raise ValueError(f"File is empty: {f.filename}")

            # Parse and chunk file
            chunks = processor.parse_file(f.filename, f.content_type, content)

            # Create document record in DB
            doc = create_document(session, f.filename, f.content_type, len(content))

            # Add chunks to vector store and get IDs
            ids = processor.add_documents(doc_id_prefix=str(doc.id), texts=chunks)

            # Store each chunk in DB
            for cid, text in zip(ids, chunks):
                add_chunk(session, doc.id, cid, text)

            uploaded.append({"doc_id": doc.id, "filename": f.filename, "chunks": len(chunks)})

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to process {f.filename}: {e}")

    return uploaded[0]
