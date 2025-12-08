"""
Hybrid Search Service for Advanced RAG.
Combines semantic search (ChromaDB) with keyword search (BM25).
"""

import re
from typing import List, Dict, Any, Optional, Tuple
from rank_bm25 import BM25Okapi
from app.utils.logger import logger
from app.services.chroma_client import get_chroma_service


class HybridSearch:
    """
    Combines semantic (vector) search with keyword (BM25) search.

    Benefits:
    1. Semantic search captures meaning and concepts
    2. BM25 captures exact keyword matches
    3. Combination provides better recall for both types of queries
    """

    def __init__(self, semantic_weight: float = 0.6, keyword_weight: float = 0.4):
        """
        Initialize hybrid search with configurable weights.

        Args:
            semantic_weight: Weight for semantic search results (0-1)
            keyword_weight: Weight for keyword search results (0-1)
        """
        self.chroma = get_chroma_service()
        self.semantic_weight = semantic_weight
        self.keyword_weight = keyword_weight

        # BM25 index (built on demand)
        self._bm25_index: Optional[BM25Okapi] = None
        self._corpus: List[str] = []
        self._corpus_metadata: List[Dict] = []
        self._corpus_ids: List[str] = []

    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenizer for BM25."""
        # Convert to lowercase and split on non-alphanumeric
        text = text.lower()
        tokens = re.findall(r'\b\w+\b', text)
        # Remove very short tokens and common stopwords
        stopwords = {
            'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
            'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'could', 'should', 'may', 'might', 'must', 'can',
            'of', 'in', 'to', 'for', 'with', 'on', 'at', 'by', 'from',
            'as', 'into', 'through', 'during', 'before', 'after',
            'and', 'or', 'but', 'if', 'then', 'else', 'when', 'where',
            'this', 'that', 'these', 'those', 'it', 'its'
        }
        return [t for t in tokens if len(t) > 2 and t not in stopwords]

    def _build_bm25_index(self) -> None:
        """Build BM25 index from all documents in ChromaDB."""
        logger.info("Building BM25 index...")

        # Get all raw documents from ChromaDB collection (with content)
        try:
            results = self.chroma.collection.get(include=["documents", "metadatas"])

            if not results or not results.get("documents"):
                logger.warning("No documents found for BM25 index")
                self._bm25_index = None
                return

            self._corpus = []
            self._corpus_metadata = []
            self._corpus_ids = []

            documents = results.get("documents", [])
            metadatas = results.get("metadatas", [])
            ids = results.get("ids", [])

            for i, doc in enumerate(documents):
                if doc:
                    self._corpus.append(doc)
                    self._corpus_metadata.append(metadatas[i] if i < len(metadatas) else {})
                    self._corpus_ids.append(ids[i] if i < len(ids) else "")

        except Exception as e:
            logger.error(f"Error building BM25 index: {e}")
            self._bm25_index = None
            return

        if self._corpus:
            # Tokenize corpus for BM25
            tokenized_corpus = [self._tokenize(doc) for doc in self._corpus]
            self._bm25_index = BM25Okapi(tokenized_corpus)
            logger.info(f"BM25 index built with {len(self._corpus)} documents")
        else:
            self._bm25_index = None
            logger.warning("Empty corpus for BM25 index")

    def _bm25_search(
        self,
        query: str,
        top_k: int = 10
    ) -> List[Tuple[str, Dict, float]]:
        """
        Perform BM25 keyword search.

        Returns:
            List of (document, metadata, score) tuples
        """
        if self._bm25_index is None:
            self._build_bm25_index()

        if self._bm25_index is None or not self._corpus:
            return []

        # Tokenize query
        query_tokens = self._tokenize(query)

        if not query_tokens:
            return []

        # Get BM25 scores
        scores = self._bm25_index.get_scores(query_tokens)

        # Get top-k results
        scored_docs = list(zip(
            self._corpus,
            self._corpus_metadata,
            self._corpus_ids,
            scores
        ))

        # Sort by score descending
        scored_docs.sort(key=lambda x: x[3], reverse=True)

        # Return top-k with score > 0
        results = [
            (doc, meta, score)
            for doc, meta, doc_id, score in scored_docs[:top_k]
            if score > 0
        ]

        logger.debug(f"BM25 search found {len(results)} results for: {query[:50]}")
        return results

    def _semantic_search(
        self,
        query: str,
        top_k: int = 10
    ) -> List[Tuple[str, Dict, float]]:
        """
        Perform semantic (vector) search using ChromaDB.

        Returns:
            List of (document, metadata, score) tuples
        """
        results = self.chroma.query(query, n_results=top_k)

        documents = results.get("documents", [])
        metadatas = results.get("metadatas", [])
        distances = results.get("distances", [])

        if not documents:
            return []

        # Convert distances to similarity scores (lower distance = higher similarity)
        # ChromaDB uses L2 distance by default, so we normalize to 0-1 range
        semantic_results = []
        for doc, meta, dist in zip(documents, metadatas, distances):
            # Convert distance to similarity score (assuming max distance ~2 for normalized vectors)
            similarity = max(0, 1 - (dist / 2))
            semantic_results.append((doc, meta, similarity))

        logger.debug(f"Semantic search found {len(semantic_results)} results for: {query[:50]}")
        return semantic_results

    def search(
        self,
        query: str,
        top_k: int = 5,
        use_bm25: bool = True,
        use_semantic: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Perform hybrid search combining semantic and keyword search.

        Args:
            query: Search query
            top_k: Number of results to return
            use_bm25: Whether to use BM25 keyword search
            use_semantic: Whether to use semantic search

        Returns:
            List of search results with combined scores
        """
        # Get more results from each method to ensure good coverage after merging
        fetch_k = top_k * 2

        results_map: Dict[str, Dict[str, Any]] = {}

        # Perform semantic search
        if use_semantic:
            semantic_results = self._semantic_search(query, fetch_k)
            for doc, meta, score in semantic_results:
                doc_key = doc[:100]  # Use first 100 chars as key
                if doc_key not in results_map:
                    results_map[doc_key] = {
                        "document": doc,
                        "metadata": meta,
                        "semantic_score": 0,
                        "bm25_score": 0,
                    }
                results_map[doc_key]["semantic_score"] = score

        # Perform BM25 search
        if use_bm25:
            bm25_results = self._bm25_search(query, fetch_k)

            # Normalize BM25 scores to 0-1 range
            if bm25_results:
                max_bm25 = max(score for _, _, score in bm25_results)
                if max_bm25 > 0:
                    bm25_results = [
                        (doc, meta, score / max_bm25)
                        for doc, meta, score in bm25_results
                    ]

            for doc, meta, score in bm25_results:
                doc_key = doc[:100]
                if doc_key not in results_map:
                    results_map[doc_key] = {
                        "document": doc,
                        "metadata": meta,
                        "semantic_score": 0,
                        "bm25_score": 0,
                    }
                results_map[doc_key]["bm25_score"] = score

        # Calculate combined scores using Reciprocal Rank Fusion (RRF)
        final_results = []
        for doc_key, data in results_map.items():
            # Weighted combination
            combined_score = (
                self.semantic_weight * data["semantic_score"] +
                self.keyword_weight * data["bm25_score"]
            )

            final_results.append({
                "document": data["document"],
                "metadata": data["metadata"],
                "score": combined_score,
                "semantic_score": data["semantic_score"],
                "bm25_score": data["bm25_score"],
            })

        # Sort by combined score
        final_results.sort(key=lambda x: x["score"], reverse=True)

        logger.info(
            f"Hybrid search returned {len(final_results[:top_k])} results "
            f"(semantic: {use_semantic}, bm25: {use_bm25})"
        )

        return final_results[:top_k]

    def refresh_index(self) -> None:
        """Rebuild the BM25 index (call after document changes)."""
        self._bm25_index = None
        self._corpus = []
        self._corpus_metadata = []
        self._corpus_ids = []
        self._build_bm25_index()


# Singleton instance
_hybrid_search: Optional[HybridSearch] = None


def get_hybrid_search() -> HybridSearch:
    """Get or create the hybrid search singleton."""
    global _hybrid_search
    if _hybrid_search is None:
        _hybrid_search = HybridSearch()
    return _hybrid_search
