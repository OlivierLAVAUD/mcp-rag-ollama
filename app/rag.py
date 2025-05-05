from langchain_ollama import OllamaEmbeddings  
from langchain.text_splitter import RecursiveCharacterTextSplitter  
from langchain_community.vectorstores import FAISS  
from langchain_core.documents import Document  
from config import config  
import logging  
  
"""logging.basicConfig(level=logging.INFO)  
logger = logging.getLogger(__name__) """ 

from utils.logging_utils import JSONLogger  
json_logger = JSONLogger("rag_processor")
for handler in json_logger.logger.handlers:
    if isinstance(handler, logging.FileHandler):
        handler.encoding = 'utf-8'
  

class RAGProcessor:  
    """  
    Processeur RAG (Retrieval-Augmented Generation) qui gère les embeddings,  
    le découpage de texte et la recherche vectorielle.  
    """  
    def __init__(self):  
        self.embeddings = OllamaEmbeddings(  
            model=config.EMBEDDING_MODEL,  
            base_url=config.OLLAMA_BASE_URL  
        )  
        self.text_splitter = RecursiveCharacterTextSplitter(  
            chunk_size=config.CHUNK_SIZE,  
            chunk_overlap=config.CHUNK_OVERLAP  
        )  
      
    async def create_from_documents(self, documents: list[Document]) -> FAISS:  
        """  
        Crée un vectorstore FAISS à partir d'une liste de documents  
        """ 
        json_logger.log(logging.INFO, "Création vectorstore",   
                   doc_count=len(documents)) 

#        logger.info(f"Création du vectorstore à partir de {len(documents)} documents")  
        split_docs = self.text_splitter.split_documents(documents)  
#        logger.info(f"Documents découpés en {len(split_docs)} chunks")         
         
        return await FAISS.afrom_documents(split_docs, self.embeddings)  
      
    async def similarity_search(self, query: str, vectorstore: FAISS, k: int = 3) -> list[Document]:  
        """  
        Effectue une recherche de similarité dans le vectorstore  
        """ 
        json_logger.log(logging.INFO, "Recherche de similarité pour: {query[:50]}...")  
 #       logger.info(f"Recherche de similarité pour: {query[:50]}...")  
        return await vectorstore.asimilarity_search(query, k=k)
    
    