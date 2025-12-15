import re
from typing import List, Dict, Any
from sqlalchemy import select, text, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import AsyncSessionLocal
from app.db.models import Document
from app.utils.logger import logger
from .base import BaseTool

# Common stop words to filter out
STOP_WORDS = {'what', 'where', 'when', 'who', 'how', 'why', 'is', 'are', 'was', 'were',
              'do', 'does', 'did', 'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on',
              'at', 'to', 'for', 'of', 'with', 'by', 'about', 'can', 'could', 'would',
              'should', 'have', 'has', 'had', 'be', 'been', 'being', 'this', 'that'}

# Query expansion: synonyms for better recall
SYNONYMS = {
    'job': ['work', 'position', 'role', 'employment', 'experience'],
    'work': ['job', 'position', 'role', 'employment', 'experience'],
    'company': ['employer', 'organization', 'firm'],
    'skill': ['skills', 'technology', 'technologies', 'expertise'],
    'skills': ['skill', 'technology', 'technologies', 'expertise'],
    'education': ['degree', 'diploma', 'university', 'school', 'training'],
    'project': ['projects', 'portfolio', 'work'],
    'projects': ['project', 'portfolio', 'work'],
    'language': ['languages', 'speak', 'fluent'],
    'languages': ['language', 'speak', 'fluent'],
}


class KeywordSearchTool(BaseTool):
    name = "keyword_search"
    description = "Use this tool to find exact matches for terms, dates, product names, or IDs in the document content."

    def _build_tsquery(self, query: str) -> str:
        """
        Build OR-based tsquery from natural language query.
        Filters stop words, expands synonyms, joins with OR (|).
        """
        # Extract words, lowercase, filter stop words
        words = re.findall(r'\b\w+\b', query.lower())
        keywords = [w for w in words if w not in STOP_WORDS and len(w) > 2]

        if not keywords:
            # Fallback: use all words if filtering removed everything
            keywords = [w for w in words if len(w) > 2]

        # Expand with synonyms for better recall
        expanded = set(keywords)
        for word in keywords:
            if word in SYNONYMS:
                expanded.update(SYNONYMS[word])

        # Join with OR operator for PostgreSQL tsquery
        return ' | '.join(expanded) if expanded else query

    async def execute(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Execute full-text search using PostgreSQL's tsvector with GIN index.
        Uses OR-based to_tsquery for better natural language matching.
        """
        # Build OR-based query from natural language
        tsquery_str = self._build_tsquery(query)
        logger.info(f"[KEYWORD] Query: '{query}' -> tsquery: '{tsquery_str}'")

        try:
            async with AsyncSessionLocal() as session:
                # Use to_tsquery with OR logic for better recall
                # ts_rank orders by relevance
                stmt = (
                    select(
                        Document,
                        func.ts_rank(Document.tsv, func.to_tsquery('english', tsquery_str)).label('rank')
                    )
                    .where(Document.tsv.op('@@')(func.to_tsquery('english', tsquery_str)))
                    .order_by(text('rank DESC'))
                    .limit(limit)
                )

                result = await session.execute(stmt)
                rows = result.all()

                logger.info(f"[KEYWORD] TSVECTOR returned {len(rows)} results")

                return [
                    {
                        "id": str(row.Document.id),
                        "content": row.Document.content,
                        "metadata": {
                            "source": row.Document.source,
                            "title": row.Document.title,
                            "rank": float(row.rank) if row.rank else 0.0
                        }
                    }
                    for row in rows
                ]
        except Exception as e:
            logger.error(f"[KEYWORD] Error: {e}")
            return []
