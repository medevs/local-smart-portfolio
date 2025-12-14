from rank_bm25 import BM25Okapi
from typing import List, Tuple, Optional
import numpy as np

class HybridRetriever:
    """Combines semantic search with BM25 keyword search."""

    def __init__(self, chroma_client, documents: List[str], doc_ids: List[str]):
        self.chroma = chroma_client
        self.documents = documents
        self.doc_ids = doc_ids
        # Tokenize documents for BM25
        self.bm25 = BM25Okapi([doc.lower().split() for doc in documents])

    def search(
        self,
        query: str,
        top_k: int = 5,
        alpha: float = 0.5
    ) -> List[Tuple[str, float]]:
        """
        Hybrid search with Reciprocal Rank Fusion.
        """
        # Semantic search
        semantic_results = self.chroma.query(
            query_texts=[query],
            n_results=top_k * 2
        )
        
        # Keyword search (BM25)
        tokenized_query = query.lower().split()
        bm25_scores = self.bm25.get_scores(tokenized_query)
        bm25_top_indices = np.argsort(bm25_scores)[::-1][:top_k * 2]

        # Reciprocal Rank Fusion
        combined_scores = {}
        k = 60

        # Add semantic ranks
        if semantic_results and 'ids' in semantic_results and semantic_results['ids']:
             for rank, doc_id in enumerate(semantic_results['ids'][0]):
                combined_scores[doc_id] = combined_scores.get(doc_id, 0) + alpha / (k + rank + 1)

        # Add BM25 ranks
        for rank, idx in enumerate(bm25_top_indices):
            if idx < len(self.doc_ids):
                doc_id = self.doc_ids[idx]
                combined_scores[doc_id] = combined_scores.get(doc_id, 0) + (1 - alpha) / (k + rank + 1)

        # Sort by combined score
        sorted_results = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)

        return sorted_results[:top_k]
