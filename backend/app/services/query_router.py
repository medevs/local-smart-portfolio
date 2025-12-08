"""
Query Router Service for Advanced RAG.
Determines if RAG retrieval is needed or if the query can be answered directly.
"""

from typing import Optional, List, Dict
from enum import Enum
from app.utils.logger import logger


class QueryType(Enum):
    """Types of queries the router can identify."""
    PORTFOLIO_FACTUAL = "portfolio_factual"    # Needs RAG for specific portfolio facts
    PORTFOLIO_GENERAL = "portfolio_general"    # Can use built-in knowledge
    GREETING = "greeting"                       # Greetings, no RAG needed
    CHITCHAT = "chitchat"                       # Small talk, no RAG needed
    OFF_TOPIC = "off_topic"                     # Not portfolio-related
    CLARIFICATION = "clarification"            # Follow-up or clarification


class QueryRouter:
    """
    Routes queries to the appropriate handling strategy.

    This saves resources by:
    1. Not running RAG for greetings or chitchat
    2. Using built-in knowledge for common portfolio questions
    3. Only querying the vector DB for specific document lookups
    """

    def __init__(self):
        # Greeting patterns
        self.greeting_patterns = {
            "hi", "hello", "hey", "good morning", "good afternoon",
            "good evening", "howdy", "greetings", "sup", "yo",
            "hola", "bonjour", "hallo", "guten tag", "salut"
        }

        # Chitchat patterns (questions not about portfolio)
        self.chitchat_patterns = [
            "how are you", "what's up", "how's it going",
            "nice to meet", "thank you", "thanks", "bye",
            "goodbye", "see you", "take care", "have a nice day"
        ]

        # Portfolio keywords that suggest RAG is needed
        self.portfolio_keywords = {
            # Skills
            "skill", "skills", "technology", "technologies", "tech stack",
            "programming", "language", "languages", "framework", "frameworks",
            "tool", "tools", "expertise", "proficient", "experience with",

            # Experience
            "experience", "work", "job", "company", "companies",
            "career", "position", "role", "project", "projects",
            "employment", "employer", "worked", "working",

            # Education
            "education", "degree", "university", "school", "college",
            "certification", "certified", "training", "course",

            # Personal/Contact
            "contact", "email", "phone", "location", "address",
            "about", "background", "bio", "profile", "summary",
            "github", "linkedin", "portfolio", "website",

            # Person references
            "ahmed", "oublihi", "developer", "engineer",
        }

        # Built-in knowledge topics (don't need RAG)
        self.builtin_topics = {
            "name", "title", "email", "github", "location",
            "frontend", "backend", "database", "ai", "devops",
            "ephilos", "freelance",
        }

        # Topics that need RAG for details
        self.rag_needed_topics = {
            "document", "uploaded", "file", "pdf", "resume", "cv",
            "specific", "detail", "particular", "which project",
            "tell me more", "elaborate", "explain more",
        }

    def route(
        self,
        query: str,
        history: Optional[List[Dict]] = None
    ) -> tuple[QueryType, bool]:
        """
        Route a query to determine handling strategy.

        Args:
            query: User's query
            history: Conversation history

        Returns:
            Tuple of (QueryType, needs_rag: bool)
        """
        query_lower = query.lower().strip()

        # Check for greetings
        if self._is_greeting(query_lower):
            logger.debug(f"Query routed as: GREETING")
            return QueryType.GREETING, False

        # Check for chitchat
        if self._is_chitchat(query_lower):
            logger.debug(f"Query routed as: CHITCHAT")
            return QueryType.CHITCHAT, False

        # Check for clarification/follow-up
        if self._is_clarification(query_lower, history):
            logger.debug(f"Query routed as: CLARIFICATION")
            return QueryType.CLARIFICATION, True

        # Check for portfolio-related query
        if self._is_portfolio_query(query_lower):
            # Determine if RAG is needed or built-in knowledge suffices
            needs_rag = self._needs_rag(query_lower)
            query_type = QueryType.PORTFOLIO_FACTUAL if needs_rag else QueryType.PORTFOLIO_GENERAL
            logger.debug(f"Query routed as: {query_type.value}, needs_rag: {needs_rag}")
            return query_type, needs_rag

        # Default: treat as potentially off-topic but still try to help
        logger.debug(f"Query routed as: OFF_TOPIC")
        return QueryType.OFF_TOPIC, False

    def _is_greeting(self, query: str) -> bool:
        """Check if query is a greeting."""
        # Remove punctuation for matching
        query_clean = query.rstrip("!?.,")

        # Exact match
        if query_clean in self.greeting_patterns:
            return True

        # Check if starts with greeting
        for greeting in self.greeting_patterns:
            if query_clean.startswith(greeting):
                # Make sure it's not a longer portfolio question
                remainder = query_clean[len(greeting):].strip()
                if not remainder or not self._is_portfolio_query(remainder):
                    return True

        return False

    def _is_chitchat(self, query: str) -> bool:
        """Check if query is chitchat."""
        for pattern in self.chitchat_patterns:
            if pattern in query:
                return True
        return False

    def _is_clarification(
        self,
        query: str,
        history: Optional[List[Dict]]
    ) -> bool:
        """Check if query is a clarification or follow-up."""
        clarification_patterns = [
            "i mean", "no,", "no i", "not that", "i meant",
            "what about", "how about", "and also", "also",
            "more about", "tell me more", "elaborate",
        ]

        for pattern in clarification_patterns:
            if query.startswith(pattern):
                return True

        # Check for very short follow-ups with history
        if history and len(query.split()) <= 3:
            # Likely a follow-up like "and skills?" or "his projects?"
            return True

        return False

    def _is_portfolio_query(self, query: str) -> bool:
        """Check if query is related to portfolio content."""
        # Check for portfolio keywords
        for keyword in self.portfolio_keywords:
            if keyword in query:
                return True

        # Check for question patterns about a person
        person_patterns = [
            "who is", "who's", "tell me about", "what does",
            "where does", "what are", "what is", "how did",
        ]
        for pattern in person_patterns:
            if query.startswith(pattern):
                return True

        return False

    def _needs_rag(self, query: str) -> bool:
        """Determine if RAG retrieval is needed for this portfolio query."""
        # Check for topics that specifically need RAG
        for topic in self.rag_needed_topics:
            if topic in query:
                return True

        # Check for topics that can use built-in knowledge
        builtin_match_count = sum(
            1 for topic in self.builtin_topics if topic in query
        )

        # If multiple built-in topics match, probably doesn't need RAG
        if builtin_match_count >= 2:
            return False

        # For general portfolio questions, use RAG to potentially get more detail
        return True

    def get_routing_hint(self, query_type: QueryType) -> str:
        """Get a hint for how to handle this query type."""
        hints = {
            QueryType.GREETING: "Respond with a friendly greeting and offer to help with portfolio questions.",
            QueryType.CHITCHAT: "Respond briefly and redirect to portfolio assistance.",
            QueryType.PORTFOLIO_GENERAL: "Use built-in knowledge about Ahmed. RAG optional.",
            QueryType.PORTFOLIO_FACTUAL: "Use RAG to find specific information from documents.",
            QueryType.CLARIFICATION: "Use conversation history and RAG to address the follow-up.",
            QueryType.OFF_TOPIC: "Politely redirect to portfolio-related topics.",
        }
        return hints.get(query_type, "")


# Singleton instance
_query_router: Optional[QueryRouter] = None


def get_query_router() -> QueryRouter:
    """Get or create the query router singleton."""
    global _query_router
    if _query_router is None:
        _query_router = QueryRouter()
    return _query_router
