from typing import List, Dict, Any
from sqlalchemy import select, text, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import AsyncSessionLocal
from app.db.models import Document
from app.utils.logger import logger
from .base import BaseTool


class KeywordSearchTool(BaseTool):
    name = "keyword_search"
    description = "Use this tool to find exact matches for terms, dates, product names, or IDs in the document content."

    async def execute(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Execute full-text search using PostgreSQL's tsvector.
        Falls back to ILIKE if tsvector returns no results.
        """
        logger.info(f"Keyword search: '{query}' (limit={limit})")

        try:
            async with AsyncSessionLocal() as session:
                # First try: Full-text search with plainto_tsquery (more forgiving)
                stmt = select(Document).where(
                    text("tsv @@ plainto_tsquery('english', :query)")
                ).params(query=query).limit(limit)

                result = await session.execute(stmt)
                documents = result.scalars().all()

                # Fallback: If no results, use simple ILIKE search
                if not documents:
                    logger.info(f"TSVECTOR returned 0, falling back to ILIKE search")
                    # Split query into words and search for any match
                    words = query.split()
                    conditions = [Document.content.ilike(f"%{word}%") for word in words]

                    stmt = select(Document).where(or_(*conditions)).limit(limit)
                    result = await session.execute(stmt)
                    documents = result.scalars().all()

                logger.info(f"Keyword search found {len(documents)} results")

                return [
                    {
                        "id": str(doc.id),
                        "content": doc.content,
                        "metadata": {
                            "source": doc.source,
                            "title": doc.title,
                        }
                    }
                    for doc in documents
                ]
        except Exception as e:
            logger.error(f"Keyword search error: {e}")
            return []
