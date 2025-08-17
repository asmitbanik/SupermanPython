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
