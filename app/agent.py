import asyncio
import sys
from typing import Optional
from search import WebSearcher
from rag import RAGProcessor
from config import config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OllamaAgent:
    def __init__(self):
        self.searcher = WebSearcher()
        self.rag = RAGProcessor()


    async def query(self, prompt: str) -> str:
        try:
            formatted, docs = await self.searcher.execute(prompt)
            if not docs:
                return formatted
            
            vectorstore = await self.rag.create_from_documents(docs)
            relevant = await self.rag.similarity_search(prompt, vectorstore, k=3)
            
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
            
            # Formatage final corrigé
            return (
                f"{formatted}\n\n"
                f"## Analyse contextuelle\n\n"
                + "\n\n".join(analysis_parts)
            )
        
        except Exception as e:
            logger.error(f"Erreur: {str(e)}")
            return "Désolé, une erreur s'est produite. Veuillez réessayer."

async def main():
    agent = OllamaAgent()
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Requête : ")
    print(await agent.query(query))

if __name__ == "__main__":
    asyncio.run(main())