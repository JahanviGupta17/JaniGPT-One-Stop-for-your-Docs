from settings import settings
import openai, httpx

class LLMClient:
    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        if self.provider == "openai":
            openai.api_key = settings.OPENAI_API_KEY

    async def generate(self, prompt: str, context_chunks: list):
        system = "You are an assistant that answers concisely based on uploaded documents."
        joined_context = "\n\n---\n\n".join(context_chunks)
        full_prompt = f"{system}\n\nContext:\n{joined_context}\n\nQuestion:\n{prompt}"
        if self.provider == "openai":
            resp = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role":"system","content":system},{"role":"user","content":full_prompt}],
                max_tokens=512,
                temperature=0.0,
            )
            return resp["choices"][0]["message"]["content"]
        else:
            async with httpx.AsyncClient() as client:
                resp = await client.post("http://example.com", json={"prompt": full_prompt})
                return resp.json().get("text", "")
