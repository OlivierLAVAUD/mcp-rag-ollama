from typing import Dict, Type, Optional
from agent import OllamaAgent, BaseAgent, AnalysisAgent, GenerationAgent
import logging
from utils.logging_service import LoggingService

class AgentOrchestrator:
    """
    Orchestrateur central pour la gestion des agents spécialisés.
    
    Responsabilités :
    - Maintenir un registre des types d'agents disponibles
    - Gérer le cycle de vie des instances d'agents
    - Router les requêtes vers les agents appropriés
    - Fournir une gestion centralisée des erreurs et du logging
    """
    
    # Registre des types d'agents disponibles
    AGENT_REGISTRY: Dict[str, Type[BaseAgent]] = {
        "search": OllamaAgent,
        "analyze": AnalysisAgent,
        "generate": GenerationAgent
    }

    def __init__(self):
        """Initialise l'orchestrateur avec un cache vide d'instances d'agents"""
        self.logger = LoggingService().get_logger(self.__class__.__name__)
        self._agent_instances: Dict[str, BaseAgent] = {}  # Cache d'instances

    def get_agent(self, agent_type: str) -> BaseAgent:
        """
        Obtient une instance d'agent, en la créant si nécessaire (pattern Singleton par type)
        
        Args:
            agent_type: Le type d'agent ('search', 'analyze' ou 'generate')
            
        Returns:
            Instance de l'agent demandé
            
        Raises:
            ValueError: Si le type d'agent n'est pas supporté
        """
        # Validation du type d'agent
        if agent_type not in self.AGENT_REGISTRY:
            error_msg = f"Type d'agent non supporté: {agent_type}"
            self.logger.error(error_msg, extra={"agent_type": agent_type})
            raise ValueError(error_msg)
        
        # Création lazy de l'instance si elle n'existe pas
        if agent_type not in self._agent_instances:
            self._agent_instances[agent_type] = self.AGENT_REGISTRY[agent_type]()
            self.logger.info(
                f"Nouvelle instance créée pour l'agent {agent_type}",
                extra={"agent_type": agent_type}
            )
        
        return self._agent_instances[agent_type]

    async def process_query(self, query: str, agent_type: str = "search") -> str:
        """
        Traite une requête en la routant vers l'agent approprié
        
        Args:
            query: La requête à traiter
            agent_type: Le type d'agent à utiliser ('search' par défaut)
            
        Returns:
            La réponse générée par l'agent
            
        Note:
            Logge les erreurs et retourne un message d'erreur convivial en cas d'échec
        """
        try:
            # Log de la requête entrante
            self._log_request(agent_type, query)
            
            # Récupération et exécution de l'agent
            agent = self.get_agent(agent_type)
            return await agent.query(query)
            
        except Exception as error:
            # Gestion centralisée des erreurs
            return self._handle_error(error, agent_type, query)

    def _log_request(self, agent_type: str, query: str) -> None:
        """Journalise les détails d'une requête entrante"""
        LoggingService().log_structured(
            logging.INFO,
            "Requête reçue",
            self.__class__.__name__,
            {
                "agent_type": agent_type,
                "query_length": len(query),
                "query_sample": query[:200]  # Log seulement un extrait
            }
        )

    def _handle_error(self, error: Exception, agent_type: str, query: str) -> str:
        """Gère et journalise les erreurs de traitement"""
        LoggingService().log_structured(
            logging.ERROR,
            "Erreur de traitement",
            self.__class__.__name__,
            {
                "error": str(error),
                "agent_type": agent_type,
                "query_sample": query[:200]
            }
        )
        return (
            "Désolé, une erreur s'est produite lors du traitement de votre requête. "
            "Notre équipe technique a été notifiée."
        )