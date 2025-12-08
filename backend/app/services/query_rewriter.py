"""
Query Rewriter Service for Advanced RAG.
Uses LLM to reformulate queries for better retrieval.
"""

from typing import Optional, List, Dict
import httpx
from app.config import get_settings
from app.utils.logger import logger


class QueryRewriter:
    """
    Rewrites user queries to improve retrieval quality.

    Techniques:
    1. Query expansion - add related terms
    2. Query decomposition - break complex queries into sub-queries
    3. Hypothetical document generation (HyDE) - generate what an ideal answer looks like
    """

    def __init__(self):
        self.settings = get_settings()
        self.ollama_url = self.settings.ollama_base_url
        self.model = self.settings.ollama_model
        self.timeout = httpx.Timeout(60.0, connect=10.0)

    async def rewrite_query(
        self,
        query: str,
        history: Optional[List[Dict]] = None
    ) -> str:
        """
        Rewrite a query for better retrieval.

        Args:
            query: Original user query
            history: Conversation history for context

        Returns:
            Rewritten query optimized for retrieval
        """
        # First, resolve any pronouns or references
        resolved_query = self._resolve_references(query, history)

        # For simple queries, just expand them
        if self._is_simple_query(resolved_query):
            return self._expand_query(resolved_query)

        # For complex queries, use LLM to rewrite
        return await self._llm_rewrite(resolved_query)

    def _resolve_references(
        self,
        query: str,
        history: Optional[List[Dict]] = None
    ) -> str:
        """Resolve pronouns and references using conversation history."""
        query_lower = query.lower().strip()

        # Portfolio-specific pronoun mappings
        pronoun_mappings = {
            "your skills": "Ahmed Oublihi's skills",
            "your experience": "Ahmed Oublihi's experience",
            "your projects": "Ahmed Oublihi's projects",
            "your education": "Ahmed Oublihi's education",
            "your background": "Ahmed Oublihi's background",
            "what can you do": "what can Ahmed Oublihi do as a developer",
            "tell me about yourself": "tell me about Ahmed Oublihi",
            "who are you": "who is Ahmed Oublihi",
            "his skills": "Ahmed Oublihi's skills",
            "his experience": "Ahmed Oublihi's experience",
            "his projects": "Ahmed Oublihi's projects",
        }

        resolved = query
        for pronoun, replacement in pronoun_mappings.items():
            if pronoun in query_lower:
                resolved = query_lower.replace(pronoun, replacement)
                break

        # Handle follow-up clarifications like "i mean ahmed"
        if history and (
            query_lower.startswith("i mean") or
            query_lower.startswith("no,") or
            query_lower.startswith("no ")
        ):
            # Find the last user question to understand context
            prev_user_query = None
            for msg in reversed(history[:-1] if history else []):
                if msg.get("role") == "user":
                    prev_user_query = msg.get("content", "")
                    break

            if prev_user_query:
                clarification = (
                    query_lower
                    .replace("i mean", "")
                    .replace("no,", "")
                    .replace("no ", "")
                    .strip()
                )

                if clarification in ["ahmed", "ahmed's", "his", "him"]:
                    # Reformulate with Ahmed as subject
                    prev_lower = prev_user_query.lower()
                    if "skills" in prev_lower:
                        return "What are Ahmed Oublihi's skills and technologies?"
                    elif "experience" in prev_lower or "work" in prev_lower:
                        return "Tell me about Ahmed Oublihi's work experience"
                    elif "projects" in prev_lower:
                        return "What projects has Ahmed Oublihi worked on?"
                    elif "education" in prev_lower:
                        return "What is Ahmed Oublihi's educational background?"
                    else:
                        return f"Tell me about Ahmed Oublihi: {prev_user_query}"

        return resolved

    def _is_simple_query(self, query: str) -> bool:
        """Check if query is simple enough for rule-based expansion."""
        # Simple queries are short and don't contain complex structures
        word_count = len(query.split())
        has_complex_structure = any(word in query.lower() for word in [
            "how", "why", "compare", "difference", "explain", "describe"
        ])
        return word_count <= 6 and not has_complex_structure

    def _expand_query(self, query: str) -> str:
        """Expand query with related terms for better retrieval."""
        query_lower = query.lower()

        # Domain-specific expansions for portfolio context
        expansions = {
            "skills": "skills technologies programming languages frameworks tools expertise",
            "experience": "experience work job employment career professional history company",
            "projects": "projects portfolio applications apps software built created developed",
            "education": "education degree university school training certification academic",
            "contact": "contact email phone location address reach",
            "about": "about bio background summary profile introduction",
            "ahmed": "Ahmed Oublihi developer engineer software",
            "frontend": "frontend React Next.js TypeScript JavaScript UI",
            "backend": "backend Python FastAPI Node.js API server",
            "ai": "AI artificial intelligence LLM RAG machine learning Ollama",
            "devops": "DevOps Docker CI/CD Git Linux deployment",
        }

        expanded = query
        for term, expansion in expansions.items():
            if term in query_lower:
                expanded = f"{query} {expansion}"
                break

        logger.debug(f"Query expansion: '{query}' -> '{expanded}'")
        return expanded

    async def _llm_rewrite(self, query: str) -> str:
        """Use LLM to rewrite complex queries."""
        prompt = f"""Rewrite this query to be more specific for searching a portfolio/resume database about Ahmed Oublihi, a software engineer.

Original query: {query}

Rules:
1. Keep it concise (under 20 words)
2. Include relevant keywords
3. Make implicit references explicit
4. Focus on searchable terms
5. Always refer to "Ahmed Oublihi" instead of pronouns

Rewritten query:"""

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.3,
                            "num_predict": 50,
                        }
                    }
                )

                if response.status_code == 200:
                    data = response.json()
                    rewritten = data.get("response", "").strip()

                    # Validate the rewritten query
                    if rewritten and len(rewritten) < 200:
                        logger.debug(f"LLM query rewrite: '{query}' -> '{rewritten}'")
                        return rewritten

        except Exception as e:
            logger.warning(f"LLM query rewrite failed: {e}")

        # Fallback to expansion if LLM fails
        return self._expand_query(query)

    async def generate_sub_queries(self, query: str) -> List[str]:
        """
        Decompose a complex query into multiple sub-queries.
        Useful for multi-faceted questions.
        """
        # Check if decomposition is needed
        decomposition_triggers = ["and", "also", "as well as", "both", "multiple"]
        needs_decomposition = any(
            trigger in query.lower() for trigger in decomposition_triggers
        )

        if not needs_decomposition:
            return [query]

        prompt = f"""Break down this complex question into 2-3 simpler search queries.

Question: {query}

Rules:
1. Each sub-query should focus on one aspect
2. Keep queries short and specific
3. Include relevant keywords

Sub-queries (one per line):"""

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.3,
                            "num_predict": 100,
                        }
                    }
                )

                if response.status_code == 200:
                    data = response.json()
                    lines = data.get("response", "").strip().split("\n")
                    sub_queries = [
                        line.strip().lstrip("0123456789.-) ")
                        for line in lines
                        if line.strip() and len(line.strip()) > 5
                    ]

                    if sub_queries:
                        logger.debug(f"Query decomposition: '{query}' -> {sub_queries}")
                        return sub_queries[:3]  # Max 3 sub-queries

        except Exception as e:
            logger.warning(f"Query decomposition failed: {e}")

        return [query]

    async def generate_hyde_document(self, query: str) -> str:
        """
        Generate a Hypothetical Document Embedding (HyDE).
        Creates what an ideal answer might look like to improve retrieval.
        """
        prompt = f"""Write a brief, factual paragraph that would be a perfect answer to this question about Ahmed Oublihi's portfolio:

Question: {query}

Write as if this is from Ahmed's resume or portfolio. Be specific and professional. Keep it under 100 words.

Answer:"""

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.5,
                            "num_predict": 150,
                        }
                    }
                )

                if response.status_code == 200:
                    data = response.json()
                    hyde_doc = data.get("response", "").strip()

                    if hyde_doc:
                        logger.debug(f"Generated HyDE document for: '{query}'")
                        return hyde_doc

        except Exception as e:
            logger.warning(f"HyDE generation failed: {e}")

        # Fallback: return expanded query
        return self._expand_query(query)


# Singleton instance
_query_rewriter: Optional[QueryRewriter] = None


def get_query_rewriter() -> QueryRewriter:
    """Get or create the query rewriter singleton."""
    global _query_rewriter
    if _query_rewriter is None:
        _query_rewriter = QueryRewriter()
    return _query_rewriter
