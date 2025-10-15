from fastapi import APIRouter
from main.core.embeddings import EmbeddingsProvider
from main.core.vector_store import VectorStore
from main.core.llm_client import LLMClient
from settings import settings
from schemas import QueryRequest, QueryResponse

router = APIRouter(tags=["query"])

# Initialize providers
emb = EmbeddingsProvider()
vs = VectorStore()
llm = LLMClient()

@router.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    # 1. Embed the query
    q_emb = emb.embed_texts([request.q])[0]

    # 2. Retrieve relevant documents using embedding
    res = vs.query([q_emb], k=settings.MAX_RETRIEVALS)

    # Chroma similarity_search_by_vector returns list of Document objects
    # Extract the text from the returned documents
    docs = [d['document'] if isinstance(d, dict) and 'document' in d else str(d) for d in res]

    # 3. Generate answer using LLM
    answer = await llm.generate(request.q, docs)

    return QueryResponse(
        answer=answer,
        retrieved_count=len(docs)
    )
