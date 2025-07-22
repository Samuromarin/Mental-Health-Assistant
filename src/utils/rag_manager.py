"""
RAG Manager

Retrieval-Augmented Generation system using FAISS for knowledge enhancement.
Manages document indexing and semantic search for therapeutic content.
"""


import os
import logging
import pickle
import numpy as np
from typing import List, Dict, Any, Optional
from pathlib import Path

from src.config.settings import RAG_CONFIG

# LangChain imports
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document


# FAISS and SentenceTransformers imports
try:
    import faiss
    from sentence_transformers import SentenceTransformer
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False

class RAGManager:
    """Manager for Retrieval-Augmented Generation"""
    
    def __init__(self, 
                 documents_dir: str = None,
                 embeddings_model: str = None,
                 index_directory: str = None,
                 chunk_size: int = None,
                 chunk_overlap: int = None):
        """
        Initializes the RAG manager using centralized configuration
        """
        
        # Use RAG_CONFIG as defaults
        self.documents_dir = Path(documents_dir or RAG_CONFIG["documents_dir"])
        self.index_directory = Path(index_directory or RAG_CONFIG["index_dir"])
        self.chunk_size = chunk_size or RAG_CONFIG["chunk_size"]
        self.chunk_overlap = chunk_overlap or RAG_CONFIG["chunk_overlap"]
        self.embeddings_model_name = embeddings_model or RAG_CONFIG["embeddings_model"]
        
        # Create directories if they don't exist
        self.documents_dir.mkdir(parents=True, exist_ok=True)
        self.index_directory.mkdir(parents=True, exist_ok=True)
        
        # Configure logging
        self.logger = logging.getLogger(__name__)
        
        # Verify FAISS availability
        if not FAISS_AVAILABLE:
            raise ImportError("FAISS is not available. Install with: pip install faiss-cpu")
        
        # Initialize embeddings model
        self.model = None
        self.index = None
        self.documents = None
        self.metadata = None
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # Load existing index or prepare to create a new one
        self._load_or_initialize()
    
    def _load_embeddings_model(self):
        """Loads the embeddings model"""
        if self.model is None:
            try:
                self.logger.info(f"Loading embeddings model: {self.embeddings_model_name}")
                self.model = SentenceTransformer(self.embeddings_model_name)
                self.logger.info("Embeddings model loaded correctly")
            except Exception as e:
                self.logger.error(f"Error loading embeddings model: {e}")
                raise
    
    def _load_or_initialize(self):
        """Loads existing index or initializes to create a new one"""
        index_path = self.index_directory / "index.faiss"
        docs_path = self.index_directory / "documents.pkl"
        metadata_path = self.index_directory / "metadata.pkl"
        
        if index_path.exists() and docs_path.exists() and metadata_path.exists():
            try:
                self.logger.info("Loading existing FAISS index...")
                
                # Load FAISS index
                self.index = faiss.read_index(str(index_path))
                
                # Load documents
                with open(docs_path, 'rb') as f:
                    self.documents = pickle.load(f)
                
                # Load metadata
                with open(metadata_path, 'rb') as f:
                    self.metadata = pickle.load(f)
                
                self.logger.info(f"Index loaded: {len(self.documents)} documents")
                
            except Exception as e:
                self.logger.error(f"Error loading existing index: {e}")
                self.index = None
                self.documents = None
                self.metadata = None
        else:
            self.logger.info("No existing index found")
    
    def load_documents(self) -> List[Document]:
        """
        Loads documents from the configured directory
        
        Returns:
            List of loaded documents
        """
        documents = []
        
        if not self.documents_dir.exists():
            self.logger.warning(f"Documents directory does not exist: {self.documents_dir}")
            return documents
        
        # Supported file types
        supported_extensions = ['.md', '.txt']
        
        for extension in supported_extensions:
            for file_path in self.documents_dir.glob(f"**/*{extension}"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if content.strip():  # Only process files with content
                        doc = Document(
                            page_content=content,
                            metadata={
                                'source': str(file_path),
                                'source_file': file_path.name,
                                'file_type': extension
                            }
                        )
                        documents.append(doc)
                        self.logger.info(f"Loaded: {file_path.name}")
                        
                except Exception as e:
                    self.logger.error(f"Error loading {file_path}: {e}")
        
        self.logger.info(f"Total documents loaded: {len(documents)}")
        return documents
    
    def index_documents(self) -> bool:
        """
        Indexes documents in FAISS
        
        Returns:
            True if documents were indexed, False otherwise
        """
        try:
            # Load embeddings model
            self._load_embeddings_model()
            
            # Load documents
            documents = self.load_documents()
            
            if not documents:
                self.logger.warning("No documents found to index")
                return False
            
            # Split documents into chunks
            chunks = self.text_splitter.split_documents(documents)
            self.logger.info(f"Documents split into {len(chunks)} chunks")
            
            # Extract text and metadata
            texts = []
            metadata_list = []
            
            for i, chunk in enumerate(chunks):
                texts.append(chunk.page_content)
                chunk_metadata = chunk.metadata.copy()
                chunk_metadata.update({
                    'chunk_id': i,
                    'chunk_size': len(chunk.page_content)
                })
                metadata_list.append(chunk_metadata)
            
            # Generate embeddings
            self.logger.info("Generating embeddings...")
            embeddings = self.model.encode(texts, show_progress_bar=True)
            self.logger.info(f"Embeddings generated: {embeddings.shape}")
            
            # Create FAISS index
            self.logger.info("Creating FAISS index...")
            dimension = embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dimension)
            self.index.add(embeddings.astype('float32'))
            
            # Save documents and metadata
            self.documents = texts
            self.metadata = metadata_list
            
            # Persist index
            self._save_index()
            
            self.logger.info(f"Indexed {len(chunks)} chunks in FAISS")
            return True
            
        except Exception as e:
            self.logger.error(f"Error indexing documents: {e}")
            return False
    
    def _save_index(self):
        """Saves the FAISS index and metadata"""
        try:
            # Save FAISS index
            index_path = self.index_directory / "index.faiss"
            faiss.write_index(self.index, str(index_path))
            
            # Save documents
            docs_path = self.index_directory / "documents.pkl"
            with open(docs_path, 'wb') as f:
                pickle.dump(self.documents, f)
            
            # Save metadata
            metadata_path = self.index_directory / "metadata.pkl"
            with open(metadata_path, 'wb') as f:
                pickle.dump(self.metadata, f)
            
            self.logger.info("FAISS index saved correctly")
            
        except Exception as e:
            self.logger.error(f"Error saving index: {e}")
    
    def search_relevant_content(self, 
                              query: str, 
                              k: int = 3,
                              category: str = None,
                              relevance_threshold: float = 1.0) -> List[Dict[str, Any]]:
        """
        Searches for relevant content for a query
        
        Args:
            query: User query
            k: Number of results to return
            category: Mental health category (optional)
            relevance_threshold: Maximum distance for relevant results
            
        Returns:
            List of relevant documents with metadata
        """
        if not self.index or not self.documents:
            self.logger.error("FAISS index not available")
            return []
        
        try:
            # Load model if not loaded
            self._load_embeddings_model()
            
            # Enhance query with category context
            enhanced_query = query
            if category and category != "General":
                enhanced_query = f"{category}: {query}"
            
            # Generate query embedding
            query_embedding = self.model.encode([enhanced_query])
            
            # Search in FAISS
            distances, indices = self.index.search(query_embedding.astype('float32'), k)
            
            # Format results with relevance filtering
            formatted_results = []
            for distance, idx in zip(distances[0], indices[0]):
                # Only include results below threshold (more relevant)
                if idx < len(self.documents) and distance < relevance_threshold:
                    formatted_results.append({
                        'content': self.documents[idx],
                        'metadata': self.metadata[idx],
                        'relevance_score': float(distance),
                        'source': self.metadata[idx].get('source_file', 'unknown')
                    })
            
            self.logger.info(f"Found {len(formatted_results)} relevant documents (threshold: {relevance_threshold})")
            return formatted_results
            
        except Exception as e:
            self.logger.error(f"Error in search: {e}")
            return []
    
    def get_context_for_query(self, 
                            query: str, 
                            category: str = "General",
                            max_context_length: int = 2000) -> str:
        """
        Gets relevant context for a query
        
        Args:
            query: User query
            category: Mental health category
            max_context_length: Maximum context length
            
        Returns:
            Relevant context as string
        """
        # Search for relevant content with threshold
        relevant_docs = self.search_relevant_content(
            query, 
            k=3, 
            category=category, 
            relevance_threshold=1.2  
        )
        
        if not relevant_docs:
            self.logger.info("No relevant documents found above threshold")
            return ""  # No context = No RAG note
        
        # Build context
        context_parts = []
        current_length = 0
        
        for doc in relevant_docs:
            content = doc['content'].strip()
            
            # Check if adding this content would exceed the limit
            if current_length + len(content) > max_context_length:
                # Truncate content if necessary
                remaining_space = max_context_length - current_length
                if remaining_space > 100:  # Only add if significant space remains
                    content = content[:remaining_space] + "..."
                    context_parts.append(content)
                break
            
            context_parts.append(content)
            current_length += len(content)
        
        # Join all context parts
        context = "\n\n---\n\n".join(context_parts)
        
        if context:
            return f"Relevant information from the knowledge base:\n\n{context}"
        
        return ""
    
    def add_document_from_text(self, 
                             text: str, 
                             metadata: Dict[str, Any] = None) -> bool:
        """
        Adds a document from text directly
        
        Args:
            text: Document content
            metadata: Document metadata
            
        Returns:
            True if added correctly
        """
        try:
            # Create document
            doc = Document(
                page_content=text,
                metadata=metadata or {}
            )
            
            # Split into chunks
            chunks = self.text_splitter.split_documents([doc])
            
            if not chunks:
                return False
            
            # Load model if not loaded
            self._load_embeddings_model()
            
            # Generate embeddings for new chunks
            new_texts = [chunk.page_content for chunk in chunks]
            new_embeddings = self.model.encode(new_texts)
            
            # Add to existing index
            if self.index is None:
                # Create new index if it doesn't exist
                dimension = new_embeddings.shape[1]
                self.index = faiss.IndexFlatL2(dimension)
                self.documents = []
                self.metadata = []
            
            # Add embeddings to index
            self.index.add(new_embeddings.astype('float32'))
            
            # Add texts and metadata
            for i, chunk in enumerate(chunks):
                self.documents.append(chunk.page_content)
                chunk_metadata = chunk.metadata.copy()
                chunk_metadata.update({
                    'chunk_id': len(self.documents) - 1,
                    'chunk_size': len(chunk.page_content)
                })
                self.metadata.append(chunk_metadata)
            
            # Save updated index
            self._save_index()
            
            self.logger.info(f"Document added: {len(chunks)} chunks")
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding document: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Gets FAISS index statistics
        
        Returns:
            Dictionary with statistics
        """
        try:
            stats = {
                "documents_indexed": len(self.documents) if self.documents else 0,
                "documents_directory": str(self.documents_dir),
                "index_directory": str(self.index_directory),
                "chunk_size": self.chunk_size,
                "chunk_overlap": self.chunk_overlap,
                "embeddings_model": self.embeddings_model_name,
                "index_type": "FAISS"
            }
            
            if self.index:
                stats["faiss_index_size"] = self.index.ntotal
                stats["embedding_dimension"] = self.index.d
            
            return stats
            
        except Exception as e:
            return {"error": f"Error getting statistics: {e}"}


# Utility functions for easy integration
def initialize_rag_manager(**kwargs) -> Optional[RAGManager]:
    """
    Initializes the RAG manager with default configuration
    
    Returns:
        RAGManager instance or None if error
    """
    try:
        return RAGManager(**kwargs)
    except Exception as e:
        logging.error(f"Error initializing RAG: {e}")
        return None