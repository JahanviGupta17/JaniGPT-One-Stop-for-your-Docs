import pytest
from main.core.processor import Processor

@pytest.fixture
def processor():
    return Processor()

@pytest.fixture
def sample_docs():
    return [
        "Artificial Intelligence is transforming industries. "
        "It enables automation and better decision-making."
    ]

def test_chunk_documents(processor, sample_docs):
    chunks = processor.chunk_documents(sample_docs)
    assert isinstance(chunks, list), "Output should be a list"
    assert all(isinstance(chunk, str) for chunk in chunks), "Each chunk should be a string"
    assert len(chunks) > 0, "Chunking should produce at least one chunk"

def test_clean_text(processor):
    raw_text = "AI is awesome!!  🤖  "
    cleaned = processor.clean_text(raw_text)
    assert "!" not in cleaned, "Special characters should be removed"
    assert "🤖" not in cleaned, "Emojis should be removed"
    assert isinstance(cleaned, str), "Output should be a string"

