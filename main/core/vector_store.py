import chromadb
from chromadb.config import Settings as ChromaSettings
from settings import settings

class VectorStore:
    def __init__(self):
        self.client = chromadb.Client(ChromaSettings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=settings.CHROMA_DIR
        ))
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"source": "rag-app"},
            embedding_function=None
        )

    def add_documents(self, ids, texts, embeddings, metadatas=None):
        self.collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas or []
        )
        self.client.persist()

    def query(self, query_embeddings, n=5):
        results = self.collection.query(
            query_embeddings=query_embeddings,
            n_results=n,
            include=["documents", "metadatas", "distances", "ids"]
        )
        return results
