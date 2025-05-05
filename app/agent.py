import asyncio
import sys
import logging  # <-- Import manquant ajouté ici
from typing import Optional, List, Dict, Any
from abc import ABC, abstractmethod
from search import WebSearcher
from rag import RAGProcessor
from ollama import AsyncClient
from config import config
from langchain_core.documents import Document
from langchain_ollama import OllamaLLM
from utils.logging_service import LoggingService

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

class BaseAgent(ABC):
    """Classe de base abstraite pour tous les agents"""
    def __init__(self):
        self.logger = LoggingService().get_logger(self.__class__.__name__)
        self.logging = LoggingService()
        self._init_logging()
        
    def _init_logging(self):
        """Initialise le logging pour l'agent"""
        self.logging.log_structured(
            logging.INFO,
            f"Initialisation de {self.__class__.__name__}",
            self.__class__.__name__
        )

    def _log_result(self, prompt: str, response: str):
        """Log le résultat complet"""
        self.logging.log_structured(
            logging.INFO,
            "Résultat de la requête",
            self.__class__.__name__,
            {
                "prompt": prompt,
                "response_length": len(response),
                "response_sample": response[:1000] + "..." if len(response) > 1000 else response
            }
        )

    @abstractmethod
    async def query(self, prompt: str) -> str:
        pass

class Summarizer:
    """Classe dédiée à la génération de synthèse"""
    def __init__(self, model: str = "mistral"):
        self.client = AsyncClient()
        self.model = model
        self.last_prompt = ""
        self.logger = LoggingService().get_logger(self.__class__.__name__)

    async def summarize(self, text: str) -> str:
        """Génère une synthèse concise en français"""
        self.last_prompt = f"Fait la synthèse en langue française, du contenu de ces sources:\n\n{text}"
        try:
            response = await self.client.generate(
                model=self.model,
                prompt=self.last_prompt,
                options={"temperature": 0.3}
            )
            self.logger.info("Synthèse générée avec succès", extra={
                "model": self.model,
                "prompt_length": len(self.last_prompt),
                "response_length": len(response['response'])
            })
            return response['response']
        except Exception as e:
            self.logger.error("Erreur lors de la synthèse", exc_info=True, extra={
                "model": self.model,
                "prompt": self.last_prompt[:200]
            })
            return ""

class OllamaAgent(BaseAgent):
    """Agent qui utilise Ollama pour la recherche et le RAG"""
    def __init__(self):
        super().__init__()
        self.searcher = WebSearcher()
        self.rag = RAGProcessor()
        self.summarizer = Summarizer()

    async def query(self, prompt: str) -> str:
        try:
            self.logging.log_structured(
                logging.INFO,
                "Début du traitement",
                self.__class__.__name__,
                {"prompt": prompt}
            )
            
            # 1. Recherche initiale
            initial_summary, docs = await self.searcher.execute(prompt)
            if not docs:
                self._log_result(prompt, initial_summary)
                return initial_summary
              
            # 2. Extraction RAG
            vectorstore = await self.rag.create_from_documents(docs)
            relevant_docs = await self.rag.similarity_search(prompt, vectorstore, k=config.RAG_RESULTS)
            
            # 3. Formatage des sources
            sources_content = []
            sources_used = []
            
            for doc in relevant_docs:
                if not doc.metadata.get('error'):
                    content = ' '.join(doc.page_content.split())
                    sources_content.append(
                        f"**Titre:** {doc.metadata.get('title', 'Sans titre')}\n"
                        f"**URL:** {doc.metadata['source']}\n"
                        f"**Contenu:**\n{content[:800]}...\n"
                        f"{'-'*50}"
                    )
                    sources_used.append(doc.metadata['source'])

            # 4. Synthèse globale
            combined_content = initial_summary + "\n\n" + "\n".join(sources_content)
            final_summary = await self.summarizer.summarize(combined_content)

            # 5. Construction réponse
            response = (
                f"## Synthèse\n\n{final_summary}\n\n"
                f"## Sources\n\n" + "\n\n".join(sources_content) +
                f"\n\n### URLs:\n" + "\n".join(f"- {url}" for url in sources_used))
            
            self._log_result(prompt, response)
            return response
          
        except Exception as e:
            self.logger.error("Erreur lors du traitement", exc_info=True, extra={
                "prompt": prompt,
                "error": str(e)
            })
            return "Désolé, une erreur s'est produite. Veuillez réessayer."

class AnalysisAgent(BaseAgent):
    """Agent spécialisé dans l'analyse de texte"""
    def __init__(self):
        super().__init__()
        self.rag = RAGProcessor()
    
    async def query(self, text: str) -> str:
        try:
            doc = Document(page_content=text, metadata={"source": "user_input"})
            vectorstore = await self.rag.create_from_documents([doc])
            response = f"## Analyse du texte\n\nLe texte fourni contient {len(text)} caractères."
            
            self._log_result(text, response)
            return response
          
        except Exception as e:
            self.logger.error("Erreur d'analyse", exc_info=True, extra={
                "text_sample": text[:200],
                "error": str(e)
            })
            return f"Erreur lors de l'analyse: {str(e)}"

class GenerationAgent(BaseAgent):
    """Agent spécialisé dans la génération de contenu"""
    def __init__(self):
        super().__init__()
        self.llm = OllamaLLM(
            model=config.OLLAMA_MODEL,
            base_url=config.OLLAMA_BASE_URL
        )
    
    async def query(self, prompt: str) -> str:
        try:
            response = await self.llm.ainvoke(prompt)
            formatted_response = f"## Contenu généré\n\n{response}"
            
            self._log_result(prompt, formatted_response)
            return formatted_response
          
        except Exception as e:
            self.logger.error("Erreur de génération", exc_info=True, extra={
                "prompt": prompt,
                "error": str(e)
            })
            return f"Erreur lors de la génération: {str(e)}"

async def main():
    agent = OllamaAgent()
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Requête : ")
    
    print("\nTraitement en cours...\n")
    response = await agent.query(query)
    
    print("\n=== RÉSULTAT ===")
    print(response)
    
    # Sauvegarde du résultat
    with open("logs/reponse.txt", "w", encoding="utf-8") as f:
        f.write(response)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        LoggingService().log_structured(
            logging.CRITICAL,
            "Erreur critique",
            "Main",
            {"error": str(e)}
        )
        raise