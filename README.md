# SupermanPython: RAG-based GitHub Onboarding Helper

> **A full-stack, production-ready developer onboarding assistant using Retrieval-Augmented Generation (RAG), FastAPI, Next.js, Gemini LLM, and FAISS.**

---

## Overview
SupermanPython is an AI-powered onboarding assistant for developers joining new codebases. It crawls any GitHub repository, indexes code and docs, and answers natural language questions with context-grounded, cited responses. Built with a modern, scalable architecture and best practices for real-world deployment.

---

## Architecture
```
[ User ]
   |
   v
[ Frontend (Next.js + React) ]
   |
   |--- Sends query (e.g., "How does auth work in this repo?")
   v
[ Backend API (FastAPI, async) ]
   |
   |--- (1) Retrieves relevant code/docs from GitHub repo
   |--- (2) Stores & queries embeddings in Vector DB (FAISS)
   |--- (3) Augments user query with context
   |--- (4) Sends enriched query to Gemini LLM API
   |
   v
[ Gemini LLM API ]
   |
   |--- Processes question + repo context
   |--- Returns natural language + code snippet response
   v
[ Backend API (FastAPI) ]
   |
   |--- Sends final structured answer back
   v
[ Frontend (Next.js + React) ]
   |
   v
[ User ]
   -> Sees explanation, code snippet, onboarding guidance
```

---

## Features
- **RAG Pipeline**: Retrieval-augmented generation for accurate, cited answers
- **GitHub Integration**: Async crawling, incremental updates, supports public/private repos
- **Chunking**: Markdown/code-aware, token-based chunking for optimal context
- **Embeddings & Vector Search**: Gemini API + FAISS for fast, scalable retrieval
- **LLM Integration**: Gemini LLM for high-quality, context-grounded answers
- **Modern Frontend**: Next.js (React), beautiful UI, instant feedback
- **Production Ready**: Docker, .env config, logging, error handling, tests

---

## Tech Stack
- **Frontend**: Next.js, React, TypeScript, Axios
- **Backend**: FastAPI (async), Pydantic, httpx, FAISS, Gemini API, tiktoken
- **DevOps**: Docker, dotenv, pytest

---

## Project Structure
```
SupermanPython/
├── backend_fastapi/      # FastAPI async backend (RAG, FAISS, Gemini, GitHub)
│   ├── main.py
│   ├── routers/
│   ├── models/
│   ├── services/
│   ├── utils/
│   ├── docs/
│   ├── tests/
│   ├── config.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/             # Next.js frontend (React, TS)
│   ├── app/
│   ├── components/
│   ├── pages/
│   ├── public/
│   ├── .env.local
│   ├── package.json
│   └── next.config.js
├── docs/                 # Architecture, screenshots, detailed docs
│   ├── architecture/
│   └── ...
└── README.md             # (This file)
```

---

## How It Works
1. **Index a Repo**: Enter a GitHub repo (e.g., `facebook/react`) and click "Index Repo". The backend crawls, chunks, embeds, and stores all code/docs.
2. **Ask Questions**: Type any question about the repo. The backend retrieves relevant context, augments your query, and gets a cited answer from Gemini LLM.
3. **Get Cited Answers**: See answers with code snippets and file path citations for instant onboarding.

---

## Usage
### Backend
1. Set environment variables in `.env` (see `backend_fastapi/docs/configuration.md`)
2. Install dependencies:
   ```sh
   pip install -r backend_fastapi/requirements.txt
   ```
3. Run backend:
   ```sh
   uvicorn backend_fastapi.main:app --reload
   ```

### Frontend
1. Set `NEXT_PUBLIC_BACKEND_URL` in `frontend/.env.local` (default: `http://localhost:8000`)
2. Install dependencies:
   ```sh
   cd frontend
   npm install
   ```
3. Run frontend:
   ```sh
   npm run dev
   ```

---

## Testing
- Backend: `pytest backend_fastapi/tests/`
- Frontend: Use the UI and check API responses

---

## Documentation
- Backend: `backend_fastapi/docs/README.md`, `rag_pipeline.md`, `configuration.md`
- Frontend: `docs/frontend_detailed_documentation.md`
- Architecture: `docs/architecture/architecture.md`

---


## Author
- Asmit Banik

---

## License
MIT License
