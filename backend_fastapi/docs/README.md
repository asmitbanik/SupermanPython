# SupermanPython FastAPI Backend Documentation

This backend implements a production-ready, async Retrieval-Augmented Generation (RAG) system for developer onboarding, using FastAPI, FAISS, and Gemini LLM.

## Features
- **FastAPI**: Async, modular API with OpenAPI docs
- **RAG Pipeline**: GitHub crawling, chunking, embedding, vector search, LLM answer generation
- **Endpoints**:
  - `/index` (POST): Index a GitHub repo
  - `/ask` (POST): Ask a question about a repo
  - `/repos` (GET): List indexed repos
  - `/health` (GET): Health check
- **Services**: Modular, testable code for GitHub, chunking, embedding, vector store, and LLM
- **Production Ready**: Logging, config, error handling, Docker, tests

## Usage
1. Set environment variables in `.env` or system (see `config.py`)
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `uvicorn main:app --reload`
4. See OpenAPI docs at `/docs`

## RAG Pipeline Overview
1. **/index**: Crawl repo, chunk files, embed, store in FAISS
2. **/ask**: Embed question, retrieve top-k chunks, send to Gemini LLM, return answer + citations

## File Structure
- `main.py`: FastAPI app and router registration
- `routers/`: API endpoints
- `models/`: Pydantic schemas
- `services/`: Business logic (GitHub, chunking, FAISS, Gemini, RAG)
- `utils/`: Logging, helpers
- `config.py`: All config and secrets
- `tests/`: Pytest-based tests

## Deployment
- Use Dockerfile for containerization
- Set all secrets and keys via environment variables
- For production, use HTTPS, CORS, and monitoring

---
