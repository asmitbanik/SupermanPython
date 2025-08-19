import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# GitHub
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

# Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_EMBED_MODEL = os.getenv("GEMINI_EMBED_MODEL", "models/text-embedding-004")
GEMINI_GEN_MODEL = os.getenv("GEMINI_GEN_MODEL", "models/gemini-1.5-flash")

# Chunking
CHUNK_TOKENS = int(os.getenv("CHUNK_TOKENS", "800"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))

# Vector DB
VECTOR_DIR = os.getenv("VECTOR_DIR", str(Path(__file__).parent / "vectorstore"))

# Other
HTTP_TIMEOUT = float(os.getenv("HTTP_TIMEOUT", "30"))
