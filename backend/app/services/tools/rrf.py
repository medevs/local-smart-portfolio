from typing import List, Dict, Any, Tuple

def reciprocal_rank_fusion(
    semantic_results: List[Dict[str, Any]],
    keyword_results: List[Dict[str, Any]],
    k: int = 60
) -> List[Dict[str, Any]]:
    """
    Combine results from semantic and keyword search using Reciprocal Rank Fusion (RRF).
    
    RRF_score = Σ (1 / (k + rank))
    
    Args:
        semantic_results: List of documents from semantic search
        keyword_results: List of documents from keyword search
        k: Ranking constant (default 60)
        
    Returns:
        List of merged and ranked documents
    """
    scores: Dict[str, float] = {}
    doc_map: Dict[str, Dict[str, Any]] = {}
    
    # Process semantic results
    for rank, doc in enumerate(semantic_results):
        doc_id = str(doc.get("id"))
        if not doc_id:
            continue
            
        doc_map[doc_id] = doc
        scores[doc_id] = scores.get(doc_id, 0) + 1.0 / (k + rank + 1)
        
    # Process keyword results
    for rank, doc in enumerate(keyword_results):
        doc_id = str(doc.get("id"))
        if not doc_id:
            continue
            
        # Merge document data if not present (prefer semantic metadata if conflict?)
        if doc_id not in doc_map:
            doc_map[doc_id] = doc
            
        scores[doc_id] = scores.get(doc_id, 0) + 1.0 / (k + rank + 1)
        
    # Sort by score descending
    sorted_ids = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
    
    # Return merged documents with score
    results = []
    for doc_id in sorted_ids:
        doc = doc_map[doc_id]
        doc["rrf_score"] = scores[doc_id]
        results.append(doc)
        
    return results
