"""
RAG (Retrieval-Augmented Generation) service.
Combines document retrieval with LLM generation.
"""

from typing import List, Optional, Dict, Any, AsyncGenerator
from app.config import get_settings
from app.utils.logger import logger
from app.services.chroma_client import get_chroma_service
from app.services.ollama_client import get_ollama_client
from app.services.document_loader import get_document_loader


class RAGService:
    """Service for RAG-based question answering."""
    
    def __init__(self):
        self.settings = get_settings()
        self.chroma = get_chroma_service()
        self.ollama = get_ollama_client()
        self.document_loader = get_document_loader()
    
    def retrieve_context(
        self,
        query: str,
        top_k: Optional[int] = None
    ) -> tuple[str, List[str]]:
        """
        Retrieve relevant context for a query.
        
        Args:
            query: The user's question
            top_k: Number of chunks to retrieve
            
        Returns:
            Tuple of (formatted_context, source_filenames)
        """
        k = top_k or self.settings.top_k_results
        
        results = self.chroma.query(query, n_results=k)
        
        documents = results.get("documents", [])
        metadatas = results.get("metadatas", [])
        
        if not documents:
            logger.debug("No relevant documents found")
            return "", []
        
        # Format context
        context_parts = []
        sources = set()
        
        for i, (doc, meta) in enumerate(zip(documents, metadatas)):
            filename = meta.get("filename", "Unknown")
            sources.add(filename)
            context_parts.append(f"[Source: {filename}]\n{doc}")
        
        context = "\n\n---\n\n".join(context_parts)
        logger.debug(f"Retrieved {len(documents)} chunks from {len(sources)} sources")
        
        return context, list(sources)
    
    async def query(
        self,
        question: str,
        history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Answer a question using RAG.
        
        Args:
            question: User's question
            history: Previous conversation history
            
        Returns:
            Dict with response and sources
        """
        # Retrieve relevant context
        context, sources = self.retrieve_context(question)
        
        # Generate response
        response = await self.ollama.generate(
            query=question,
            context=context,
            history=history
        )
        
        return {
            "response": response,
            "sources": sources,
        }
    
    async def query_stream(
        self,
        question: str,
        history: Optional[List[Dict[str, str]]] = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Answer a question using RAG with streaming response.
        
        Args:
            question: User's question
            history: Previous conversation history
            
        Yields:
            Dicts with response chunks and metadata
        """
        # Retrieve relevant context
        context, sources = self.retrieve_context(question)
        
        # Stream response
        async for chunk in self.ollama.generate_stream(
            query=question,
            context=context,
            history=history
        ):
            yield {
                "chunk": chunk,
                "done": False,
                "sources": None,
            }
        
        # Final message with sources
        yield {
            "chunk": "",
            "done": True,
            "sources": sources,
        }
    
    async def ingest_document(
        self,
        filename: str,
        content: bytes
    ) -> Dict[str, Any]:
        """
        Ingest a document into the knowledge base.
        
        Args:
            filename: Original filename
            content: File content as bytes
            
        Returns:
            Dict with ingestion results
        """
        # Process the file
        result = await self.document_loader.process_file(filename, content)
        
        if not result.get("success"):
            return result
        
        # Add to vector database
        chunks = result["chunks"]
        metadata = result["metadata"]
        
        # Create metadata for each chunk
        chunk_metadatas = [
            {
                **metadata,
                "chunk_index": i,
                "total_chunks": len(chunks),
            }
            for i in range(len(chunks))
        ]
        
        # Add to ChromaDB
        ids = self.chroma.add_documents(
            texts=chunks,
            metadatas=chunk_metadatas
        )
        
        if not ids:
            return {
                "success": False,
                "error": "Failed to add document to vector database"
            }
        
        logger.info(f"Ingested document: {filename} ({len(chunks)} chunks)")
        
        return {
            "success": True,
            "document_id": result["document_id"],
            "filename": filename,
            "file_type": result["file_type"],
            "file_size": result["file_size"],
            "chunk_count": len(chunks),
        }
    
    def delete_document(self, document_id: str) -> Dict[str, Any]:
        """
        Delete a document from the knowledge base.
        
        Args:
            document_id: The document ID to delete
            
        Returns:
            Dict with deletion status
        """
        # Delete from vector database
        db_deleted = self.chroma.delete_by_document_id(document_id)
        
        # Delete file from disk
        file_deleted = self.document_loader.delete_file(document_id)
        
        if db_deleted or file_deleted:
            return {
                "success": True,
                "message": f"Document {document_id} deleted",
                "deleted_id": document_id,
            }
        else:
            return {
                "success": False,
                "message": f"Document {document_id} not found",
            }
    
    def get_documents(self) -> List[Dict[str, Any]]:
        """Get list of all documents in the knowledge base."""
        return self.chroma.get_all_documents()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get knowledge base statistics."""
        stats = self.chroma.get_stats()
        stats["embedding_model"] = self.settings.embedding_model
        return stats


# Singleton instance
_rag_service: Optional[RAGService] = None


def get_rag_service() -> RAGService:
    """Get or create the RAG service singleton."""
    global _rag_service
    if _rag_service is None:
        _rag_service = RAGService()
    return _rag_service

