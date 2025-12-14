from typing import List, Dict, Any
from app.services.chroma_client import get_chroma_client
from app.utils.logger import logger
from .base import BaseTool


class SemanticSearchTool(BaseTool):
    name = "semantic_search"
    description = "Use this tool to find semantically similar content, concepts, or synonyms."

    def __init__(self):
        self.chroma = get_chroma_client()

    async def execute(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Execute semantic search using ChromaDB vector similarity.
        """
        logger.info(f"[SEMANTIC] Query: '{query}' (limit={limit})")

        try:
            results = self.chroma.query(
                query_texts=[query],
                n_results=limit
            )

            # Flatten results
            documents = []
            if results and 'documents' in results and results['documents']:
                for i, doc_text in enumerate(results['documents'][0]):
                    meta = results['metadatas'][0][i] if 'metadatas' in results else {}
                    doc_id = results['ids'][0][i] if 'ids' in results else ""

                    documents.append({
                        "id": doc_id,
                        "content": doc_text,
                        "metadata": meta
                    })

            logger.info(f"[SEMANTIC] ChromaDB returned {len(documents)} results")
            return documents

        except Exception as e:
            logger.error(f"[SEMANTIC] Error: {e}")
            return []
