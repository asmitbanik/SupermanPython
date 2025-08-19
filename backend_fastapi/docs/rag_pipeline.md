# RAG Pipeline: Step-by-Step

## 1. GitHub Integration
- Async crawling of public/private repos
- Incremental updates using commit SHA
- Fetches only text/code files

## 2. Chunking & Preprocessing
- Markdown/code-aware chunking
- Token-based (tiktoken) with overlap
- Each chunk stores file path, index, and text

## 3. Embedding & Vector Store
- Gemini embedding API (async, batched)
- FAISS for vector storage/search (per repo)
- Metadata stored alongside vectors

## 4. Retrieval
- Embed user query
- Top-k vector search in FAISS
- Return context chunks for LLM

## 5. LLM Integration
- Compose prompt with context + question
- Gemini LLM API (async)
- Return answer + citations (file paths, ranks, scores)

## 6. API Endpoints
- `/index`: Triggers full pipeline for a repo
- `/ask`: Answers a question using RAG
- `/repos`: Lists all indexed repos
- `/health`: Health check

---
