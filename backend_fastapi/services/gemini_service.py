# Placeholder for Gemini LLM API integration
# Use httpx for async HTTP calls

class GeminiService:
    def __init__(self):
        import httpx
        from config import GEMINI_API_KEY, GEMINI_EMBED_MODEL, GEMINI_GEN_MODEL, HTTP_TIMEOUT
        from typing import List

        def _embed_url() -> str:
            return f"https://generativelanguage.googleapis.com/v1/{GEMINI_EMBED_MODEL}:batchEmbedContents?key={GEMINI_API_KEY}"

        def _gen_url() -> str:
            return f"https://generativelanguage.googleapis.com/v1/models/{GEMINI_GEN_MODEL}:generateContent?key={GEMINI_API_KEY}"

        class GeminiService:
            def __init__(self):
                pass

            async def embed_texts(self, texts: List[str]) -> List[List[float]]:
                if not texts:
                    return []
                payload = {
                    "requests": [
                        {"model": GEMINI_EMBED_MODEL, "content": {"parts":[{"text": t}]}}
                        for t in texts
                    ]
                }
                async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
                    r = await client.post(_embed_url(), json=payload)
                    r.raise_for_status()
                    data = r.json()
                    return [resp.get("embedding", {}).get("values", []) for resp in data.get("responses", [])]

            async def embed_query(self, text: str) -> List[float]:
                arr = await self.embed_texts([text])
                return arr[0] if arr else []

            async def generate(self, question: str, context: str) -> str:
                prompt = (
                    "You are an expert open-source developer.\n"
                    f"Context:\n{context}\n\n"
                    f"Question: {question}\n"
                    "Provide a clear, concise answer with citations (file paths)."
                )
                payload = {"contents": [{"role": "user", "parts": [{"text": prompt}]}]}
                async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
                    r = await client.post(_gen_url(), json=payload)
                    r.raise_for_status()
                    data = r.json()
                    return (
                        data.get("candidates", [{}])[0]
                        .get("content", {})
                        .get("parts", [{}])[0]
                        .get("text", "")
                    )
