from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2:latest"

BACKEND_HOST = "127.0.0.1"
BACKEND_PORT = 5000

DATABASE_PATH = BASE_DIR / "solar_chat.db"
KNOWLEDGE_BASE_DIR = BASE_DIR / "Knowledge_base"
FRONTEND_DIR = BASE_DIR / "frontend"
DOCUMENTATION_DIR = BASE_DIR / "documentation"
