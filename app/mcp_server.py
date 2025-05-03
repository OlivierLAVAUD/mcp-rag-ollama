import asyncio
from fastmcp import FastMCP
from agent import OllamaAgent
from config import config
import logging
from fastapi import FastAPI
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()  # Création au niveau module pour être importable

class MCPServer:
    def __init__(self, fastapi_app):
        self.agent = OllamaAgent()
        self.mcp = FastMCP(
            app=fastapi_app,
            name="Ollama Search Agent",
            version="1.0"
        )
        self.setup_routes()

    def setup_routes(self):
        @self.mcp.tool()
        async def search(query: str) -> str:
            logger.info(f"Processing query: {query}")
            return await self.agent.query(query)

# Initialisation
server = MCPServer(app)

def run():
    """Point d'entrée pour l'exécution directe"""
    uvicorn.run(
        "mcp_server:app",  # Format chaîne d'import
        host=config.MCP_HOST,
        port=config.MCP_PORT,
        reload=True
    )

if __name__ == "__main__":
    run()