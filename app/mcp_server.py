import asyncio  
from fastapi import FastAPI, HTTPException  
from fastmcp import FastMCP  
from agent_orchestrator import AgentOrchestrator  
from config import config  
import logging  
import uvicorn


from utils.logging_utils import JSONLogger  
json_logger = JSONLogger("mcp_server")
for handler in json_logger.logger.handlers:
    if isinstance(handler, logging.FileHandler):
        handler.encoding = 'utf-8'  

# from utils.logging_utils import setup_logging, JSONLogger  
  
# Configuration du logging au démarrage du serveur  
#setup_logging(log_level=logging.INFO, log_file="logs/mcp_server.log")  
  
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
        self.setup_routes()  
          
    def setup_routes(self):  
        # Enregistrement des outils MCP  
        @self.mcp.tool()  
        async def search(query: str) -> str:  
            """Recherche d'informations via les agents"""
            json_logger.log(logging.INFO, f"Traitement de la requête de recherche: {query}", query=query)   
            #logger.info(f"Traitement de la requête de recherche: {query}")  
            return await self.orchestrator.process_query(query, agent_type="search")  
              
        @self.mcp.tool()  
        async def analyze(text: str) -> str:  
            """Analyse de texte via les agents"""  
            json_logger.log(logging.INFO, f"Traitement de la requête d'analyse: {text[:50]}...")  
            #logger.info(f"Traitement de la requête d'analyse: {text[:50]}...")  
            return await self.orchestrator.process_query(text, agent_type="analyze")  
              
        @self.mcp.tool()  
        async def generate(prompt: str) -> str:  
            """Génération de contenu via les agents"""
            json_logger.log(logging.INFO, f"Traitement de la requête de génération: {prompt[:50]}...")  
            #logger.info(f"Traitement de la requête de génération: {prompt[:50]}...")  
            return await self.orchestrator.process_query(prompt, agent_type="generate")  

        @self.mcp.tool()  
        async def health() -> dict:  
            """Vérification de l'état du serveur"""  
            return {"status": "ok", "version": "1.0"}  
  


# Initialisation  
server = MCPServer(app)  
  
def run():  
    """Point d'entrée pour l'exécution directe"""  
    uvicorn.run(  
        "mcp_server:app",  
        host=config.MCP_HOST,  
        port=config.MCP_PORT,  
        reload=config.DEBUG  
    )  
  
if __name__ == "__main__":  
    run()