from fastapi import FastAPI
from routers import ask, index, repos, health
from utils.logging import setup_logging
import config

setup_logging()

app = FastAPI(title="SupermanPython RAG Backend", version="0.1.0")

app.include_router(ask.router)
app.include_router(index.router)
app.include_router(repos.router)
app.include_router(health.router)
