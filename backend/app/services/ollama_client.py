"""
Ollama LLM client for generating responses.
Supports both streaming and non-streaming responses.
Production-ready with improved prompt engineering for RAG chatbots.
"""

import httpx
import json
from typing import AsyncGenerator, Optional, List, Dict
from app.config import get_settings
from app.utils.logger import logger


# ============================================================================
# AHMED'S CORE KNOWLEDGE BASE (Always available, no RAG needed)
# ============================================================================
AHMED_KNOWLEDGE = {
    "personal": {
        "name": "Ahmed Oublihi",
        "title": "Software Engineer | Local AI/LLM Specialist",
        "location": "Delmenhorst, Germany",
        "email": "oublihi.a@gmail.com",
        "github": "https://github.com/medevs",
        "bio": "I help founders build production-ready AI systems with self-hosted LLMs, reducing costs by up to 90% while maintaining complete data privacy and control. Specialized in Local AI deployment, RAG systems, and modern web applications.",
    },
    "skills": {
        "frontend": [
            "JavaScript",
            "TypeScript",
            "React",
            "Next.js",
            "Material UI",
            "Tailwind CSS",
        ],
        "backend": ["Node.js", "PHP", "Python", "Express.js", "FastAPI"],
        "databases": ["MySQL", "PostgreSQL", "MongoDB", "ChromaDB"],
        "ai": ["Langchain", "LangGraph", "OpenAI API", "RAG", "Ollama", "Local LLMs"],
        "devops": ["Git", "Docker", "CI/CD", "Linux"],
        "other": ["RESTful APIs", "tRPC", "WebSockets", "Agile"],
    },
    "experience": [
        {
            "role": "Full Stack Developer",
            "company": "ePhilos AG",
            "period": "May 2024 - June 2025",
            "location": "Bremen, Germany",
            "highlights": [
                "WebSocket implementation",
                "Code reviews",
                "Mentoring apprentices",
            ],
        },
        {
            "role": "IT Specialist Apprentice",
            "company": "ePhilos AG",
            "period": "Aug 2021 - May 2024",
            "location": "Bremen, Germany",
            "highlights": [
                "Full Stack Development",
                "Agile teams",
                "IHK certification",
            ],
        },
        {
            "role": "Freelance Web Developer",
            "company": "Self-employed",
            "period": "Mar 2020 - Jun 2021",
            "location": "Morocco (Remote)",
            "highlights": ["Responsive websites", "SEO optimization", "WordPress"],
        },
    ],
}


def format_knowledge_for_prompt() -> str:
    """Format Ahmed's knowledge into a concise prompt section."""
    k = AHMED_KNOWLEDGE

    return f"""=== AHMED OUBLIHI - PORTFOLIO DATA ===
        Name: {k['personal']['name']}
        Title: {k['personal']['title']}
        Location: {k['personal']['location']}
        Email: {k['personal']['email']}
        GitHub: {k['personal']['github']}

        Bio: {k['personal']['bio']}

        SKILLS:
        - Frontend: {', '.join(k['skills']['frontend'])}
        - Backend: {', '.join(k['skills']['backend'])}
        - Databases: {', '.join(k['skills']['databases'])}
        - AI/ML: {', '.join(k['skills']['ai'])}
        - DevOps: {', '.join(k['skills']['devops'])}

        EXPERIENCE:
        """ + "\n".join(
                [
                    f"- {exp['role']} at {exp['company']} ({exp['period']})"
                    for exp in k["experience"]
                ]
            )


