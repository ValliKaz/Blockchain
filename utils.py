import os
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

class DocumentProcessor:
    def __init__(self):
        # Initialize embeddings using Hugging Face
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        self.vector_store = None

    def process_documents(self, file_paths: List[str]) -> None:
        """Process multiple documents and store them in the vector database."""
        documents = []
        for file_path in file_paths:
            loader = PyPDFLoader(file_path)
            documents.extend(loader.load())
        
        # Split documents into chunks
        chunks = self.text_splitter.split_documents(documents)
        
        # Create vector store
        self.vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory="./chroma_db"
        )

    def query_documents(self, query: str, k: int = 3) -> List[str]:
        """Query the vector database for relevant document chunks."""
        if not self.vector_store:
            return []
        
        # Search for relevant documents
        docs = self.vector_store.similarity_search(query, k=k)
        return [doc.page_content for doc in docs] 