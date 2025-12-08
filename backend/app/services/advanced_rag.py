"""
Advanced RAG Pipeline for production-ready retrieval.

Pipeline: Query -> Route -> Rewrite -> Hybrid Search -> Re-rank -> Generate

This implements the "Advanced RAG" pattern with:
1. Query routing - decide if RAG is needed
2. Query rewriting - improve query for better retrieval
3. Hybrid search - combine semantic + keyword search
4. Re-ranking - use cross-encoder to re-score results
"""

from typing import List, Dict, Any, Optional, AsyncGenerator
from dataclasses import dataclass
from app.utils.logger import logger
from app.config import get_settings
from app.services.query_router import get_query_router, QueryType
from app.services.query_rewriter import get_query_rewriter
from app.services.hybrid_search import get_hybrid_search
from app.services.reranker import get_reranker
from app.services.ollama_client import get_ollama_client


@dataclass
class RetrievalResult:
    """Result from the retrieval pipeline."""
    context: str
    sources: List[str]
    query_type: QueryType
    rewritten_query: str
    num_results: int
    used_rag: bool


class AdvancedRAGPipeline:
    """
    Advanced RAG pipeline with query routing, rewriting, hybrid search, and re-ranking.
    """

    def __init__(
        self,
        use_reranker: bool = True,
        use_lightweight_reranker: bool = True,  # Use heuristic reranker by default
        top_k: int = 5,
        rerank_top_k: int = 3,
    ):
        """
        Initialize the advanced RAG pipeline.

        Args:
            use_reranker: Whether to use re-ranking
            use_lightweight_reranker: Use heuristic vs ML reranker
            top_k: Number of results from hybrid search
            rerank_top_k: Number of results after re-ranking
        """
        self.settings = get_settings()
        self.router = get_query_router()
        self.rewriter = get_query_rewriter()
        self.hybrid_search = get_hybrid_search()
        self.reranker = get_reranker(use_lightweight=use_lightweight_reranker)
        self.ollama = get_ollama_client()

        self.use_reranker = use_reranker
        self.top_k = top_k
        self.rerank_top_k = rerank_top_k

    async def retrieve(
        self,
        query: str,
        history: Optional[List[Dict]] = None,
        force_rag: bool = False,
    ) -> RetrievalResult:
        """
        Execute the full retrieval pipeline.

        Args:
            query: User's question
            history: Conversation history
            force_rag: Force RAG even if router says not needed

        Returns:
            RetrievalResult with context and metadata
        """
        # Step 1: Route the query
        query_type, needs_rag = self.router.route(query, history)
        logger.info(f"Query routed as: {query_type.value}, needs_rag: {needs_rag}")

        # Skip RAG for greetings/chitchat unless forced
        if not needs_rag and not force_rag:
            return RetrievalResult(
                context="",
                sources=[],
                query_type=query_type,
                rewritten_query=query,
                num_results=0,
                used_rag=False,
            )

        # Step 2: Rewrite the query for better retrieval
        rewritten_query = await self.rewriter.rewrite_query(query, history)
        logger.info(f"Query rewritten: '{query}' -> '{rewritten_query}'")

        # Step 3: Hybrid search (semantic + keyword)
        search_results = self.hybrid_search.search(
            rewritten_query,
            top_k=self.top_k,
            use_bm25=True,
            use_semantic=True,
        )

        if not search_results:
            logger.info("No results from hybrid search")
            return RetrievalResult(
                context="",
                sources=[],
                query_type=query_type,
                rewritten_query=rewritten_query,
                num_results=0,
                used_rag=True,
            )

        # Step 4: Re-rank results
        if self.use_reranker and len(search_results) > 1:
            search_results = self.reranker.rerank(
                query,  # Use original query for re-ranking
                search_results,
                top_k=self.rerank_top_k,
            )
            logger.info(f"Re-ranked to top {len(search_results)} results")

        # Step 5: Format context
        context, sources = self._format_context(search_results)

        return RetrievalResult(
            context=context,
            sources=sources,
            query_type=query_type,
            rewritten_query=rewritten_query,
            num_results=len(search_results),
            used_rag=True,
        )

    def _format_context(
        self,
        results: List[Dict[str, Any]]
    ) -> tuple[str, List[str]]:
        """Format search results into context string."""
        context_parts = []
        sources = set()

        for i, result in enumerate(results):
            doc = result.get("document", "")
            meta = result.get("metadata", {})
            score = result.get("rerank_score", result.get("score", 0))

            filename = meta.get("filename", "Unknown")
            sources.add(filename)

            # Include relevance indicator
            relevance = "High" if score > 0.7 else "Medium" if score > 0.4 else "Low"

            chunk_info = f"[Source: {filename}]"
            if meta.get("chunk_index") is not None:
                chunk_info = f"[Source: {filename}, Part {meta.get('chunk_index', 0) + 1}]"

            context_parts.append(f"{chunk_info}\n{doc}")

        context = "\n\n---\n\n".join(context_parts)
        return context, list(sources)

    async def query(
        self,
        question: str,
        history: Optional[List[Dict]] = None,
    ) -> Dict[str, Any]:
        """
        Full RAG query: retrieve context and generate response.

        Args:
            question: User's question
            history: Conversation history

        Returns:
            Dict with response, sources, and metadata
        """
        # Retrieve context
        retrieval = await self.retrieve(question, history)

        # Generate response
        response = await self.ollama.generate(
            query=question,
            context=retrieval.context,
            history=history,
        )

        return {
            "response": response,
            "sources": retrieval.sources,
            "query_type": retrieval.query_type.value,
            "rewritten_query": retrieval.rewritten_query,
            "used_rag": retrieval.used_rag,
            "num_results": retrieval.num_results,
        }

    async def query_stream(
        self,
        question: str,
        history: Optional[List[Dict]] = None,
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Full RAG query with streaming response.

        Args:
            question: User's question
            history: Conversation history

        Yields:
            Dicts with response chunks and metadata
        """
        # Retrieve context
        retrieval = await self.retrieve(question, history)

        # Stream response
        async for chunk in self.ollama.generate_stream(
            query=question,
            context=retrieval.context,
            history=history,
        ):
            yield {
                "chunk": chunk,
                "done": False,
                "sources": None,
            }

        # Final message with metadata
        yield {
            "chunk": "",
            "done": True,
            "sources": retrieval.sources,
            "query_type": retrieval.query_type.value,
            "used_rag": retrieval.used_rag,
            "num_results": retrieval.num_results,
        }

    def refresh_index(self) -> None:
        """Refresh the hybrid search index (call after document changes)."""
        self.hybrid_search.refresh_index()
        logger.info("Advanced RAG index refreshed")


# Singleton instance
_advanced_rag: Optional[AdvancedRAGPipeline] = None


def get_advanced_rag() -> AdvancedRAGPipeline:
    """Get or create the advanced RAG pipeline singleton."""
    global _advanced_rag
    if _advanced_rag is None:
        _advanced_rag = AdvancedRAGPipeline()
    return _advanced_rag
