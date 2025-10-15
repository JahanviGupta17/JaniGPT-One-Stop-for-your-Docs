# main/core/embeddings.py
from langchain_community.embeddings import HuggingFaceEmbeddings

class EmbeddingsProvider:
    def __init__(self):
        self.model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"}  # or "cuda" if GPU
        )

    def embed_texts(self, texts: list):
        # This returns list of embeddings
        return self.model.embed_documents(texts)
