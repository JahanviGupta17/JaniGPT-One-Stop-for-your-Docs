from pydantic import BaseModel
from typing import List

class UploadResponse(BaseModel):
    doc_id: int
    filename: str
    chunks: int

class QueryRequest(BaseModel):
    q: str

class QueryResponse(BaseModel):
    answer: str
    retrieved_count: int

class DocMetadata(BaseModel):
    doc_id: int
    filename: str
    num_chunks: int
