import asyncio
import sys
import logging
from typing import Optional, List, Dict, Any
from abc import ABC, abstractmethod
from search import WebSearcher
from rag import RAGProcessor
from ollama import AsyncClient
from config import config
from langchain_core.documents import Document
from langchain_ollama import OllamaLLM
from utils.logging_service import LoggingService

# Configuration de l'encodage standard
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

class BaseAgent(ABC):
    """
    Classe abstraite de base pour tous les agents.
    Fournit des fonctionnalités communes de logging et d'initialisation.
    """
    
    def __init__(self):
        """Initialise l'agent avec le système de logging"""
        self.logger = LoggingService().get_logger(self.__class__.__name__)
        self.logging_service = LoggingService()
        self._log_init()

    def _log_init(self) -> None:
        """Journalise l'initialisation de l'agent"""
        self.logging_service.log_structured(
            level=logging.INFO,
            message=f"Initialisation de l'agent {self.__class__.__name__}",
            module=self.__class__.__name__
        )

    def _log_query_result(self, prompt: str, response: str) -> None:
        """Journalise les résultats d'une requête"""
        self.logging_service.log_structured(
            level=logging.INFO,
            message="Résultat de requête",
            module=self.__class__.__name__,
            metadata={
                "prompt": prompt,
                "response_length": len(response),
                "response_sample": response[:1000] + "..." if len(response) > 1000 else response
            }
        )

    @abstractmethod
    async def query(self, prompt: str) -> str:
        """Méthode abstraite à implémenter par les sous-classes"""
        pass

class Summarizer:
    """Service dédié à la génération de résumés avec le modele LLM via Ollama"""
    
    def __init__(self, model: str = config.OLLAMA_MODEL):
        """Initialise le summarizer avec le modèle spécifié"""
        self.client = AsyncClient()
        self.model = model
        self.logger = LoggingService().get_logger(self.__class__.__name__)
        self.model_options = {
            "temperature": config.OLLAMA_MODEL_TEMPERATURE,
            "num_predict": config.OLLAMA_MODEL_MAX_TOKENS,
            "top_p": config.OLLAMA_MODEL_TOP_P
        }

    async def summarize(self, text: str) -> str:
        """
        Génère un résumé concis en français du texte fourni
        
        Args:
            text: Texte à résumer
            
        Returns:
            Le résumé généré ou une chaîne vide en cas d'erreur
        """
        # prompt = f"Génère un résumé concis en français de ce contenu:\n\n{text}"
        self.last_prompt = f"Fait la synthèse en langue française, du contenu de ces sources:\n\n{text}"
        try:
            response = await self.client.generate(
                model=self.model,
                prompt=self.last_prompt,
          #      prompt=prompt,
                options=self.model_options
            )
            
            self.logger.info(
                "Résumé généré avec succès",
                extra={
                    "model": self.model,
                    "input_length": len(text),
                    "output_length": len(response['response'])
                }
            )
            return response['response']
            
        except Exception as error:
            self.logger.error(
                "Échec de la génération de résumé",
                exc_info=True,
                extra={
                    "model": self.model,
                    "error": str(error),
                    "prompt_sample": prompt[:200]
                }
            )
            return ""

