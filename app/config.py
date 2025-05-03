import os
from dotenv import load_dotenv
from typing import Literal

load_dotenv()

class Config:
    """Configuration centrale pour l'agent MCP Ollama"""
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

    # Ollama
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.2")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "llama3.2")
    
    # FAISS
    FAISS_TYPE = os.getenv("FAISS_TYPE", "cpu")  # cpu ou gpu

    # RAG
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", 4096))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", 512))
    RAG_RESULTS: int = int(os.getenv("RAG_RESULTS", 3))
    
    # Recherche
    SEARCH_PROVIDER: Literal["exa", "firecrawl"] = os.getenv("SEARCH_PROVIDER", "exa")
    EXA_API_KEY: str = os.getenv("EXA_API_KEY", "")
    FIRECRAWL_API_KEY: str = os.getenv("FIRECRAWL_API_KEY", "")
    SEARCH_TIMEOUT: int = int(os.getenv("SEARCH_TIMEOUT", 30))
    MAX_RESULTS: int = int(os.getenv("MAX_RESULTS", 5))
    
    # Serveur
    MCP_HOST: str = os.getenv("MCP_HOST", "0.0.0.0")
    MCP_PORT: int = int(os.getenv("MCP_PORT", 8000))

config = Config()