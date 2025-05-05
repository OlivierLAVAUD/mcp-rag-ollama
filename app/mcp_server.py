import asyncio  
from fastapi import FastAPI, HTTPException  
from fastmcp import FastMCP  
from agent_orchestrator import AgentOrchestrator  
from config import config  
from utils.logging_service import LoggingService  
import uvicorn

app = FastAPI(  
    title="MCP A2A Server",  
    description="Serveur MCP implémentant le protocole Machine Conversation Protocol",  
    version="1.0.0"  
)  

class MCPServer:  
    def __init__(self, fastapi_app):  
        self.orchestrator = AgentOrchestrator()  
        self.mcp = FastMCP(  
            app=fastapi_app,  
            name="MCP A2A Server",  
            version="1.0",  
            description="Serveur MCP pour la communication agent-à-agent"  
        )  
        self.logger = LoggingService().get_logger(self.__class__.__name__)
        self.setup_routes()  
          
    def setup_routes(self):  
        @self.mcp.tool()  
        async def search(query: str) -> str:  
            """Recherche d'informations via les agents"""
            LoggingService().log_structured(
                logging.INFO,
                "Traitement de la requête de recherche",
                self.__class__.__name__,
                {"query": query, "type": "search"}
            )
            return await self.orchestrator.process_query(query, agent_type="search")  
              
        @self.mcp.tool()  
        async def analyze(text: str) -> str:  
            """Analyse de texte via les agents"""  
            LoggingService().log_structured(
                logging.INFO,
                "Traitement de la requête d'analyse",
                self.__class__.__name__,
                {"text_sample": text[:200], "type": "analyze"}
            )
            return await self.orchestrator.process_query(text, agent_type="analyze")  
              
        @self.mcp.tool()  
        async def generate(prompt: str) -> str:  
            """Génération de contenu via les agents"""
            LoggingService().log_structured(
                logging.INFO,
                "Traitement de la requête de génération",
                self.__class__.__name__,
                {"prompt_sample": prompt[:200], "type": "generate"}
            )
            return await self.orchestrator.process_query(prompt, agent_type="generate")  

        @self.mcp.tool()  
        async def health() -> dict:  
            """Vérification de l'état du serveur"""  
            return {"status": "ok", "version": "1.0"}  

server = MCPServer(app)  

def run():  
    """Point d'entrée pour l'exécution directe"""  
    LoggingService().get_logger("MCPServer").info(
        "Démarrage du serveur MCP",
        extra={
            "host": config.MCP_HOST,
            "port": config.MCP_PORT,
            "debug": config.DEBUG
        }
    )
    uvicorn.run(  
        "mcp_server:app",  
        host=config.MCP_HOST,  
        port=config.MCP_PORT,  
        reload=config.DEBUG  
    )  

if __name__ == "__main__":  
    run()