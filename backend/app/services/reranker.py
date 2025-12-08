"""
Re-ranker Service for Advanced RAG.
Uses cross-encoder to re-score retrieved documents for better relevance.
"""

from typing import List, Dict, Any, Optional
from sentence_transformers import CrossEncoder
from app.utils.logger import logger
from app.config import get_settings


class Reranker:
    """
    Re-ranks retrieved documents using a cross-encoder model.

    Cross-encoders are more accurate than bi-encoders (used for initial retrieval)
    because they process query and document together, capturing interactions.

    Trade-off: More accurate but slower, so used after initial retrieval.
    """

    # Available cross-encoder models (from smallest to largest)
    MODELS = {
        "tiny": "cross-encoder/ms-marco-TinyBERT-L-2-v2",      # ~17MB, fastest
        "mini": "cross-encoder/ms-marco-MiniLM-L-6-v2",        # ~80MB, balanced
        "small": "cross-encoder/ms-marco-MiniLM-L-12-v2",      # ~120MB, better
        "base": "cross-encoder/ms-marco-electra-base",         # ~400MB, best
    }

    def __init__(self, model_size: str = "mini"):
        """
        Initialize re-ranker with specified model size.

        Args:
            model_size: One of 'tiny', 'mini', 'small', 'base'
        """
        self.settings = get_settings()
        self.model_name = self.MODELS.get(model_size, self.MODELS["mini"])
        self._model: Optional[CrossEncoder] = None
        self._model_loaded = False

    def _load_model(self) -> None:
        """Lazy load the cross-encoder model."""
        if self._model_loaded:
            return

        try:
            logger.info(f"Loading cross-encoder model: {self.model_name}")
            self._model = CrossEncoder(self.model_name, max_length=512)
            self._model_loaded = True
            logger.info("Cross-encoder model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load cross-encoder model: {e}")
            self._model = None
            self._model_loaded = True  # Don't retry on every call

    def rerank(
        self,
        query: str,
        documents: List[Dict[str, Any]],
        top_k: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Re-rank documents by relevance to the query.

        Args:
            query: The search query
            documents: List of documents with 'document' key containing text
            top_k: Number of top results to return (None = all)

        Returns:
            Re-ranked list of documents with added 'rerank_score'
        """
        if not documents:
            return []

        # Ensure model is loaded
        self._load_model()

        # If model failed to load, return original order
        if self._model is None:
            logger.warning("Cross-encoder not available, returning original order")
            return documents[:top_k] if top_k else documents

        try:
            # Prepare query-document pairs
            pairs = [
                [query, doc.get("document", "")]
                for doc in documents
            ]

            # Get cross-encoder scores
            scores = self._model.predict(pairs)

            # Add scores to documents
            for doc, score in zip(documents, scores):
                doc["rerank_score"] = float(score)

            # Sort by rerank score (descending)
            reranked = sorted(
                documents,
                key=lambda x: x.get("rerank_score", 0),
                reverse=True
            )

            logger.debug(
                f"Re-ranked {len(documents)} documents, "
                f"top score: {reranked[0].get('rerank_score', 0):.3f}"
            )

            return reranked[:top_k] if top_k else reranked

        except Exception as e:
            logger.error(f"Re-ranking failed: {e}")
            return documents[:top_k] if top_k else documents

    def score_relevance(self, query: str, document: str) -> float:
        """
        Score the relevance of a single document to a query.

        Args:
            query: The search query
            document: Document text

        Returns:
            Relevance score (higher = more relevant)
        """
        self._load_model()

        if self._model is None:
            return 0.0

        try:
            score = self._model.predict([[query, document]])[0]
            return float(score)
        except Exception as e:
            logger.error(f"Relevance scoring failed: {e}")
            return 0.0

    def filter_relevant(
        self,
        query: str,
        documents: List[Dict[str, Any]],
        threshold: float = 0.0
    ) -> List[Dict[str, Any]]:
        """
        Filter documents that meet a relevance threshold.

        Args:
            query: The search query
            documents: List of documents
            threshold: Minimum rerank score to include

        Returns:
            Filtered list of relevant documents
        """
        reranked = self.rerank(query, documents)
        filtered = [
            doc for doc in reranked
            if doc.get("rerank_score", 0) >= threshold
        ]

        logger.debug(
            f"Filtered {len(documents)} -> {len(filtered)} documents "
            f"(threshold: {threshold})"
        )

        return filtered


class LightweightReranker:
    """
    Lightweight re-ranker using heuristics instead of ML model.
    Faster but less accurate. Good for resource-constrained environments.
    """

    def __init__(self):
        self.settings = get_settings()

    def rerank(
        self,
        query: str,
        documents: List[Dict[str, Any]],
        top_k: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Re-rank using keyword matching and position heuristics."""
        if not documents:
            return []

        query_terms = set(query.lower().split())

        for doc in documents:
            doc_text = doc.get("document", "").lower()

            # Score based on:
            # 1. Exact phrase match (highest)
            # 2. All query terms present
            # 3. Percentage of query terms found
            # 4. Term frequency

            score = 0.0

            # Exact phrase match bonus
            if query.lower() in doc_text:
                score += 2.0

            # Count matching terms
            found_terms = sum(1 for term in query_terms if term in doc_text)
            term_coverage = found_terms / len(query_terms) if query_terms else 0

            # All terms present bonus
            if term_coverage == 1.0:
                score += 1.0

            # Coverage score
            score += term_coverage * 0.5

            # Term frequency (capped to avoid bias to long docs)
            for term in query_terms:
                count = doc_text.count(term)
                score += min(count * 0.1, 0.3)

            # Add to existing score if present
            existing_score = doc.get("score", 0)
            doc["rerank_score"] = score + (existing_score * 0.3)

        # Sort by rerank score
        reranked = sorted(
            documents,
            key=lambda x: x.get("rerank_score", 0),
            reverse=True
        )

        return reranked[:top_k] if top_k else reranked


# Singleton instances
_reranker: Optional[Reranker] = None
_lightweight_reranker: Optional[LightweightReranker] = None


def get_reranker(use_lightweight: bool = False) -> Reranker | LightweightReranker:
    """
    Get or create the re-ranker singleton.

    Args:
        use_lightweight: Use heuristic-based reranker instead of ML model
    """
    global _reranker, _lightweight_reranker

    if use_lightweight:
        if _lightweight_reranker is None:
            _lightweight_reranker = LightweightReranker()
        return _lightweight_reranker
    else:
        if _reranker is None:
            _reranker = Reranker(model_size="mini")
        return _reranker
