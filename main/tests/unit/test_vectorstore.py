import pytest
from main.core.vector_store import VectorStore

@pytest.fixture
def vector_store():
    return VectorStore()

def test_add_documents(vector_store):
    docs = ["AI improves efficiency.", "ML models learn patterns."]
    vector_store.add_documents(docs)
    assert len(vector_store.db) == len(docs), "All documents should be stored"

def test_similarity_search(vector_store):
    # add dummy docs
    docs = ["AI improves efficiency.", "ML models learn patterns."]
    vector_store.add_documents(docs)
    results = vector_store.similarity_search("AI", top_k=1)
    assert isinstance(results, list), "Search should return a list"
    assert len(results) == 1, "Should return top_k results"
    assert any("AI" in r for r in results), "Should retrieve relevant document"
