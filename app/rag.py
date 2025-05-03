from langchain_ollama import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from config import config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGProcessor:
    def __init__(self):
        self.embeddings = OllamaEmbeddings(
            model=config.EMBEDDING_MODEL,
            base_url=config.OLLAMA_BASE_URL
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1024,
            chunk_overlap=200
        )

    async def create_from_documents(self, documents: list[Document]) -> FAISS:
        """Crée le vectorstore FAISS"""
        split_docs = self.text_splitter.split_documents(documents)
        return await FAISS.afrom_documents(split_docs, self.embeddings)

    async def similarity_search(self, query: str, vectorstore: FAISS, k: int = 3) -> list[Document]:
        """Effectue une recherche de similarité"""
        return await vectorstore.asimilarity_search(query, k=k)