"""
Gestor RAG (Retrieval-Augmented Generation) usando FAISS
Versión simplificada y confiable para el asistente de salud mental
"""

import os
import logging
import pickle
import numpy as np
from typing import List, Dict, Any, Optional
from pathlib import Path

# LangChain imports simplificados
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

# Importaciones FAISS y SentenceTransformers
try:
    import faiss
    from sentence_transformers import SentenceTransformer
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False

class RAGManager:
    """Gestor para Retrieval-Augmented Generation usando FAISS"""
    
    def __init__(self, 
                 documents_dir: str = "src/data/documents",
                 embeddings_model: str = "all-MiniLM-L6-v2",
                 index_directory: str = "src/data/faiss_index",
                 chunk_size: int = 1000,
                 chunk_overlap: int = 200):
        """
        Inicializa el gestor RAG con FAISS
        
        Args:
            documents_dir: Directorio donde están los documentos a indexar
            embeddings_model: Modelo de embeddings a usar
            index_directory: Directorio para el índice FAISS
            chunk_size: Tamaño de los chunks de texto
            chunk_overlap: Solapamiento entre chunks
        """
        self.documents_dir = Path(documents_dir)
        self.index_directory = Path(index_directory)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embeddings_model_name = embeddings_model
        
        # Crear directorios si no existen
        self.documents_dir.mkdir(parents=True, exist_ok=True)
        self.index_directory.mkdir(parents=True, exist_ok=True)
        
        # Configurar logging
        self.logger = logging.getLogger(__name__)
        
        # Verificar disponibilidad de FAISS
        if not FAISS_AVAILABLE:
            raise ImportError("FAISS no está disponible. Instala con: pip install faiss-cpu")
        
        # Inicializar modelo de embeddings
        self.model = None
        self.index = None
        self.documents = None
        self.metadata = None
        
        # Inicializar text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # Cargar índice existente o preparar para crear uno nuevo
        self._load_or_initialize()
    
    def _load_embeddings_model(self):
        """Carga el modelo de embeddings"""
        if self.model is None:
            try:
                self.logger.info(f"Cargando modelo de embeddings: {self.embeddings_model_name}")
                self.model = SentenceTransformer(self.embeddings_model_name)
                self.logger.info("Modelo de embeddings cargado correctamente")
            except Exception as e:
                self.logger.error(f"Error cargando modelo de embeddings: {e}")
                raise
    
    def _load_or_initialize(self):
        """Carga el índice existente o inicializa para crear uno nuevo"""
        index_path = self.index_directory / "index.faiss"
        docs_path = self.index_directory / "documents.pkl"
        metadata_path = self.index_directory / "metadata.pkl"
        
        if index_path.exists() and docs_path.exists() and metadata_path.exists():
            try:
                self.logger.info("Cargando índice FAISS existente...")
                
                # Cargar índice FAISS
                self.index = faiss.read_index(str(index_path))
                
                # Cargar documentos
                with open(docs_path, 'rb') as f:
                    self.documents = pickle.load(f)
                
                # Cargar metadatos
                with open(metadata_path, 'rb') as f:
                    self.metadata = pickle.load(f)
                
                self.logger.info(f"Índice cargado: {len(self.documents)} documentos")
                
            except Exception as e:
                self.logger.error(f"Error cargando índice existente: {e}")
                self.index = None
                self.documents = None
                self.metadata = None
        else:
            self.logger.info("No se encontró índice existente")
    
    def load_documents(self) -> List[Document]:
        """
        Carga documentos desde el directorio configurado
        
        Returns:
            Lista de documentos cargados
        """
        documents = []
        
        if not self.documents_dir.exists():
            self.logger.warning(f"Directorio de documentos no existe: {self.documents_dir}")
            return documents
        
        # Tipos de archivo soportados
        supported_extensions = ['.md', '.txt']
        
        for extension in supported_extensions:
            for file_path in self.documents_dir.glob(f"**/*{extension}"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if content.strip():  # Solo procesar archivos con contenido
                        doc = Document(
                            page_content=content,
                            metadata={
                                'source': str(file_path),
                                'source_file': file_path.name,
                                'file_type': extension
                            }
                        )
                        documents.append(doc)
                        self.logger.info(f"Cargado: {file_path.name}")
                        
                except Exception as e:
                    self.logger.error(f"Error cargando {file_path}: {e}")
        
        self.logger.info(f"Total de documentos cargados: {len(documents)}")
        return documents
    
    def index_documents(self) -> bool:
        """
        Indexa los documentos en FAISS
        
        Returns:
            True si se indexaron documentos, False en caso contrario
        """
        try:
            # Cargar modelo de embeddings
            self._load_embeddings_model()
            
            # Cargar documentos
            documents = self.load_documents()
            
            if not documents:
                self.logger.warning("No se encontraron documentos para indexar")
                return False
            
            # Dividir documentos en chunks
            chunks = self.text_splitter.split_documents(documents)
            self.logger.info(f"Documentos divididos en {len(chunks)} chunks")
            
            # Extraer texto y metadatos
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
            
            # Generar embeddings
            self.logger.info("Generando embeddings...")
            embeddings = self.model.encode(texts, show_progress_bar=True)
            self.logger.info(f"Embeddings generados: {embeddings.shape}")
            
            # Crear índice FAISS
            self.logger.info("Creando índice FAISS...")
            dimension = embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dimension)
            self.index.add(embeddings.astype('float32'))
            
            # Guardar documentos y metadatos
            self.documents = texts
            self.metadata = metadata_list
            
            # Persistir índice
            self._save_index()
            
            self.logger.info(f"Indexados {len(chunks)} chunks en FAISS")
            return True
            
        except Exception as e:
            self.logger.error(f"Error indexando documentos: {e}")
            return False
    
    def _save_index(self):
        """Guarda el índice FAISS y metadatos"""
        try:
            # Guardar índice FAISS
            index_path = self.index_directory / "index.faiss"
            faiss.write_index(self.index, str(index_path))
            
            # Guardar documentos
            docs_path = self.index_directory / "documents.pkl"
            with open(docs_path, 'wb') as f:
                pickle.dump(self.documents, f)
            
            # Guardar metadatos
            metadata_path = self.index_directory / "metadata.pkl"
            with open(metadata_path, 'wb') as f:
                pickle.dump(self.metadata, f)
            
            self.logger.info("Índice FAISS guardado correctamente")
            
        except Exception as e:
            self.logger.error(f"Error guardando índice: {e}")
    
    def search_relevant_content(self, 
                              query: str, 
                              k: int = 3,
                              category: str = None) -> List[Dict[str, Any]]:
        """
        Busca contenido relevante para una consulta
        
        Args:
            query: Consulta del usuario
            k: Número de resultados a devolver
            category: Categoría de salud mental (opcional)
            
        Returns:
            Lista de documentos relevantes con metadatos
        """
        if not self.index or not self.documents:
            self.logger.error("Índice FAISS no disponible")
            return []
        
        try:
            # Cargar modelo si no está cargado
            self._load_embeddings_model()
            
            # Mejorar la query con contexto de categoría
            enhanced_query = query
            if category and category != "General":
                enhanced_query = f"{category}: {query}"
            
            # Generar embedding de la consulta
            query_embedding = self.model.encode([enhanced_query])
            
            # Buscar en FAISS
            distances, indices = self.index.search(query_embedding.astype('float32'), k)
            
            # Formatear resultados
            formatted_results = []
            for distance, idx in zip(distances[0], indices[0]):
                if idx < len(self.documents):  # Verificar índice válido
                    formatted_results.append({
                        'content': self.documents[idx],
                        'metadata': self.metadata[idx],
                        'relevance_score': float(distance),
                        'source': self.metadata[idx].get('source_file', 'unknown')
                    })
            
            self.logger.info(f"Encontrados {len(formatted_results)} documentos relevantes")
            return formatted_results
            
        except Exception as e:
            self.logger.error(f"Error en búsqueda: {e}")
            return []
    
    def get_context_for_query(self, 
                            query: str, 
                            category: str = "General",
                            max_context_length: int = 2000) -> str:
        """
        Obtiene contexto relevante para una consulta
        
        Args:
            query: Consulta del usuario
            category: Categoría de salud mental
            max_context_length: Longitud máxima del contexto
            
        Returns:
            Contexto relevante como string
        """
        # Buscar contenido relevante
        relevant_docs = self.search_relevant_content(query, k=3, category=category)
        
        if not relevant_docs:
            return ""
        
        # Construir contexto
        context_parts = []
        current_length = 0
        
        for doc in relevant_docs:
            content = doc['content'].strip()
            
            # Verificar si añadir este contenido excedería el límite
            if current_length + len(content) > max_context_length:
                # Truncar el contenido si es necesario
                remaining_space = max_context_length - current_length
                if remaining_space > 100:  # Solo añadir si queda espacio significativo
                    content = content[:remaining_space] + "..."
                    context_parts.append(content)
                break
            
            context_parts.append(content)
            current_length += len(content)
        
        # Unir todas las partes del contexto
        context = "\n\n---\n\n".join(context_parts)
        
        if context:
            return f"Información relevante de la base de conocimiento:\n\n{context}"
        
        return ""
    
    def add_document_from_text(self, 
                             text: str, 
                             metadata: Dict[str, Any] = None) -> bool:
        """
        Añade un documento desde texto directamente
        
        Args:
            text: Contenido del documento
            metadata: Metadatos del documento
            
        Returns:
            True si se añadió correctamente
        """
        try:
            # Crear documento
            doc = Document(
                page_content=text,
                metadata=metadata or {}
            )
            
            # Dividir en chunks
            chunks = self.text_splitter.split_documents([doc])
            
            if not chunks:
                return False
            
            # Cargar modelo si no está cargado
            self._load_embeddings_model()
            
            # Generar embeddings para los nuevos chunks
            new_texts = [chunk.page_content for chunk in chunks]
            new_embeddings = self.model.encode(new_texts)
            
            # Añadir al índice existente
            if self.index is None:
                # Crear nuevo índice si no existe
                dimension = new_embeddings.shape[1]
                self.index = faiss.IndexFlatL2(dimension)
                self.documents = []
                self.metadata = []
            
            # Añadir embeddings al índice
            self.index.add(new_embeddings.astype('float32'))
            
            # Añadir textos y metadatos
            for i, chunk in enumerate(chunks):
                self.documents.append(chunk.page_content)
                chunk_metadata = chunk.metadata.copy()
                chunk_metadata.update({
                    'chunk_id': len(self.documents) - 1,
                    'chunk_size': len(chunk.page_content)
                })
                self.metadata.append(chunk_metadata)
            
            # Guardar índice actualizado
            self._save_index()
            
            self.logger.info(f"Documento añadido: {len(chunks)} chunks")
            return True
            
        except Exception as e:
            self.logger.error(f"Error añadiendo documento: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas del índice FAISS
        
        Returns:
            Diccionario con estadísticas
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
            return {"error": f"Error obteniendo estadísticas: {e}"}


# Funciones de utilidad para integración fácil
def initialize_rag_manager(**kwargs) -> Optional[RAGManager]:
    """
    Inicializa el gestor RAG con configuración por defecto
    
    Returns:
        Instancia de RAGManager o None si hay error
    """
    try:
        return RAGManager(**kwargs)
    except Exception as e:
        logging.error(f"Error inicializando RAG: {e}")
        return None