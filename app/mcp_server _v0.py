import logging
from fastapi import FastAPI
from fastmcp import FastMCP
from agent_orchestrator import AgentOrchestrator
from config import config
from utils.logging_service import LoggingService
import uvicorn

class MCPServer:
    """Serveur MCP principal gérant les endpoints d'API"""

    def __init__(self, fastapi_app: FastAPI):
        """Initialise le serveur avec l'application FastAPI"""
        self.app = fastapi_app
        self.orchestrator = AgentOrchestrator()
        self.logger = LoggingService().get_logger(self.__class__.__name__)

        # Initialise FastMCP
        self.mcp = FastMCP(
            name=config.SERVER_NAME,
            version=config.SERVER_VERSION
        )

        # Configure les outils et les routes
        self._setup_tools()
        self._setup_routes()
        self._log_startup()

    def _setup_tools(self) -> None:
        """Configure les outils MCP"""

        @self.mcp.tool()
        async def search(query: str) -> str:
            """Endpoint de recherche"""
            self._log_request("search", query)
            return await self.orchestrator.process_query(query, "search")

        @self.mcp.tool()
        async def analyze(text: str) -> str:
            """Endpoint d'analyse de texte"""
            self._log_request("analyze", text)
            return await self.orchestrator.process_query(text, "analyze")

        @self.mcp.tool()
        async def generate(prompt: str) -> str:
            """Endpoint de génération de contenu"""
            self._log_request("generate", prompt)
            return await self.orchestrator.process_query(prompt, "generate")

        @self.mcp.tool()
        async def health() -> dict:
            """Endpoint de santé du serveur"""
            return {
                "status": "ok",
                "version": config.SERVER_VERSION,
                "service": config.SERVER_NAME
            }

    def _setup_routes(self) -> None:
        """Configure les routes FastAPI directement"""
        # Crée des routes FastAPI standard qui utilisent les outils MCP
        
        @self.app.post("/search")
        async def search_route(query: str) -> str:
            return await self.orchestrator.process_query(query, "search")

        @self.app.post("/analyze")
        async def analyze_route(text: str) -> str:
            return await self.orchestrator.process_query(text, "analyze")

        @self.app.post("/generate")
        async def generate_route(prompt: str) -> str:
            return await self.orchestrator.process_query(prompt, "generate")

        @self.app.get("/health")
        async def health_route() -> dict:
            return {
                "status": "ok",
                "version": config.SERVER_VERSION,
                "service": config.SERVER_NAME
            }

        # Route pour les outils MCP (si FastMCP fournit une interface)
        @self.app.get("/tools")
        async def list_tools():
            """Liste les outils MCP disponibles"""
            return {"tools": [tool.name for tool in self.mcp.tools]}

    def _log_request(self, endpoint: str, data: str) -> None:
        """Journalise les requêtes entrantes"""
        LoggingService().log_structured(
            logging.INFO,
            f"Traitement de la requête {endpoint}",
            self.__class__.__name__,
            {
                "type": endpoint,
                "data_sample": data[:200],
                "data_length": len(data)
            }
        )

    def _log_startup(self) -> None:
        """Journalise le démarrage du serveur"""
        self.logger.info(
            "Configuration du serveur MCP",
            extra={
                "host": config.SERVER_HOST,
                "port": config.SERVER_PORT,
                "debug": config.SERVER_DEBUG,
                "workers": config.SERVER_WORKERS
            }
        )

def create_app() -> FastAPI:
    """Factory pour l'application FastAPI"""
    app = FastAPI(
        title=config.SERVER_NAME,
        description=config.SERVER_DESCRIPTION,
        version=config.SERVER_VERSION
    )
    MCPServer(app)  # Initialise et configure le serveur
    return app

def run_server() -> None:
    """Lance le serveur Uvicorn"""
    uvicorn.run(
        "mcp_server:create_app",
        host=config.SERVER_HOST,
        port=config.SERVER_PORT,
        reload=config.SERVER_DEBUG,
        factory=True
    )

if __name__ == "__main__":
    run_server()





