import os
from dotenv import load_dotenv

load_dotenv()

# Google Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
EMBED_MODEL    = os.getenv("EMBED_MODEL", "models/text-embedding-004")     # 768d
GEN_MODEL      = os.getenv("GEN_MODEL", "models/gemini-1.5-flash")         # fast; or 1.5-pro

# GitHub (recommended to avoid rate limits)
GITHUB_TOKEN   = os.getenv("GITHUB_TOKEN", "")

# Indexing
CHUNK_TOKENS   = int(os.getenv("CHUNK_TOKENS", "800"))
CHUNK_OVERLAP  = int(os.getenv("CHUNK_OVERLAP", "200"))
TOP_K          = int(os.getenv("TOP_K", "5"))

# Storage
BASE_DIR       = os.path.dirname(__file__)
DATA_DIR       = os.getenv("DATA_DIR", os.path.join(BASE_DIR, "data"))
os.makedirs(DATA_DIR, exist_ok=True)

# HTTP timeouts
HTTP_TIMEOUT   = float(os.getenv("HTTP_TIMEOUT", "30"))
