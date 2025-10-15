from langchain_community.chat_models import ChatOpenAI
from settings import settings

class LLMProvider:
    def __init__(self):
        self.llm = ChatOpenAI(
            model_name="gemini-1.5-t",
            openai_api_key=settings.GEMINI_API_KEY,
            temperature=0.7,
            max_tokens=500
        )

    def generate_answer(self, prompt: str, context_chunks=[]):
        if context_chunks:
            context_text = "\n\n---\n\n".join(context_chunks)
            full_prompt = f"Answer based on context:\n{context_text}\n\nQuestion:\n{prompt}"
        else:
            full_prompt = prompt
        return self.llm(full_prompt)
