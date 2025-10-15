# JaniGPT: Retrieval-Augmented Generation System
### 1. Problem Statement

Organizations and researchers often manage large volumes of textual data—technical papers, policy documents, internal reports, and manuals—that are difficult to navigate efficiently. Conventional search mechanisms rely on keyword matching, which fails to capture contextual relevance and semantic meaning.
There is a growing need for an intelligent system that enables users to upload multiple documents and query them conversationally, receiving accurate and context-aware answers derived directly from the uploaded content.

### 2. Objective
![alt text](assets\unnamed.jpg)

The objective of this project is to design and implement a Retrieval-Augmented Generation (RAG) pipeline that enables:

i. Uploading and processing multiple documents of varying lengths and formats.

ii. Storing document embeddings for efficient semantic retrieval.

iii. Responding to user queries using context derived from the stored documents through a Large Language Model (LLM).

iv. Providing a modular and deployable solution using containerization for scalability and ease of use.

### 3. System Design and Solution Overview

The DocuQuery system combines document ingestion, vector storage, and language model reasoning in a unified architecture.

a. Document Ingestion and Processing

Accepts up to 20 documents, each with a maximum of 1000 pages.

Extracts and cleans text, splits it into contextually coherent chunks.

Generates embeddings using SentenceTransformers (all-MiniLM-L6-v2).

b. Vector Database and Retrieval

Embeddings are stored in a vector database (ChromaDB or FAISS).

When a query is submitted, the system retrieves the top-N most relevant document chunks based on cosine similarity.

c. Contextual Response Generation

Retrieved content is passed to an LLM (e.g., OpenAI GPT or Gemini) for contextual response synthesis.

The LLM combines the retrieved evidence with user intent to produce an accurate, citation-grounded answer.

d. API and Deployment

A FastAPI backend exposes REST endpoints for document upload, query submission, and metadata inspection.

The entire system is containerized via Docker Compose for seamless deployment on both local and cloud environments.

### 4. System Architecture
                   ┌────────────────────────────┐
                   │        User Interface       │
                   │   (Upload and Query)        │
                   └────────────┬────────────────┘
                                │
                   ┌────────────▼───────────────┐
                   │         FastAPI API         │
                   │ upload | query | metadata   │
                   └────────────┬────────────────┘
                                │
           ┌────────────────────▼────────────────────┐
           │      RAG Core Processing Pipeline       │
           │ chunking → embedding → retrieval → LLM  │
           └────────────────────┬────────────────────┘
                                │
                   ┌────────────▼───────────────┐
                   │      Vector Database       │
                   │     (ChromaDB / FAISS)     │
                   └────────────┬───────────────┘
                                │
                   ┌────────────▼───────────────┐
                   │   LLM API (OpenAI/Gemini)  │
                   └────────────────────────────┘

### 5. Implementation Details
a. Backend Stack

i. FastAPI for RESTful service architecture and request handling.
ii. LangChain for orchestrating retrieval and generation components.
iii. SentenceTransformers for efficient embedding generation.
iv. ChromaDB for local vector storage and similarity search.
v. SQLite (optional) for document metadata storage.

b. Deployment

i. Dockerfile defines containerized environment for FastAPI app.
ii. docker-compose.yml manages vector database and backend services.
iii. Supports deployment on AWS, GCP, or local Docker environments.

c. Testing

i. Unit tests ensure reliability of key modules (processing and vectorstore).
ii. Integration tests validate document ingestion, embedding, and retrieval pipeline.

### 6. Evaluation Metrics

The project is evaluated based on the following performance and design criteria:
![alt text](image.png)
 
### 7. Experimental Validation

a. Initial testing was performed using a mix of PDF and DOCX documents (research articles and reports).
Results indicate:
b. Successful ingestion and chunking across diverse formats.
c. Consistent retrieval precision for semantically related queries.
d. LLM responses remained contextually aligned and concise within the retrieved scope.

### 8. Tech Stack
![alt text](img2.png)

### 9. Directory Structure
DocuQuery/
│
├── main/
│   ├── api/              # FastAPI route definitions
│   ├── core/             # Embedding, retrieval, and processing modules
│   ├── db/               # Database and vector store initialization
│   ├── tests/            # Unit and integration test cases
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── show_test_output.py

### 10. Setup and Execution

Step 1: Clone and Install Dependencies
git clone https://github.com/JahanviGupta17/DocuQuery.git
cd DocuQuery
pip install -r requirements.txt
Step 2: Run the Application
uvicorn app:app --reload
Access interactive API documentation at:
http://127.0.0.1:8000/docs

Step 3: Run Tests
pytest -v

Step 4: Run via Docker
docker-compose up --build

### 11. Conclusion

DocuQuery demonstrates an end-to-end implementation of a Retrieval-Augmented Generation system with a focus on modularity, explainability, and deployability.
Its architecture is extendable for research and enterprise applications involving large-scale text intelligence, knowledge retrieval, and document-based question answering.