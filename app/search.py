import asyncio  
from exa_py import Exa  
from typing import List, Tuple  
from langchain_core.documents import Document  
from config import config  
import logging  
import requests  
from bs4 import BeautifulSoup  
import re  
  
"""logging.basicConfig(level=logging.INFO)  
logger = logging.getLogger(__name__)  """

from utils.logging_utils import JSONLogger  
json_logger = JSONLogger("web_searcher")  

class WebSearcher:  
    def __init__(self):  
        self.exa = Exa(config.EXA_API_KEY)  
        self.headers = {  
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'  
        }  
  
    async def execute(self, query: str) -> Tuple[str, List[Document]]:  
        try:  
            # Recherche avec Exa  
            results = await asyncio.to_thread(  
                self.exa.search_and_contents,  
                query,  
                num_results=3,  
                use_autoprompt=True,  
                text={"include_html_tags": False}  
            )  
              
            formatted = self._format_results(results)  
            docs = await self._fetch_clean_content([r.url for r in results.results])  
            return formatted, docs  
              
        except Exception as e:  
            logger.error(f"Erreur de recherche: {str(e)}")  
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
                logger.warning(f"Échec sur {url}: {str(e)}")  
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
            logger.warning(f"Échec du scraping {url}: {str(e)}")  
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