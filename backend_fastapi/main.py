from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import ask, index, repos, health
from utils.logging import setup_logging
import config

setup_logging()

app = FastAPI(title="SupermanPython RAG Backend", version="0.1.0")

# CORS for frontend (adjust origins in production)
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(ask.router)
app.include_router(index.router)
app.include_router(repos.router)
app.include_router(health.router)
