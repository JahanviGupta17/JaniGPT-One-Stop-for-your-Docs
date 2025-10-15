import io, re
from PyPDF2 import PdfReader
from docx import Document as DocxDocument
from typing import List
from main.core.vector_store import VectorStore
from main.core.llm_client import LLMClient
from main.core.embeddings import EmbeddingsProvider
from settings import settings

class Processor:
    def __init__(self):
        self.vectorstore = VectorStore()
        self.emb_provider = EmbeddingsProvider()
        self.llm_client = LLMClient()

    # --- Text chunking ---
    def _chunk_text(self, text: str, chunk_size: int, overlap: int):
        tokens = text.split()
        i = 0
        while i < len(tokens):
            yield " ".join(tokens[i:i+chunk_size])
            i += chunk_size - overlap

    # --- File parsing ---
    def parse_file(self, filename: str, content_type: str, file_bytes: bytes) -> List[str]:
        if filename.lower().endswith(".pdf") or "pdf" in content_type:
            reader = PdfReader(io.BytesIO(file_bytes))
            text = "\n".join(p.extract_text() or "" for p in reader.pages)
        elif filename.lower().endswith(".docx"):
            doc = DocxDocument(io.BytesIO(file_bytes))
            text = "\n".join(p.text for p in doc.paragraphs)
        else:
            text = file_bytes.decode("utf-8", errors="ignore")

        text = re.sub(r'\s+', ' ', text).strip()
        return list(self._chunk_text(text, settings.CHUNK_SIZE, settings.CHUNK_OVERLAP))

    # --- Add documents to vector store ---
    def add_documents(self, doc_id_prefix: str, texts: List[str]):
        ids = [f"{doc_id_prefix}_{i}" for i in range(len(texts))]
        metas = [{"doc_id": doc_id_prefix, "chunk_index": i} for i in range(len(texts))]
        self.vectorstore.add_documents(ids=ids, texts=texts, metadatas=metas)
        return ids

    # --- Query ---
    async def ask(self, question: str, k: int = 3):
        q_emb = self.emb_provider.embed_texts([question])[0]
        docs = self.vectorstore.query([q_emb], k=k)
        context_chunks = [d.page_content for d in docs]
        answer = await self.llm_client.generate(question, context_chunks)
        return answer, len(context_chunks)
