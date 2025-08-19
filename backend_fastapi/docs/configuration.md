# Configuration Guide

## Environment Variables
- `GITHUB_TOKEN`: GitHub API token (recommended)
- `GEMINI_API_KEY`: Gemini LLM API key
- `GEMINI_EMBED_MODEL`: Embedding model name (default: text-embedding-004)
- `GEMINI_GEN_MODEL`: Generation model name (default: gemini-1.5-flash)
- `CHUNK_TOKENS`: Chunk size in tokens (default: 800)
- `CHUNK_OVERLAP`: Overlap in tokens (default: 200)
- `VECTOR_DIR`: Directory for FAISS/metadata (default: ./vectorstore)
- `HTTP_TIMEOUT`: HTTP timeout in seconds (default: 30)

## How to Set
- Create a `.env` file in the backend root or set variables in your deployment environment.
- Example `.env`:
  ```env
  GITHUB_TOKEN=your_github_token
  GEMINI_API_KEY=your_gemini_key
  ```

## Security
- Never commit secrets to version control.
- Use Docker secrets or cloud secret managers for production.

---
