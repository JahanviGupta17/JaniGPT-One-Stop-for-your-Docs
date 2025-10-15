# app.py
from fastapi.middleware.cors import CORSMiddleware
from main.db.session import init_db, get_session
from main.db.crud import create_document, add_chunk 
from main.core.processor import Processor
from sqlmodel import Session
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
import uuid

from settings import settings

app = FastAPI(
    title=settings.APP_NAME,
    version="0.1",
    description="RAG Pipeline API - Upload documents, query them, and explore docs interactively."
)

# Allow CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize core Processor singleton
processor = Processor()

@app.on_event("startup")
def startup_event():
    init_db()
    print("✅ Database initialized. RAG API is ready.")

@app.get("/api/health", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "API is running"}

@app.get("/api/hello", tags=["Test"])
def hello(name: str = "User"):
    return {"message": f"Hello, {name}! You can now interact with the RAG API."}

@app.get("/", tags=["Docs"])
def root():
    return {"message": "Go to /docs to interact with the RAG API."}

# Upload document endpoint
@app.post("/api/upload_file", tags=["Upload"])
async def upload_file(file: UploadFile = File(...), session: Session = Depends(get_session)):
    try:
        file_bytes = await file.read()
        if not file_bytes:
            raise HTTPException(status_code=400, detail="File is empty")

        # Parse file into chunks
        chunks = processor.parse_file(file.filename, file.content_type, file_bytes)
        # Add to vector store
        doc_id_prefix = f"doc_{file.filename}_{len(chunks)}"
        processor.add_documents(doc_id_prefix=doc_id_prefix, texts=chunks)

        # Optionally, store chunks in DB here if needed
        # for chunk_id, text in zip(ids, chunks):
        #     add_chunk(session, doc_id, chunk_id, text)

        return {"status": "ok", "chunks_added": len(chunks)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {e}")

# Query endpoint
@app.post("/api/query", tags=["Query"])
async def query_documents(question: str = Form(...), top_k: int = Form(3)):
    try:
        if top_k <= 0:
            top_k = 3

        answer, retrieved_count = await processor.ask(question, k=top_k)

        return {
            "question": question,
            "answer": answer,
            "retrieved_count": retrieved_count
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {e}")
