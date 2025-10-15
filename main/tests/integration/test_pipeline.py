from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_upload_documents():
    response = client.post("/upload", files={"file": ("test.txt", "AI is transforming education.")})
    assert response.status_code in (200, 201)
    assert "message" in response.json()

def test_query_response():
    response = client.post("/query", json={"query": "What is AI?"})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
