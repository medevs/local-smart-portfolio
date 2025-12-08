"""
Re-ranker Service for Advanced RAG.
Uses lightweight heuristics or Ollama LLM for re-scoring retrieved documents.
No sentence-transformers dependency - production-ready and lightweight.
"""

from typing import List, Dict, Any, Optional
import re
import httpx
from app.utils.logger import logger
from app.config import get_settings


class LightweightReranker:
    """
    Lightweight re-ranker using heuristics instead of ML model.
    Fast, resource-efficient, and production-ready.
    """

    def __init__(self):
        self.settings = get_settings()
        # Common English stopwords for filtering
        self.stopwords = {
            'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been',
            'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'could', 'should', 'may', 'might', 'can', 'of', 'in',
            'to', 'for', 'on', 'with', 'at', 'by', 'from', 'as', 'into',
            'through', 'during', 'before', 'after', 'above', 'below',
            'between', 'under', 'again', 'further', 'then', 'once', 'here',
            'there', 'when', 'where', 'why', 'how', 'all', 'each', 'few',
            'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
            'only', 'own', 'same', 'so', 'than', 'too', 'very', 'just',
            'and', 'but', 'if', 'or', 'because', 'until', 'while', 'about',
            'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those',
            'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'you', 'your',
            'he', 'him', 'his', 'she', 'her', 'it', 'its', 'they', 'them'
        }

    def _tokenize(self, text: str) -> set:
        """Tokenize text and filter stopwords."""
        words = re.findall(r'\b\w+\b', text.lower())
        return {w for w in words if w not in self.stopwords and len(w) > 2}

    def _calculate_relevance_score(self, query: str, document: str) -> float:
        """
        Calculate relevance score based on multiple heuristics.
        Returns score between 0 and 1.
        """
        query_lower = query.lower()
        doc_lower = document.lower()
        query_tokens = self._tokenize(query)
        doc_tokens = self._tokenize(document)

        if not query_tokens:
            return 0.0

        score = 0.0

        # 1. Exact phrase match (strongest signal)
        if query_lower in doc_lower:
            score += 0.4

        # 2. Token overlap coverage
        overlap = query_tokens & doc_tokens
        coverage = len(overlap) / len(query_tokens)
        score += coverage * 0.3

        # 3. All query terms present bonus
        if coverage == 1.0:
            score += 0.15

        # 4. Multi-word phrase matches
        query_words = query_lower.split()
        for i in range(len(query_words) - 1):
            bigram = f"{query_words[i]} {query_words[i+1]}"
            if bigram in doc_lower:
                score += 0.05

        # 5. Term frequency (capped)
        for term in query_tokens:
            if term in doc_lower:
                count = doc_lower.count(term)
                score += min(count * 0.02, 0.1)

        return min(score, 1.0)

    def rerank(
        self,
        query: str,
        documents: List[Dict[str, Any]],
        top_k: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Re-rank documents by relevance to query using heuristics.

        Args:
            query: The search query
            documents: List of documents with 'document' key containing text
            top_k: Number of top results to return (None = all)

        Returns:
            Re-ranked list of documents with added 'rerank_score'
        """
        if not documents:
            return []

        for doc in documents:
            doc_text = doc.get("document", "")
            relevance = self._calculate_relevance_score(query, doc_text)

            # Combine with existing semantic/bm25 score if present
            existing_score = doc.get("score", 0)
            # Weight: 60% heuristic, 40% original score
            doc["rerank_score"] = (relevance * 0.6) + (existing_score * 0.4)

        # Sort by rerank score descending
        reranked = sorted(
            documents,
            key=lambda x: x.get("rerank_score", 0),
            reverse=True
        )

        logger.debug(
            f"Re-ranked {len(documents)} documents, "
            f"top score: {reranked[0].get('rerank_score', 0):.3f}" if reranked else ""
        )

        return reranked[:top_k] if top_k else reranked

    def filter_relevant(
        self,
        query: str,
        documents: List[Dict[str, Any]],
        threshold: float = 0.2
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


class OllamaReranker:
    """
    Re-ranker using Ollama LLM for relevance scoring.
    More accurate than heuristics but slower. Use for critical queries.
    """

    def __init__(self, model_name: Optional[str] = None):
        settings = get_settings()
        self.base_url = settings.ollama_base_url
        self.model_name = model_name or settings.ollama_model
        self._client: Optional[httpx.Client] = None

    @property
    def client(self) -> httpx.Client:
        """Lazy load HTTP client."""
        if self._client is None:
            self._client = httpx.Client(timeout=30.0)
        return self._client

    def _score_document(self, query: str, document: str) -> float:
        """
        Use LLM to score document relevance.
        Returns a score between 0 and 1.
        """
        # Truncate document to avoid token limits
        doc_preview = document[:800] if len(document) > 800 else document

        prompt = f"""Rate how relevant this document is to the query on a scale of 0-10.
Only respond with a single number, nothing else.

Query: {query}

Document: {doc_preview}

Relevance (0-10):"""

        try:
            response = self.client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0, "num_predict": 5}
                }
            )
            response.raise_for_status()
            result = response.json().get("response", "5").strip()

            # Parse score from response
            match = re.search(r'\d+\.?\d*', result)
            if match:
                score = float(match.group())
                return min(score / 10.0, 1.0)
            return 0.5

        except Exception as e:
            logger.warning(f"LLM reranking failed for document: {e}")
            return 0.5  # Neutral score on failure

    def rerank(
        self,
        query: str,
        documents: List[Dict[str, Any]],
        top_k: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Re-rank documents using LLM scoring.

        Args:
            query: The search query
            documents: List of documents with 'document' key
            top_k: Number of top results to return

        Returns:
            Re-ranked documents with 'rerank_score'
        """
        if not documents:
            return []

        logger.info(f"LLM re-ranking {len(documents)} documents...")

        for doc in documents:
            doc_text = doc.get("document", "")
            score = self._score_document(query, doc_text)
            doc["rerank_score"] = score

        reranked = sorted(
            documents,
            key=lambda x: x.get("rerank_score", 0),
            reverse=True
        )

        logger.info(f"LLM re-ranking complete, top score: {reranked[0].get('rerank_score', 0):.2f}")

        return reranked[:top_k] if top_k else reranked

    def __del__(self):
        """Cleanup HTTP client."""
        if self._client:
            try:
                self._client.close()
            except Exception:
                pass


# Singleton instances
_lightweight_reranker: Optional[LightweightReranker] = None
_ollama_reranker: Optional[OllamaReranker] = None


def get_reranker(use_lightweight: bool = True) -> LightweightReranker | OllamaReranker:
    """
    Get or create the re-ranker singleton.

    Args:
        use_lightweight: If True (default), use fast heuristic reranker.
                        If False, use Ollama LLM reranker (slower, more accurate).
    """
    global _lightweight_reranker, _ollama_reranker

    if use_lightweight:
        if _lightweight_reranker is None:
            _lightweight_reranker = LightweightReranker()
        return _lightweight_reranker
    else:
        if _ollama_reranker is None:
            _ollama_reranker = OllamaReranker()
        return _ollama_reranker
