"""
RAG (Retrieval-Augmented Generation) service.
Combines document retrieval with LLM generation.

Now uses Advanced RAG pipeline with:
- Query routing (skip RAG for greetings)
- Query rewriting (improve queries for better retrieval)
- Hybrid search (semantic + keyword/BM25)
- Re-ranking (cross-encoder scoring)
"""

from typing import List, Optional, Dict, Any, AsyncGenerator
from app.config import get_settings
from app.utils.logger import logger
from app.services.chroma_client import get_chroma_service
from app.services.ollama_client import get_ollama_client
from app.services.document_loader import get_document_loader
from app.services.advanced_rag import get_advanced_rag


class RAGService:
    """Service for RAG-based question answering with Advanced RAG pipeline."""

    def __init__(self, use_advanced_rag: bool = True):
        """
        Initialize RAG service.

        Args:
            use_advanced_rag: Whether to use the advanced RAG pipeline
        """
        self.settings = get_settings()
        self.chroma = get_chroma_service()
        self.ollama = get_ollama_client()
        self.document_loader = get_document_loader()
        self.use_advanced_rag = use_advanced_rag

        # Advanced RAG pipeline (lazy loaded)
        self._advanced_rag = None

    @property
    def advanced_rag(self):
        """Lazy load advanced RAG pipeline."""
        if self._advanced_rag is None and self.use_advanced_rag:
            self._advanced_rag = get_advanced_rag()
        return self._advanced_rag

    def _expand_query(self, query: str) -> str:
        """
        Expand query with related terms for better retrieval.
        This helps find relevant documents even with vague queries.
        """
        query_lower = query.lower()

        # Query expansion mappings for portfolio context
        expansions = {
            "skills": "skills technologies programming languages frameworks tools",
            "experience": "experience work job company employment career",
            "projects": "projects portfolio work applications apps built created",
            "education": "education degree university school training certification",
            "contact": "contact email phone location address",
            "about": "about bio background summary profile",
            "ahmed": "Ahmed Oublihi developer engineer",
        }

        expanded = query
        for term, expansion in expansions.items():
            if term in query_lower:
                expanded = f"{query} {expansion}"
                break

        return expanded

    def retrieve_context(
        self, query: str, top_k: Optional[int] = None
    ) -> tuple[str, List[str]]:
        """
        Retrieve relevant context for a query (basic retrieval).

        Args:
            query: The user's question
            top_k: Number of chunks to retrieve

        Returns:
            Tuple of (formatted_context, source_filenames)
        """
        # Use more chunks by default for better coverage
        k = top_k or max(self.settings.top_k_results, 5)

        # Expand query for better retrieval
        expanded_query = self._expand_query(query)
        logger.debug(f"Original query: {query}")
        logger.debug(f"Expanded query: {expanded_query}")

        results = self.chroma.query(expanded_query, n_results=k)

        documents = results.get("documents", [])
        metadatas = results.get("metadatas", [])

        if not documents:
            logger.debug("No relevant documents found in RAG")
            return "", []

        # Format context with relevance-based ordering
        context_parts = []
        sources = set()

        for doc, meta in zip(documents, metadatas):
            filename = meta.get("filename", "Unknown")
            sources.add(filename)

            # Include chunk info for better context
            chunk_info = f"[Source: {filename}]"
            if meta.get("chunk_index") is not None:
                chunk_info = (
                    f"[Source: {filename}, Part {meta.get('chunk_index', 0) + 1}]"
                )

            context_parts.append(f"{chunk_info}\n{doc}")

        # Join with clear separators
        context = "\n\n---\n\n".join(context_parts)
        logger.info(
            f"RAG retrieved {len(documents)} chunks from {len(sources)} sources"
        )

        return context, list(sources)

    async def query(
        self, question: str, history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Answer a question using RAG.

        Uses Advanced RAG pipeline if enabled:
        - Query routing to skip RAG for greetings/chitchat
        - Query rewriting for better retrieval
        - Hybrid search (semantic + keyword)
        - Re-ranking for better relevance

        Args:
            question: User's question
            history: Previous conversation history

        Returns:
            Dict with response and sources
        """
        # Use advanced RAG pipeline if enabled
        if self.use_advanced_rag and self.advanced_rag:
            logger.info("Using Advanced RAG pipeline")
            return await self.advanced_rag.query(question, history)

        # Fallback to basic RAG
        context, sources = self.retrieve_context(question)

        response = await self.ollama.generate(
            query=question, context=context, history=history
        )

        return {
            "response": response,
            "sources": sources,
        }

    async def query_stream(
        self, question: str, history: Optional[List[Dict[str, str]]] = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Answer a question using RAG with streaming response.

        Uses Advanced RAG pipeline if enabled.

        Args:
            question: User's question
            history: Previous conversation history

        Yields:
            Dicts with response chunks and metadata
        """
        # Use advanced RAG pipeline if enabled
        if self.use_advanced_rag and self.advanced_rag:
            logger.info("Using Advanced RAG pipeline (streaming)")
            async for chunk in self.advanced_rag.query_stream(question, history):
                yield chunk
            return

        # Fallback to basic RAG
        context, sources = self.retrieve_context(question)

        async for chunk in self.ollama.generate_stream(
            query=question, context=context, history=history
        ):
            yield {
                "chunk": chunk,
                "done": False,
                "sources": None,
            }

        yield {
            "chunk": "",
            "done": True,
            "sources": sources,
        }

    async def ingest_document(self, filename: str, content: bytes) -> Dict[str, Any]:
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
        ids = self.chroma.add_documents(texts=chunks, metadatas=chunk_metadatas)

        if not ids:
            return {
                "success": False,
                "error": "Failed to add document to vector database",
            }

        logger.info(f"Ingested document: {filename} ({len(chunks)} chunks)")

        # Refresh hybrid search index for advanced RAG
        if self.use_advanced_rag and self.advanced_rag:
            self.advanced_rag.refresh_index()

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
            # Refresh hybrid search index for advanced RAG
            # Wrap in try-except to prevent 500 error if refresh fails
            # (deletion already succeeded at this point)
            if self.use_advanced_rag and self.advanced_rag:
                try:
                    self.advanced_rag.refresh_index()
                except Exception as e:
                    logger.warning(f"Failed to refresh index after deletion: {e}")

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
