# RAG-based GitHub Onboarding Helper - Architecture

```
[ User ]
   |
   v
[ Frontend (Next.js + React) ]
   |
   |--- Sends query (e.g., "How does auth work in this repo?")
   v
[ Backend API (FastAPI) ]
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
