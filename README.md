# Dev Onboarding Helper

A full-stack app to help developers onboard faster by answering questions about a codebase using retrieval-augmented generation (RAG).

## Structure

- **backend/**: Python Flask API, repo crawler, chunker, embeddings, retriever, generator
- **frontend/**: Next.js UI, API route, React components
- **docker/**: Dockerfiles and docker-compose
- **docs/**: Architecture diagram, screenshots

## Quick Start

1. Build and run with Docker Compose:
   ```sh
   docker-compose -f docker/docker-compose.yml up --build
   ```
2. Access frontend at http://localhost:3000
3. API at http://localhost:5000

## License
MIT


## End-to-End User Workflow

This project implements a full Retrieval-Augmented Generation (RAG) pipeline using the Gemini API to answer questions about any public GitHub repository. Here’s how it works:

### 1. Indexing a GitHub Repository

- **User Action:**
   - On the frontend (Next.js), the user enters a GitHub repo name (e.g., `facebook/react`) in a search bar and clicks “Index Repo.”
- **Backend Process:**
   - The backend (Flask) fetches the repository’s code and documentation using the GitHub API.
   - Content (README, docs, code files) is chunked into smaller pieces (e.g., 500 tokens each).
   - Each chunk is converted into an embedding vector using Gemini’s embedding model.
   - Chunks and their embeddings are stored in a vector database (e.g., FAISS, Pinecone, or Weaviate).

### 2. Asking Questions About the Repo

- **User Action:**
   - The user types a question in the chatbox (e.g., “How does authentication work in this repo?”) and clicks “Ask.”
- **Backend Process:**
   - The backend generates an embedding for the user’s query using Gemini embeddings.
   - The vector DB retrieves the most relevant chunks (e.g., from README, `auth.js`, `config.py`).
   - The backend builds a prompt for Gemini:

      ```
      You are a helpful assistant. Use the following repo context to answer:

      Context:
      [chunk 1]
      [chunk 2]
      [chunk 3]

      Question: How does authentication work in this repo?
      ```
   - This prompt is sent to the Gemini text-generation API (e.g., gemini-1.5-flash).
   - Gemini responds with a precise, repo-specific answer.

### 3. Displaying the AI’s Response

- The frontend displays the answer in a styled chat interface (like ChatGPT, but repo-specific).
- Optionally, the UI can:
   - Show which repo files/chunks Gemini used (with file references and “Cite Source” links).
   - Provide a “Copy to Clipboard” button for code answers.

### 4. Continuous Usage

- Users can ask follow-up questions instantly (since the repo is already embedded in the DB).
- They can switch repos and re-index another one at any time.

### Example User Experience

1. Go to http://localhost:3000
2. Enter repo name: `facebook/react`
3. Click “Index Repo” (wait 2–5 seconds)
4. Ask: “How does React handle DOM updates internally?”
5. AI answers: “React uses a virtual DOM implementation… see ReactFiberReconciler.js for details.”
6. Links shown: `/packages/react-reconciler/src/ReactFiberReconciler.js`

### Why This Project Stands Out

- Not just a chatbot: it’s a real RAG pipeline (retrieval + generation)
- Uses real-world data (GitHub repos)
- Mixes frontend, backend, vector DB, and Gemini API (full-stack + AI skills)
- Flexible: can extend to any docs, not just repos
