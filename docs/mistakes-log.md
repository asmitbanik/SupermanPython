# Mistakes & Decisions Log

Purpose: Track mistakes, fixes, and guardrails to avoid repeating them.

## 2025-08-26
- Improved RAG prompt building to avoid token overflow by budgeting context tokens. Guard: token counting via tiktoken fallback to whitespace.
- Added deduplication and per-path caps to reduce redundancy and improve diversity of context.
- Added retries with backoff for Gemini generation to handle transient errors.
- Safe JSON extraction for Gemini responses to avoid KeyError on malformed responses.
- Kept public function signatures in `backend/rag.py` intact to avoid breaking callers.
- Avoided changes outside RAG logic to prevent regressions in other modules.

## Ongoing Guardrails
- Prefer async I/O in new services; use retries and timeouts for all network calls.
- Maintain typed request/response contracts using pydantic in FastAPI.
- Always consider token budgets when constructing prompts.
- Persist and validate vector dimensions and index integrity when updating FAISS.
