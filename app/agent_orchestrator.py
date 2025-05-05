from typing import Dict, Type, Optional  
from agent import OllamaAgent, BaseAgent, AnalysisAgent, GenerationAgent  
import logging  
 
from utils.logging_utils import JSONLogger  
  
logger = logging.getLogger(__name__)  
json_logger = JSONLogger("agent_orchestrator")

# logger = logging.getLogger(__name__)  

class AgentOrchestrator:  
    """  
    Orchestrateur qui gère les différents agents et route les requêtes  
    vers l'agent approprié en fonction du type de requête.  
    """  
      
    def __init__(self):  
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
            raise ValueError(f"Type d'agent non supporté: {agent_type}")  
              
        # Création de l'instance si elle n'existe pas déjà  
        if agent_type not in self.agent_instances:  
            agent_class = self.agent_registry[agent_type]  
            self.agent_instances[agent_type] = agent_class()  
              
        return self.agent_instances[agent_type]  
      
    async def process_query(self, query: str, agent_type: str = "search") -> str:  
        """  
        Traite une requête en la routant vers l'agent approprié  
        """  
        try:
            json_logger.log(logging.INFO, "Routage de requête",   
            agent_type=agent_type, query_length=len(query))
            agent = self.get_agent(agent_type)  
            return await agent.query(query)  
        except Exception as e:
            json_logger.log(logging.ERROR, "Erreur de traitement",   
                       error=str(e), agent_type=agent_type)
            #logger.error(f"Erreur lors du traitement de la requête: {str(e)}")  
            return f"Une erreur s'est produite lors du traitement de votre requête: {str(e)}"