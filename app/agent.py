import asyncio
import sys
from datetime import datetime
from pathlib import Path
import logging
from typing import List
from search import WebSearcher
from rag import RAGProcessor
from ollama import AsyncClient

# Configuration du système de logs
LOG_DIR = Path("log")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / 'agent.log'

def setup_logging():
    """Configure le système de logging de manière robuste"""
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    file_handler = logging.FileHandler(LOG_FILE, mode='a', encoding='utf-8')
    console_handler = logging.StreamHandler()

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

setup_logging()
logger = logging.getLogger(__name__)

class Summarizer:
    """Classe dédiée à la génération de synthèse"""
    def __init__(self, model: str = "mistral"):
        self.client = AsyncClient()
        self.model = model
        self.last_prompt = ""  # Stocke le dernier prompt utilisé

    async def summarize(self, text: str) -> str:
        """Génère une synthèse concise en français"""
        self.last_prompt = (
            f"Résumez en paragraphes et en français ces sources:\n\n{text}"
        )
        
        try:
            response = await self.client.generate(
                model=self.model,
                prompt=self.last_prompt,
                options={"temperature": 0.3}
            )
            return response['response']
        except Exception as e:
            logger.error(f"Erreur lors de la synthèse: {str(e)}", exc_info=True)
            return ""

class OllamaAgent:
    def __init__(self):
        self.searcher = WebSearcher()
        self.rag = RAGProcessor()
        self.summarizer = Summarizer()
        logger.info("Agent Ollama initialisé")

    async def _log_interaction(self, query: str, response: str):
        """Enregistre l'interaction complète avec le prompt LLM"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        interaction_log = LOG_DIR / f"{timestamp}.log"
        
        log_content = (
            f"=== {datetime.now().isoformat()} ===\n"
            f"Question utilisateur: {query}\n\n"
            f"Prompt LLM utilisé:\n{self.summarizer.last_prompt}\n\n"
            f"Réponse générée:\n{response}\n"
            f"{'='*50}\n"
        )
        
        try:
            with open(interaction_log, 'w', encoding='utf-8') as f:
                f.write(log_content)
            logger.info(f"Interaction sauvegardée dans {interaction_log}")
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde: {str(e)}")

    async def query(self, prompt: str) -> str:
        """Traite une requête utilisateur"""
        logger.info(f"Début du traitement: '{prompt}'")
        
        try:
            # 1. Recherche initiale
            initial_summary, docs = await self.searcher.execute(prompt)
            if not docs:
                logger.warning("Aucun document trouvé")
                return initial_summary

            # 2. Extraction RAG
            vectorstore = await self.rag.create_from_documents(docs)
            relevant_docs = await self.rag.similarity_search(prompt, vectorstore, k=3)

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
                f"\n\n### URLs:\n" + "\n".join(f"- {url}" for url in sources_used)
            )

            await self._log_interaction(prompt, response)
            return response

        except Exception as e:
            logger.error(f"Erreur: {str(e)}", exc_info=True)
            return "Erreur lors du traitement."

async def main():
    logger.info("Démarrage application")
    agent = OllamaAgent()
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Requête : ")
    
    print("\nTraitement en cours...\n")
    response = await agent.query(query)
    
    print("\n=== RÉSULTAT ===")
    print(response)
    
    with open("reponse.txt", "w", encoding="utf-8") as f:
        f.write(response)
    
    logger.info("Traitement terminé")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.critical(f"ERREUR CRITIQUE: {str(e)}", exc_info=True)
        raise