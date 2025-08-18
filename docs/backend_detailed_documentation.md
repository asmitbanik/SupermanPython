# SupermanPython Backend Documentation

This document provides detailed documentation for each Python file in the `backend` directory of the SupermanPython project. It covers the purpose, main functions/classes, and usage of each file.

---

## 1. app.py

**Purpose:**
- Entry point for the Flask API server.
- Exposes a `/api/ask` endpoint for question answering.

**Key Elements:**
- `app = Flask(__name__)`: Initializes the Flask app.
- `@app.route('/api/ask', methods=['POST'])`: Handles POST requests for questions.
- Returns a placeholder answer (integration with retriever/generator is expected).
- Runs the server on `0.0.0.0:5000` when executed directly.

---

## 2. chunker.py

**Purpose:**
- Splits large text documents into manageable chunks for embedding and retrieval.

**Key Functions:**
- `chunk_text(text, chunk_size=500)`: (Unused placeholder)
- `smart_chunk(doc)`: Splits a document by Markdown sections or code fences, then further splits by token count.
- `_tok_count(text)`: Counts tokens using tiktoken.
- `_window(text, max_tokens, overlap)`: Sliding window chunking by tokens.
- `chunk_docs(docs)`: Applies `smart_chunk` to a list of documents.

**Usage:**
- Used for preparing documents for embedding and search.

---

## 3. config.py

**Purpose:**
- Central configuration for API keys, model names, chunking parameters, and storage paths.

**Key Elements:**
- Loads environment variables for API keys and model names.
- Defines chunking and storage parameters (e.g., `CHUNK_TOKENS`, `DATA_DIR`).
- Ensures data directory exists.

---

## 4. crawler.py

**Purpose:**
- Placeholder for a GitHub repository crawler.

**Key Functions:**
- `crawl_repo(repo_url)`: To be implemented for crawling repositories.

---

## 5. embeddings.py

**Purpose:**
- Handles text embedding using the Google Gemini API.

**Key Functions:**
- `_batch_payload(texts)`: Prepares batch payload for the API.
- `_embed_batch(texts)`: Calls the Gemini API for a batch of texts.
- `embed_texts(texts, batch_size, max_retries)`: Embeds a list of texts in batches with retry logic.
- `embed_query(text)`: Embeds a single query string.

**Usage:**
- Used for generating vector representations of text for search and retrieval.

---

## 6. generator.py

**Purpose:**
- Placeholder for answer generation logic.

**Key Functions:**
- `generate_answer(context, question)`: To be implemented for generating answers from context and question.

---

## 7. github_crawler.py

**Purpose:**
- Incrementally crawls GitHub repositories, fetches file contents, and manages state.

**Key Functions:**
- `_repo_dir(repo)`: Returns the local directory for a repo.
- `_headers()`, `_session()`: Prepares HTTP headers and session for GitHub API.
- `get_latest_commit(repo, default_branch_hint)`: Gets the latest commit SHA.
- `load_state(repo)`, `save_state(repo, state)`: Loads/saves crawl state.
- `list_tree(repo, branch)`: Lists all files in a repo branch.
- `compare_commits(repo, base, head)`: Gets changed files between commits.
- `fetch_raw(repo, path, branch, etag_cache)`: Fetches raw file content, using ETag for caching.
- `crawl_repo_incremental(repo)`: Main function for incremental crawling; returns changed files and new head SHA.

---

## 8. index_store.py

**Purpose:**
- Manages storage and retrieval of vector embeddings and metadata using FAISS.

**Key Functions:**
- `_repo_dir(repo)`, `_paths(repo)`: Directory and file path helpers.
- `_normalize(V)`: Normalizes vectors.
- `load_all(repo)`, `save_all(repo, V, meta)`: Loads/saves all vectors and metadata.
- `upsert(repo, new_meta, new_vecs)`: Merges new vectors/metadata, rebuilds FAISS index.
- `load_faiss(repo)`: Loads FAISS index and metadata.
- `search(repo, qvec, top_k)`: Searches for top-k similar vectors.

---

## 9. rag.py

**Purpose:**
- Orchestrates retrieval-augmented generation (RAG) for question answering.

**Key Functions:**
- `index_repository(repo)`: Indexes changed files in a repo (crawling, chunking, embedding, upserting).
- `_build_contents(question, contexts)`: Builds a prompt for the generative model using context chunks.
- `answer_question(repo, question, top_k)`: Retrieves relevant chunks and generates an answer using Gemini API.

---

## 10. retriever.py

**Purpose:**
- Placeholder for vector search logic.

**Key Functions:**
- `retrieve(query)`: To be implemented for vector search.

---

## 11. utils.py

**Purpose:**
- Utility functions for the backend.

**Key Functions:**
- `sha1_text(s)`: Returns the SHA-1 hash of a string.

---

## 12. tests/test_app.py

**Purpose:**
- Unit tests for the Flask API in `app.py`.

**Key Elements:**
- `AppTestCase`: Test case for the Flask app.
- `setUp()`: Initializes test client.
- `test_ask()`: Tests the `/api/ask` endpoint for correct response.

---

# End of Documentation
