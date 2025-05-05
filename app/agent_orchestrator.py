from typing import Dict, Type, Optional  
from agent import OllamaAgent, BaseAgent, AnalysisAgent, GenerationAgent  
from utils.logging_service import LoggingService

class AgentOrchestrator:  
    """  
    Orchestrateur qui gère les différents agents et route les requêtes  
    vers l'agent approprié en fonction du type de requête.  
    """  
      
    def __init__(self):  
        self.logger = LoggingService().get_logger(self.__class__.__name__)
        # Registre des agents disponibles  
        self.agent_registry: Dict[str, Type[BaseAgent]] = {  
            "search": OllamaAgent,  
            "analyze": AnalysisAgent,  
            "generate": GenerationAgent  
        }  
          
        # Cache des instances d'agents  
        self.agent_instances: Dict[str, BaseAgent] = {}  
      
    def get_agent(self, agent_type: str) -> BaseAgent:  
        """  
        Récupère ou crée une instance d'agent du type spécifié  
        """  
        if agent_type not in self.agent_registry:  
            self.logger.error(
                "Type d'agent non supporté",
                extra={"agent_type": agent_type}
            )
            raise ValueError(f"Type d'agent non supporté: {agent_type}")  
              
        # Création de l'instance si elle n'existe pas déjà  
        if agent_type not in self.agent_instances:  
            agent_class = self.agent_registry[agent_type]  
            self.agent_instances[agent_type] = agent_class()  
            self.logger.info(
                f"Création d'une nouvelle instance d'agent {agent_type}",
                extra={"agent_type": agent_type}
            )
              
        return self.agent_instances[agent_type]  
      
    async def process_query(self, query: str, agent_type: str = "search") -> str:  
        """  
        Traite une requête en la routant vers l'agent approprié  
        """  
        try:
            LoggingService().log_structured(
                logging.INFO,
                "Routage de requête",
                self.__class__.__name__,
                {
                    "agent_type": agent_type,
                    "query_length": len(query),
                    "query_sample": query[:200]
                }
            )
            agent = self.get_agent(agent_type)  
            return await agent.query(query)  
        except Exception as e:
            LoggingService().log_structured(
                logging.ERROR,
                "Erreur de traitement",
                self.__class__.__name__,
                {
                    "error": str(e),
                    "agent_type": agent_type,
                    "query_sample": query[:200]
                }
            )
            return f"Une erreur s'est produite lors du traitement de votre requête: {str(e)}"