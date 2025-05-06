from langchain_ollama import OllamaEmbeddings  
from langchain.text_splitter import RecursiveCharacterTextSplitter  
from langchain_community.vectorstores import FAISS  
from langchain_core.documents import Document  
from config import config  
from utils.logging_service import LoggingService

class RAGProcessor:  
    """  
    Processeur RAG (Retrieval-Augmented Generation) qui gère les embeddings,  
    le découpage de texte et la recherche vectorielle.  
    """  
    def __init__(self):  
        self.logger = LoggingService().get_logger(self.__class__.__name__)
        self.embeddings = OllamaEmbeddings(  
            model=config.EMBEDDING_MODEL,  
            base_url=config.OLLAMA_BASE_URL  
        )  
        self.text_splitter = RecursiveCharacterTextSplitter(  
            chunk_size=config.RAG_CHUNK_SIZE,
            chunk_overlap=config.RAG_CHUNK_OVERLAP  
        )  
      
    async def create_from_documents(self, documents: list[Document]) -> FAISS:  
        """  
        Crée un vectorstore FAISS à partir d'une liste de documents  
        """ 
        self.logger.info(
            "Création du vectorstore",
            extra={
                "doc_count": len(documents),
                "chunk_size": config.RAG_CHUNK_SIZE,
                "chunk_overlap": config.RAG_CHUNK_OVERLAP
            }
        )
        
        split_docs = self.text_splitter.split_documents(documents)  
        
        self.logger.info(
            "Documents découpés",
            extra={
                "initial_docs": len(documents),
                "split_docs": len(split_docs)
            }
        )
         
        return await FAISS.afrom_documents(split_docs, self.embeddings)  
      
    async def similarity_search(self, query: str, vectorstore: FAISS, k: int = 3) -> list[Document]:  
        """  
        Effectue une recherche de similarité dans le vectorstore  
        """ 
        self.logger.info(
            "Recherche de similarité",
            extra={
                "query": query[:200],
                "k": k
            }
        )
        
        results = await vectorstore.asimilarity_search(query, k=k)
        
        self.logger.info(
            "Résultats de la recherche",
            extra={
                "query": query[:200],
                "results_count": len(results)
            }
        )
        
        return results
    