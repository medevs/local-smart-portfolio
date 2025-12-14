"""
ChromaDB client for vector storage and retrieval.
Handles document storage, querying, and management.
"""

import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Optional, Dict, Any
import uuid
from app.config import get_settings
from app.utils.logger import logger
from app.services.embeddings import get_embedding_service


class ChromaService:
    """Service for interacting with ChromaDB."""
    
    def __init__(self):
        settings = get_settings()
        self.persist_dir = settings.chroma_persist_dir
        self.collection_name = settings.chroma_collection_name
        self._client: Optional[chromadb.PersistentClient] = None
        self._collection = None
        self.embedding_service = get_embedding_service()
        
    @property
    def client(self) -> chromadb.PersistentClient:
        """Lazy load the ChromaDB client."""
        if self._client is None:
            logger.info(f"Initializing ChromaDB at: {self.persist_dir}")
            self._client = chromadb.PersistentClient(
                path=self.persist_dir,
                settings=ChromaSettings(
                    anonymized_telemetry=False,
                    allow_reset=True,
                )
            )
            logger.info("ChromaDB client initialized")
        return self._client
    
    @property
    def collection(self):
        """Get or create the document collection."""
        if self._collection is None:
            self._collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"description": "Portfolio document embeddings"}
            )
            logger.info(f"Using collection: {self.collection_name}")
            # Check for embedding dimension mismatch on first access
            self._validate_embedding_dimension()
        return self._collection

    def _validate_embedding_dimension(self) -> None:
        """
        Validate that stored embeddings match current model's dimension.
        Auto-resets collection if there's a mismatch to prevent errors.
        """
        try:
            # Get expected dimension from embedding service
            expected_dim = self.embedding_service.get_embedding_dimension()

            # Check if collection has any documents
            if self._collection.count() == 0:
                logger.info(f"Empty collection, will use {expected_dim}-dim embeddings")
                return

            # Sample one document to check stored dimension
            sample = self._collection.get(limit=1, include=["embeddings"])
            if not sample or not sample.get("embeddings") or not sample["embeddings"][0]:
                return

            stored_dim = len(sample["embeddings"][0])

            if stored_dim != expected_dim:
                logger.warning(
                    f"Embedding dimension mismatch detected! "
                    f"Stored: {stored_dim}, Expected: {expected_dim}. "
                    f"Auto-resetting collection..."
                )
                # Reset collection to fix dimension mismatch
                self.client.delete_collection(self.collection_name)
                self._collection = self.client.get_or_create_collection(
                    name=self.collection_name,
                    metadata={"description": "Portfolio document embeddings"}
                )
                logger.info(
                    f"Collection reset complete. "
                    f"Please re-ingest documents with {expected_dim}-dim embeddings."
                )
            else:
                logger.info(f"Embedding dimension OK: {stored_dim}")

        except Exception as e:
            logger.error(f"Error validating embedding dimension: {e}")
    
    def check_connection(self) -> bool:
        """Check if ChromaDB is accessible."""
        try:
            _ = self.client.heartbeat()
            return True
        except Exception as e:
            logger.error(f"ChromaDB connection check failed: {e}")
            return False
    
    def add_documents(
        self,
        texts: List[str],
        metadatas: List[Dict[str, Any]],
        ids: Optional[List[str]] = None
    ) -> List[str]:
        """
        Add documents to the collection.
        Validates metadata against rag.txt requirements:
        - chunk_id
        - document_id
        - source
        - position
        
        Args:
            texts: List of text content
            metadatas: List of metadata dicts
            ids: Optional list of IDs (generated if not provided)
            
        Returns:
            List of document IDs
        """
        if not texts:
            logger.warning("No texts provided to add")
            return []
            
        # Validate metadata fields
        required_fields = {"chunk_id", "document_id", "source", "position"}
        for idx, meta in enumerate(metadatas):
            missing = required_fields - meta.keys()
            if missing:
                logger.error(f"Metadata at index {idx} missing required fields: {missing}")
                raise ValueError(f"Metadata missing required fields: {missing}")
        
        # Generate IDs if not provided
        if ids is None:
            ids = [meta.get("chunk_id", f"chunk_{uuid.uuid4().hex[:12]}") for meta in metadatas]
        
        # Generate embeddings
        embeddings = self.embedding_service.embed_texts(texts)
        
        if not embeddings or len(embeddings) != len(texts):
            logger.error("Failed to generate embeddings for all texts")
            return []
        
        try:
            self.collection.add(
                documents=texts,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )
            logger.info(f"Added {len(texts)} documents to collection")
            return ids
        except Exception as e:
            logger.error(f"Error adding documents to ChromaDB: {e}")
            return []
    
    def query(
        self,
        query_text: Optional[str] = None,
        query_texts: Optional[List[str]] = None,
        n_results: int = 3,
        where: Optional[Dict[str, Any]] = None,
        include: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Query the collection for similar documents.
        
        Args:
            query_text: Single text to search for (legacy support)
            query_texts: List of texts to search for (preferred)
            n_results: Number of results to return
            where: Optional filter conditions
            include: Optional list of fields to include
            
        Returns:
            Dict with documents, metadatas, and distances
        """
        # Support both query_text and query_texts
        texts = query_texts if query_texts else ([query_text] if query_text else [])
        
        if not texts or all(not t or not t.strip() for t in texts):
            return {"documents": [], "metadatas": [], "distances": [], "ids": []}
        
        # Generate query embeddings
        query_embeddings = self.embedding_service.embed_texts(texts)
        
        if not query_embeddings:
            logger.error("Failed to generate query embeddings")
            return {"documents": [], "metadatas": [], "distances": [], "ids": []}
        
        default_include = ["documents", "metadatas", "distances"]
        
        try:
            results = self.collection.query(
                query_embeddings=query_embeddings,
                n_results=n_results,
                where=where,
                include=include if include else default_include
            )
            
            # Return raw results structure which contains lists of lists
            # The caller handles flattening if needed
            return results
        except Exception as e:
            logger.error(f"Error querying ChromaDB: {e}")
            return {"documents": [], "metadatas": [], "distances": [], "ids": []}
    
    def delete_by_document_id(self, document_id: str) -> bool:
        """
        Delete all chunks belonging to a document.
        
        Args:
            document_id: The document ID to delete
            
        Returns:
            True if successful
        """
        try:
            # Get all chunks with this document_id
            results = self.collection.get(
                where={"document_id": document_id},
                include=["metadatas"]
            )
            
            if results and results.get("ids"):
                self.collection.delete(ids=results["ids"])
                logger.info(f"Deleted {len(results['ids'])} chunks for document: {document_id}")
                return True
            else:
                logger.warning(f"No chunks found for document: {document_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error deleting document: {e}")
            return False
    
    def get_all_documents(self) -> List[Dict[str, Any]]:
        """
        Get metadata for all unique documents.
        
        Returns:
            List of unique document metadata
        """
        try:
            results = self.collection.get(include=["metadatas"])
            
            if not results or not results.get("metadatas"):
                return []
            
            # Extract unique documents by document_id
            documents = {}
            for metadata in results["metadatas"]:
                doc_id = metadata.get("document_id")
                if doc_id and doc_id not in documents:
                    # Use 'source' field (set during ingestion) as filename
                    source = metadata.get("source", "Unknown")
                    documents[doc_id] = {
                        "id": doc_id,
                        "filename": source,
                        "source": source,
                        "file_type": metadata.get("file_type", "Unknown"),
                        "file_size": metadata.get("file_size", 0),
                        "chunk_count": 0,
                        "uploaded_at": metadata.get("uploaded_at", ""),
                    }
                if doc_id:
                    documents[doc_id]["chunk_count"] += 1
            
            return list(documents.values())
            
        except Exception as e:
            logger.error(f"Error getting documents: {e}")
            return []
    
    def get_stats(self) -> Dict[str, Any]:
        """Get collection statistics."""
        try:
            count = self.collection.count()
            documents = self.get_all_documents()
            
            return {
                "total_chunks": count,
                "total_documents": len(documents),
                "collection_name": self.collection_name,
            }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {
                "total_chunks": 0,
                "total_documents": 0,
                "collection_name": self.collection_name,
            }
    
    def reset_collection(self) -> bool:
        """Reset (delete and recreate) the collection."""
        try:
            self.client.delete_collection(self.collection_name)
            self._collection = None
            _ = self.collection  # Recreate
            logger.info("Collection reset successfully")
            return True
        except Exception as e:
            logger.error(f"Error resetting collection: {e}")
            return False


# Singleton instance
_chroma_service: Optional[ChromaService] = None


def get_chroma_service() -> ChromaService:
    """Get or create the ChromaDB service singleton."""
    global _chroma_service
    if _chroma_service is None:
        _chroma_service = ChromaService()
    return _chroma_service

def get_chroma_client() -> ChromaService:
    """Legacy alias for get_chroma_service."""
    return get_chroma_service()
