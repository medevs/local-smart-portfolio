from typing import List, Tuple
from app.utils.logger import logger

class Reranker:
    """
    Reranker for re-ranking retrieved documents.
    Uses simple scoring or falls back to no-op if ML libs are missing.
    """

    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model = None
        self.use_cross_encoder = False
        
        try:
            from sentence_transformers import CrossEncoder
            self.model = CrossEncoder(model_name)
            self.use_cross_encoder = True
            logger.info(f"Initialized CrossEncoder with model: {model_name}")
        except ImportError:
            logger.warning("sentence-transformers not found. Falling back to simple re-ranking (or no-op).")

    def rerank(
        self,
        query: str,
        documents: List[str],
        top_k: int = 3
    ) -> List[Tuple[str, float]]:
        """
        Re-rank documents.
        """
        if not documents:
            return []

        if self.use_cross_encoder and self.model:
            try:
                # Create query-document pairs
                pairs = [[query, doc] for doc in documents]
                # Score pairs
                scores = self.model.predict(pairs)
                # Sort by score
                doc_scores = list(zip(documents, scores))
                doc_scores.sort(key=lambda x: x[1], reverse=True)
                return doc_scores[:top_k]
            except Exception as e:
                logger.error(f"Error during cross-encoder reranking: {e}")
                # Fallthrough to basic return

        # Fallback: Return documents as-is with dummy scores (preserving original order)
        # Assuming original retrieval order implies some relevance
        logger.info("Returning documents without advanced reranking")
        return [(doc, 1.0 - (i * 0.01)) for i, doc in enumerate(documents[:top_k])]


# Singleton instance
_reranker = None


def get_reranker(use_lightweight: bool = True) -> Reranker:
    """Get or create the Reranker singleton."""
    global _reranker
    if _reranker is None:
        _reranker = Reranker()
    return _reranker
