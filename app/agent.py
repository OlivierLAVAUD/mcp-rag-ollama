import asyncio  
import sys  
from typing import Optional, List, Dict, Any  
from abc import ABC, abstractmethod  
from search import WebSearcher  
from rag import RAGProcessor  
from config import config  
import logging  
  
logging.basicConfig(level=logging.INFO)  
logger = logging.getLogger(__name__)  
  
class BaseAgent(ABC):  
    """  
    Classe de base abstraite pour tous les agents  
    """  
    @abstractmethod  
    async def query(self, prompt: str) -> str:  
        """  
        Méthode abstraite que tous les agents doivent implémenter  
        """  
        pass  
  
class OllamaAgent(BaseAgent):  
    """  
    Agent qui utilise Ollama pour la recherche et le RAG  
    """  
    def __init__(self):  
        self.searcher = WebSearcher()  
        self.rag = RAGProcessor()  
  
    async def query(self, prompt: str) -> str:  
        try:  
            formatted, docs = await self.searcher.execute(prompt)  
            if not docs:  
                return formatted  
              
            vectorstore = await self.rag.create_from_documents(docs)  
            relevant = await self.rag.similarity_search(prompt, vectorstore, k=config.RAG_RESULTS)  
              
            # Construction de l'analyse  
            analysis_parts = []  
            for doc in relevant:  
                if not doc.metadata.get('error'):  
                    content = doc.page_content  
                    # Nettoyage et formatage  
                    content = ' '.join(content.split())  # Supprime les espaces multiples  
                    if len(content) > 800:  
                        content = content[:800] + "... [suite sur le site]"  
                      
                    analysis_parts.append(  
                        f"**Source:** [{doc.metadata['source']}]({doc.metadata['source']})\n\n"  
                        f"{content}\n"  
                        f"{'-'*40}"  
                    )  
              
            # Formatage final  
            return (  
                f"{formatted}\n\n"  
                f"## Analyse contextuelle\n\n"  
                + "\n\n".join(analysis_parts)  
            )  
          
        except Exception as e:  
            logger.error(f"Erreur: {str(e)}")  
            return "Désolé, une erreur s'est produite. Veuillez réessayer."  
  
class AnalysisAgent(BaseAgent):  
    """  
    Agent spécialisé dans l'analyse de texte  
    """  
    def __init__(self):  
        self.rag = RAGProcessor()  
      
    async def query(self, text: str) -> str:  
        try:  
            # Création d'un document à partir du texte fourni  
            from langchain_core.documents import Document  
            doc = Document(page_content=text, metadata={"source": "user_input"})  
              
            # Analyse du texte  
            vectorstore = await self.rag.create_from_documents([doc])  
              
            # Formatage de l'analyse  
            return f"## Analyse du texte\n\nLe texte fourni contient {len(text)} caractères."  
          
        except Exception as e:  
            logger.error(f"Erreur d'analyse: {str(e)}")  
            return f"Erreur lors de l'analyse: {str(e)}"  
  
class GenerationAgent(BaseAgent):  
    """  
    Agent spécialisé dans la génération de contenu  
    """  
    def __init__(self):  
        from langchain_ollama import Ollama  
        self.llm = Ollama(  
            model=config.OLLAMA_MODEL,  
            base_url=config.OLLAMA_BASE_URL  
        )  
      
    async def query(self, prompt: str) -> str:  
        try:  
            # Génération de contenu avec le LLM  
            response = await self.llm.ainvoke(prompt)  
            return f"## Contenu généré\n\n{response}"  
          
        except Exception as e:  
            logger.error(f"Erreur de génération: {str(e)}")  
            return f"Erreur lors de la génération: {str(e)}"  
  
async def main():  
    agent = OllamaAgent()  
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Requête : ")  
    print(await agent.query(query))  
  
if __name__ == "__main__":  
    asyncio.run(main())