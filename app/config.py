import os
from dotenv import load_dotenv
from typing import Literal, Optional

load_dotenv()

class Config:
    """Configuration centralisée via .env"""
    
    # Ollama
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL")

    # Génération
    OLLAMA_MODEL_TEMPERATURE: float = float(os.getenv("OLLAMA_MODEL_TEMPERATURE"))
    OLLAMA_MODEL_MAX_TOKENS: int = int(os.getenv("OLLAMA_MODEL_MAX_TOKENS"))
    OLLAMA_MODEL_TOP_P: float = float(os.getenv("OLLAMA_MODEL_TOP_P"))
    
    # FAISS
    FAISS_TYPE: Literal["cpu", "gpu"] = os.getenv("FAISS_TYPE", "cpu")
    FAISS_INDEX_PATH: str = os.getenv("FAISS_INDEX_PATH")
    
    # RAG
    RAG_CHUNK_SIZE: int = int(os.getenv("RAG_CHUNK_SIZE"))
    RAG_CHUNK_OVERLAP: int = int(os.getenv("RAG_CHUNK_OVERLAP"))
    RAG_RESULTS: int = int(os.getenv("RAG_RESULTS"))
    # RAG_TEMPERATURE: float = float(os.getenv("RAG_TEMPERATURE"))
    
    # Recherche
    SEARCH_PROVIDER: Literal["exa", "firecrawl"] = os.getenv("SEARCH_PROVIDER")
    SEARCH_TIMEOUT: int = int(os.getenv("SEARCH_TIMEOUT"))
    SEARCH_MAX_RESULTS: int = int(os.getenv("SEARCH_MAX_RESULTS"))
    SEARCH_AUTOPROMPT: bool = os.getenv("SEARCH_AUTOPROMPT").lower() == "true"
    
    # API Keys
    SEARCH_API_KEY: Optional[str] = os.getenv("SEARCH_API_KEY")
    EXA_API_KEY: Optional[str] = os.getenv("EXA_API_KEY")
    FIRECRAWL_API_KEY: Optional[str] = os.getenv("FIRECRAWL_API_KEY")
    
    # Serveur MCP
    SERVER_NAME:        str = os.getenv("SERVER_NAME")
    SERVER_DESCRIPTION: str = os.getenv("SERVER_DESCRIPTION")
    SERVER_VERSION:     str = os.getenv("SERVER_VERSION")


    SERVER_HOST: str = os.getenv("SERVER_HOST")
    SERVER_PORT: int = int(os.getenv("SERVER_PORT"))
    SERVER_DEBUG: bool = os.getenv("SERVER_DEBUG").lower() == "true"
    SERVER_WORKERS: int = int(os.getenv("SERVER_WORKERS"))
    SERVER_LOG_LEVEL: str = os.getenv("SERVER_LOG_LEVEL")
    
    # Logging
    LOGGING_DIR: str = os.getenv("LOGGING_DIR")
    LOGGING_MAX_SIZE: int = int(os.getenv("LOGGING_MAX_SIZE", "10").strip().split()[0])
    # LOGGING_MAX_SIZE: int = int(os.getenv("LOGGING_MAX_SIZE")) sBUG
    LOGGING_BACKUP_COUNT: int = int(os.getenv("LOGGING_BACKUP_COUNT"))
    LOGGING_ENCODING: str = os.getenv("LOGGING_ENCODING")
    
    @classmethod

    def validate(cls):
        """Valide les configurations requises"""
        required = [
            'OLLAMA_MODEL',
            'OLLAMA_BASE_URL',
            'EMBEDDING_MODEL',
            'FAISS_INDEX_PATH'
        ]
        
        for var in required:
            if not getattr(cls, var):
                raise ValueError(f"La variable {var} est requise dans .env")
            

def get_model_options() -> dict:
    """Retourne les options du modèle configurées"""
    return {
        "temperature": Config.OLLAMA_LLM_TEMPERATURE,
        "num_predict": Config.OLLAMA_LLM_MAX_TOKENS,
        "top_p": Config.OLLAMA_LLM_TOP_P
    }

config = Config()
config.validate()