import asyncio  
from exa_py import Exa  
from typing import List, Tuple  
from langchain_core.documents import Document  
from config import config  
import requests  
from bs4 import BeautifulSoup  
import re  
from utils.logging_service import LoggingService

class WebSearcher:  
    def __init__(self):  
        self.exa = Exa(config.SEARCH_API_KEY)  
        self.headers = {  
            'User-Agent': config.SEARCH_PROVIDER
        }  
        self.logger = LoggingService().get_logger(self.__class__.__name__)

    async def execute(self, query: str) -> Tuple[str, List[Document]]:  
        try:  
            self.logger.info(
                "Exécution de la recherche",
                extra={"query": query}
            )
            
            # Recherche avec Exa  
            results = await asyncio.to_thread(  
                self.exa.search_and_contents,  
                query,  
                num_results=config.SEARCH_MAX_RESULTS,  
                use_autoprompt=config.SEARCH_AUTOPROMPT,  
                text={"include_html_tags": False}  
            )  
              
            formatted = self._format_results(results)  
            docs = await self._fetch_clean_content([r.url for r in results.results])  
            
            self.logger.info(
                "Recherche terminée",
                extra={
                    "query": query,
                    "results_count": len(docs),
                    "sources": [doc.metadata['source'] for doc in docs]
                }
            )
            
            return formatted, docs  
              
        except Exception as e:  
            self.logger.error(
                "Erreur de recherche",
                exc_info=True,
                extra={
                    "query": query,
                    "error": str(e)
                }
            )
            return "Erreur lors de la recherche", []  
  
    async def _fetch_clean_content(self, urls: List[str]) -> List[Document]:  
        """Récupère et nettoie le contenu des URLs"""  
        docs = []  
        for url in urls:  
            try:  
                content = await self._scrape_and_clean(url)  
                docs.append(Document(  
                    page_content=content,  
                    metadata={"source": url}  
                ))  
            except Exception as e:  
                self.logger.warning(
                    "Échec du chargement de l'URL",
                    extra={
                        "url": url,
                        "error": str(e)
                    }
                )
                docs.append(Document(  
                    page_content=f"Impossible de charger le contenu de {url}",  
                    metadata={"source": url, "error": True}  
                ))  
        return docs  
  
    async def _scrape_and_clean(self, url: str) -> str:  
        """Version améliorée avec extraction du contenu principal"""  
        try:  
            loop = asyncio.get_event_loop()  
            response = await loop.run_in_executor(  
                None,   
                lambda: requests.get(url, headers=self.headers, timeout=15)  
            )  
            response.raise_for_status()  
              
            soup = BeautifulSoup(response.text, 'html.parser')  
              
            # Suppression des éléments inutiles  
            for element in soup(['script', 'style', 'nav', 'footer', 'iframe', 'aside', 'form']):  
                element.decompose()  
              
            # Extraction prioritaire des balises article/main  
            main_content = soup.find(['article', 'main']) or soup  
              
            # Nettoyage avancé  
            text = ' '.join(main_content.stripped_strings)  
            text = re.sub(r'\s+', ' ', text)  # Espaces multiples  
            text = re.sub(r'\[[^\]]+\]', '', text)  # Notes [1]  
            text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)  # Emails  
              
            return text[:5000]  # Limite raisonnable  
          
        except Exception as e:  
            self.logger.warning(
                "Échec du scraping",
                exc_info=True,
                extra={
                    "url": url,
                    "error": str(e)
                }
            )
            return f"Contenu non disponible - {str(e)}"  
  
    def _format_results(self, results) -> str:  
        """Génère des résumés pertinents"""  
        output = []  
        for i, r in enumerate(results.results, 1):  
            title = r.title or "Sans titre"  
            url = r.url  
              
            # Génération de résumé améliorée  
            if hasattr(r, 'text') and r.text:  
                summary = ' '.join(r.text.split()[:50]) + "..."  # 50 premiers mots  
            else:  
                summary = "Aucun contenu textuel disponible"  
                  
            output.append(f"{i}. [{title}]({url})\n{summary}\n")  
          
        return "## Résultats de recherche\n\n" + "\n".join(output)