class OllamaClient:
    """Client for interacting with Ollama API."""

    def __init__(self, base_url: Optional[str] = None, model: Optional[str] = None):
        settings = get_settings()
        self.base_url = base_url or settings.ollama_base_url
        self.model = model or settings.ollama_model
        self.timeout = httpx.Timeout(180.0, connect=30.0)

    async def check_connection(self) -> bool:
        """Check if Ollama is available."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Failed to connect to Ollama: {e}")
            return False

    async def list_models(self) -> list:
        """List available models."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                if response.status_code == 200:
                    data = response.json()
                    return [model["name"] for model in data.get("models", [])]
                return []
        except Exception as e:
            logger.error(f"Failed to list models: {e}")
            return []

    def _resolve_query_context(self, query: str, history: List[Dict] = None) -> str:
        """
        Resolve pronouns and implicit references in the query using conversation history.
        This fixes issues like "i mean ahmed" or "your skills" -> "Ahmed's skills"
        """
        query_lower = query.lower().strip()

        # Common pronoun resolutions for portfolio context
        pronoun_mappings = {
            "your skills": "Ahmed's skills",
            "your experience": "Ahmed's experience",
            "your projects": "Ahmed's projects",
            "your education": "Ahmed's education",
            "what can you do": "what can Ahmed do as a developer",
            "tell me about yourself": "tell me about Ahmed",
            "who are you": "who is Ahmed",
        }

        # Check for direct pronoun matches
        for pronoun, replacement in pronoun_mappings.items():
            if pronoun in query_lower:
                return query_lower.replace(pronoun, replacement)

        # Handle "i mean X" pattern - look for previous context
        if (
            query_lower.startswith("i mean")
            or query_lower.startswith("no,")
            or query_lower.startswith("no ")
        ):
            if history and len(history) >= 2:
                # Get the previous exchange to understand context
                prev_user = None
                for msg in reversed(history[:-1]):
                    if msg.get("role") == "user":
                        prev_user = msg.get("content", "")
                        break

                if prev_user:
                    # Extract the clarification (e.g., "ahmed" from "i mean ahmed")
                    clarification = (
                        query_lower.replace("i mean", "")
                        .replace("no,", "")
                        .replace("no ", "")
                        .strip()
                    )

                    # If the clarification is just a name/noun, reformulate
                    if clarification in ["ahmed", "ahmed's", "his"]:
                        # Reformulate the previous question about Ahmed
                        if "skills" in prev_user.lower():
                            return "What are Ahmed's skills?"
                        elif (
                            "experience" in prev_user.lower()
                            or "work" in prev_user.lower()
                        ):
                            return "Tell me about Ahmed's work experience"
                        elif "projects" in prev_user.lower():
                            return "What projects has Ahmed worked on?"
                        else:
                            return f"Tell me about Ahmed: {prev_user}"

        return query

    def _build_messages(
        self, query: str, context: str, history: List[Dict] = None
    ) -> List[Dict]:
        """
        Build chat messages for Ollama chat API with production-ready prompts.

        Key improvements:
        1. Always includes Ahmed's core knowledge
        2. Properly processes conversation history for context
        3. Resolves pronouns and implicit references
        4. Uses structured prompt with clear sections
        5. Handles uncertainty gracefully
        """

        # Resolve pronouns and implicit references
        resolved_query = self._resolve_query_context(query, history)

        # Build the system prompt with Ahmed's knowledge + RAG context
        knowledge_section = format_knowledge_for_prompt()

        # Process RAG context if available (use more context, up to 1500 chars)
        rag_context = ""
        if context and context.strip():
            clean_context = context.replace("[Source:", "\n[Source:").strip()
            rag_context = (
                f"\n\n=== ADDITIONAL CONTEXT FROM DOCUMENTS ===\n{clean_context[:1500]}"
            )

        # Production-ready system prompt
        system_content = f"""You are Ahmed Oublihi's portfolio assistant. Your job is to answer questions about Ahmed's skills, experience, projects, and background.

{knowledge_section}{rag_context}

=== RESPONSE GUIDELINES ===
1. ALWAYS respond in English unless the user writes in another language
2. When asked about "skills", "experience", "projects" - ALWAYS refer to Ahmed's data above
3. If the user says "your skills" or "your experience", they mean AHMED's skills/experience
4. If asked about something not in the data, say "I don't have that information about Ahmed"
5. Be concise (2-4 sentences) but complete
6. Be friendly and professional
7. If unsure, ask for clarification rather than guessing

Remember: You represent Ahmed's portfolio. All questions about "you" refer to Ahmed."""

        messages = [{"role": "system", "content": system_content}]

        # Include more conversation history for better context (last 4 exchanges)
        if history:
            for msg in history[-4:]:
                messages.append(
                    {"role": msg.get("role", "user"), "content": msg.get("content", "")}
                )

        # Add the resolved query
        messages.append({"role": "user", "content": resolved_query})

        logger.debug(f"Original query: {query}")
        logger.debug(f"Resolved query: {resolved_query}")

        return messages

    def _build_prompt(self, query: str, context: str, history: list = None) -> str:
        """Legacy prompt builder - kept for compatibility."""
        return f"Q: {query}\nA:"

    async def generate(
        self,
        query: str,
        context: str = "",
        history: list = None,
        model: Optional[str] = None,
    ) -> str:
        """
        Generate a response using Ollama chat API (non-streaming).
        Uses production-ready settings for portfolio chatbot.
        """
        messages = self._build_messages(query, context, history)

        payload = {
            "model": model or self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": 0.4,  # Slightly creative but focused
                "num_predict": 200,  # Allow longer responses (2-4 sentences)
                "repeat_penalty": 1.1,  # Reduce repetition
                "top_p": 0.9,  # Nucleus sampling for coherence
                "top_k": 40,  # Limit vocabulary for consistency
            },
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(f"{self.base_url}/api/chat", json=payload)

                if response.status_code == 200:
                    data = response.json()
                    response_text = data.get("message", {}).get("content", "")
                    logger.info(f"Generated response: {response_text[:100]}...")
                    return response_text
                else:
                    logger.error(
                        f"Ollama error: {response.status_code} - {response.text}"
                    )
                    return "Sorry, I encountered an error. Please try again."

        except httpx.TimeoutException:
            logger.error("Ollama request timed out")
            return "Request timed out. Please try again."
        except Exception as e:
            logger.error(f"Ollama error: {e}")
            return "Sorry, something went wrong. Please try again."

    async def generate_stream(
        self,
        query: str,
        context: str = "",
        history: list = None,
        model: Optional[str] = None,
    ) -> AsyncGenerator[str, None]:
        """
        Generate a streaming response using Ollama chat API.
        Uses production-ready settings for portfolio chatbot.
        """
        messages = self._build_messages(query, context, history)

        payload = {
            "model": model or self.model,
            "messages": messages,
            "stream": True,
            "options": {
                "temperature": 0.4,  # Slightly creative but focused
                "num_predict": 200,  # Allow longer responses
                "repeat_penalty": 1.1,  # Reduce repetition
                "top_p": 0.9,  # Nucleus sampling
                "top_k": 40,  # Vocabulary limit
            },
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                async with client.stream(
                    "POST", f"{self.base_url}/api/chat", json=payload
                ) as response:
                    if response.status_code != 200:
                        logger.error(f"Ollama stream error: {response.status_code}")
                        yield "Sorry, I encountered an error. Please try again."
                        return

                    async for line in response.aiter_lines():
                        if line:
                            try:
                                data = json.loads(line)
                                chunk = data.get("message", {}).get("content", "")
                                if chunk:
                                    yield chunk
                                if data.get("done", False):
                                    break
                            except json.JSONDecodeError:
                                continue

        except httpx.TimeoutException:
            logger.error("Ollama stream request timed out")
            yield "Request timed out. Please try again."
        except Exception as e:
            logger.error(f"Ollama stream error: {e}")
            yield "Sorry, something went wrong. Please try again."


# Singleton instance
_ollama_client: Optional[OllamaClient] = None


def get_ollama_client() -> OllamaClient:
    """Get or create the Ollama client singleton."""
    global _ollama_client
    if _ollama_client is None:
        _ollama_client = OllamaClient()
    return _ollama_client