class OllamaAgent(BaseAgent):
    """
    Agent principal combinant recherche web et RAG avec Ollama.
    
    Workflow:
    1. Recherche web initiale
    2. Traitement RAG des résultats
    3. Génération de résumé synthétique
    4. Formatage de la réponse finale
    """
    
    def __init__(self):
        super().__init__()
        self.searcher = WebSearcher()
        self.rag = RAGProcessor()
        self.summarizer = Summarizer()

    async def query(self, prompt: str) -> str:
        """
        Traite une requête utilisateur et retourne une réponse enrichie
        
        Args:
            prompt: La requête de l'utilisateur
            
        Returns:
            Réponse formatée avec sources ou message d'erreur
        """
        try:
            self.logger.info("Début du traitement", extra={"prompt": prompt})
            
            # 1. Recherche initiale
            initial_summary, docs = await self.searcher.execute(prompt)
            if not docs:
                self._log_query_result(prompt, initial_summary)
                return initial_summary
              
            # 2. Traitement RAG
            vectorstore = await self.rag.create_from_documents(docs)
            relevant_docs = await self.rag.similarity_search(
                query=prompt,
                vectorstore=vectorstore,
                k=config.RAG_RESULTS
            )
            
            # 3. Formatage des sources
            sources_content, sources_used = self._format_sources(relevant_docs)
            
            # 4. Génération du résumé
            combined_content = initial_summary + "\n\n" + "\n".join(sources_content)
            final_summary = await self.summarizer.summarize(combined_content)
            
            # 5. Construction de la réponse finale
            response = self._build_final_response(final_summary, sources_content, sources_used)
            
            self._log_query_result(prompt, response)
            return response
            
        except Exception as error:
            self.logger.error(
                "Échec du traitement de la requête",
                exc_info=True,
                extra={
                    "prompt": prompt,
                    "error": str(error)
                }
            )
            return "Désolé, une erreur s'est produite. Veuillez réessayer."

    def _format_sources(self, docs: List[Document]) -> tuple:
        """Formate les documents sources pour l'affichage"""
        sources_content = []
        sources_used = []
        
        for doc in docs:
            if not doc.metadata.get('error'):
                content = ' '.join(doc.page_content.split())
                sources_content.append(
                    f"**Titre:** {doc.metadata.get('title', 'Sans titre')}\n"
                    f"**URL:** {doc.metadata['source']}\n"
                    f"**Contenu:**\n{content[:800]}...\n"
                    f"{'-'*50}"
                )
                sources_used.append(doc.metadata['source'])
                
        return sources_content, sources_used

    def _build_final_response(self, summary: str, sources: List[str], urls: List[str]) -> str:
        """Construit la réponse finale structurée"""
        return (
            f"## Synthèse\n\n{summary}\n\n"
            f"## Sources\n\n" + "\n\n".join(sources) +
            f"\n\n### URLs:\n" + "\n".join(f"- {url}" for url in urls)
        )

class AnalysisAgent(BaseAgent):
    """Agent spécialisé dans l'analyse de texte"""
    
    def __init__(self):
        super().__init__()
        self.rag = RAGProcessor()
    
    async def query(self, text: str) -> str:
        try:
            doc = Document(page_content=text, metadata={"source": "user_input"})
            await self.rag.create_from_documents([doc])
            
            response = (
                f"## Analyse de texte\n\n"
                f"Longueur: {len(text)} caractères\n"
                f"Mots: {len(text.split())}\n"
                f"Densité lexicale: {self._calculate_lexical_density(text):.1%}"
            )
            
            self._log_query_result(text, response)
            return response
            
        except Exception as error:
            self.logger.error(
                "Échec de l'analyse",
                exc_info=True,
                extra={
                    "text_sample": text[:200],
                    "error": str(error)
                }
            )
            return f"Erreur lors de l'analyse: {str(error)}"

    def _calculate_lexical_density(self, text: str) -> float:
        """Calcule la densité lexicale (ratio mots uniques / total mots)"""
        words = text.split()
        if not words:
            return 0.0
        return len(set(words)) / len(words)

class GenerationAgent(BaseAgent):
    """Agent spécialisé dans la génération de contenu avec LLM"""
    
    def __init__(self):
        super().__init__()
        self.llm = OllamaLLM(
            model=config.OLLAMA_MODEL,
            base_url=config.OLLAMA_BASE_URL,
            temperature=config.OLLAMA_MODEL_TEMPERATURE,
            num_predict=config.OLLAMA_MODEL_MAX_TOKENS,
            top_p=config.OLLAMA_MODEL_TOP_P
        )
    
    async def query(self, prompt: str) -> str:
        try:
            response = await self.llm.ainvoke(prompt)
            formatted_response = (
                f"## Contenu généré\n\n{response}\n\n"
                f"*Prompt original:*\n{prompt}"
            )
            
            self._log_query_result(prompt, formatted_response)
            return formatted_response
            
        except Exception as error:
            self.logger.error(
                "Échec de la génération",
                exc_info=True,
                extra={
                    "prompt": prompt,
                    "error": str(error)
                }
            )
            return f"Erreur lors de la génération: {str(error)}"

async def main():
    """Point d'entrée principal pour l'exécution en ligne de commande"""
    try:
        agent = OllamaAgent()
        query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Requête : ")
        
        print("\nTraitement en cours...\n")
        response = await agent.query(query)
        
        print("\n=== RÉSULTAT ===")
        print(response)
        
        # Sauvegarde du résultat
        with open("logs/reponse.txt", "w", encoding="utf-8") as f:
            f.write(response)
            
    except Exception as error:
        LoggingService().log_structured(
            level=logging.CRITICAL,
            message="Erreur critique dans le main",
            module="Main",
            metadata={"error": str(error)}
        )
        raise

if __name__ == "__main__":
    asyncio.run(main())