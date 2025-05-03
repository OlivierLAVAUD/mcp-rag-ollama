import asyncio
import sys
from typing import Optional, List, Dict
from search import WebSearcher
from rag import RAGProcessor
from config import config
import logging
from ollama import AsyncClient  # Supposons qu'on utilise la librairie Ollama Python

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMAnalyzer:
    def __init__(self, model: str = "mistral"):
        self.model = model
        self.client = AsyncClient()
    
    async def analyze_response(self, prompt: str, response: str) -> str:
        """Analyse la réponse avec un LLM pour vérifier la qualité, cohérence, etc."""
        analysis_prompt = (
            f"Analysez la réponse suivante à la requête '{prompt}':\n\n"
            f"{response}\n\n"
            "Évaluez:\n"
            "- La pertinence par rapport à la question\n"
            "- La cohérence des informations\n"
            "- La présence de biais ou d'inexactitudes\n"
            "- La clarté et l'organisation\n"
            "- La qualité des sources citées (si présentes)\n"
            "Fournissez une analyse structurée avec des suggestions d'amélioration si nécessaire."
        )
        
        try:
            response = await self.client.generate(
                model=self.model,
                prompt=analysis_prompt,
                options={
                    "temperature": 0.3,  # Pour une analyse plus factuelle
                    "num_ctx": 8000  # Contexte plus long pour l'analyse
                }
            )
            return response['response']
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse LLM: {str(e)}")
            return ""

    async def summarize_key_points(self, text: str) -> str:
        """Résume les points clés d'un texte avec un LLM"""
        try:
            response = await self.client.generate(
                model=self.model,
                prompt=f"Résumez les points clés de ce texte en 3-5 points et en francais bullet:\n\n{text}",
                options={"temperature": 0.2}
            )
            return response['response']
        except Exception as e:
            logger.error(f"Erreur lors du résumé: {str(e)}")
            return ""

class OllamaAgent:
    def __init__(self):
        self.searcher = WebSearcher()
        self.rag = RAGProcessor()
        self.analyzer = LLMAnalyzer()

    async def query(self, prompt: str) -> str:
        try:
            # Étape 1: Recherche initiale
            formatted, docs = await self.searcher.execute(prompt)
            if not docs:
                return formatted
            
            # Étape 2: Traitement RAG
            vectorstore = await self.rag.create_from_documents(docs)
            relevant = await self.rag.similarity_search(prompt, vectorstore, k=3)
            
            # Construction de l'analyse initiale
            analysis_parts = []
            sources_used = []
            
            for doc in relevant:
                if not doc.metadata.get('error'):
                    content = doc.page_content
                    content = ' '.join(content.split())
                    if len(content) > 800:
                        content = content[:800] + "... [suite sur le site]"
                    
                    analysis_parts.append(
                        f"**Source:** [{doc.metadata['source']}]({doc.metadata['source']})\n\n"
                        f"{content}\n"
                        f"{'-'*40}"
                    )
                    sources_used.append(doc.metadata['source'])
            
            # Formatage de la réponse initiale
            initial_response = (
                f"{formatted}\n\n"
                f"## Analyse contextuelle\n\n"
                + "\n\n".join(analysis_parts)
            )
            
            # Étape 3: Analyse LLM de la réponse
            llm_analysis = await self.analyzer.analyze_response(prompt, initial_response)
            summary = await self.analyzer.summarize_key_points(initial_response)
            
            # Construction de la réponse finale
            final_response = (

                f"{initial_response}\n\n"
                f"## Analyse LLM de la réponse\n\n"
                f"{llm_analysis}\n\n"

                f"## Resumé\n\n"
                f"{summary}\n\n"

                f"### Sources utilisées\n\n"
                + "\n".join(f"- {src}" for src in sources_used)
            )
            
            return final_response
        
        except Exception as e:
            logger.error(f"Erreur: {str(e)}", exc_info=True)
            return "Désolé, une erreur s'est produite. Veuillez réessayer."

async def main():
    agent = OllamaAgent()
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Requête : ")
    
    print("\nGénération de la réponse...\n")
    response = await agent.query(query)
    
    print("\n=== RÉSULTAT FINAL ===\n")
    print(response)
    
    # Optionnel: Sauvegarde dans un fichier
    with open("response_analysis.txt", "w", encoding="utf-8") as f:
        f.write(response)

if __name__ == "__main__":
    asyncio.run(main())