# SupermanPython FastAPI Backend

This is the new FastAPI backend for the RAG-based GitHub Onboarding Helper.

## Features
- FastAPI with async endpoints
- Modular structure: routers, services, models, utils
- Endpoints: `/ask`, `/index`, `/repos`, `/health`
- Pydantic models for validation
- Placeholders for GitHub, FAISS, and Gemini integration
- Dockerfile and requirements.txt included
- Basic tests with pytest

## Project Structure

```
backend_fastapi/
├── main.py
├── routers/
│   ├── ask.py
│   ├── index.py
│   ├── repos.py
│   └── health.py
├── models/
│   ├── ask.py
│   ├── index.py
│   └── repos.py
├── services/
│   ├── github_service.py
│   ├── faiss_service.py
│   └── gemini_service.py
├── utils/
├── tests/
│   ├── test_health.py
│   ├── test_ask.py
│   ├── test_index.py
│   └── test_repos.py
├── requirements.txt
├── Dockerfile
└── README.md
```

## Running Locally

1. Install dependencies:
	```sh
	pip install -r requirements.txt
	```
2. Start the server:
	```sh
	uvicorn main:app --reload
	```
3. Run tests:
	```sh
	pytest
	```

## Next Steps
- Implement GitHub crawling and incremental updates
- Integrate FAISS for vector storage/search
- Add Gemini LLM API calls
- Expand tests and error handling
