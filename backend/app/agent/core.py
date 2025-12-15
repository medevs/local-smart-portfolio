import httpx
from typing import List, Dict, Any, Optional
from app.services.tools.keyword_search import KeywordSearchTool
from app.services.tools.semantic_search import SemanticSearchTool
from app.services.tools.rrf import reciprocal_rank_fusion
from app.config import get_settings
from app.utils.logger import logger


class Agent:
    """
    Simplified RAG Agent - Always uses hybrid search for speed.
    No planning step - directly executes search and generates answer.

    This is much faster than the agentic approach because:
    1. No JSON planning step (saves 30-90s of LLM inference)
    2. Single LLM call for answer generation
    3. Direct hybrid search without tool selection
    """

    def __init__(self):
        self.settings = get_settings()
        self.base_url = self.settings.ollama_base_url
        self.model = self.settings.ollama_model
        # Increased timeout for slow Ollama responses on CPU
        self.timeout = httpx.Timeout(300.0, connect=60.0)

        self.keyword_tool = KeywordSearchTool()
        self.semantic_tool = SemanticSearchTool()

    async def _call_ollama(self, messages: List[Dict], max_tokens: int = 500) -> str:
        """Call Ollama chat API with increased timeout."""
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": 0.3,
                "num_predict": max_tokens,
            }
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(f"{self.base_url}/api/chat", json=payload)
                if response.status_code == 200:
                    data = response.json()
                    return data.get("message", {}).get("content", "")
                else:
                    logger.error(f"Ollama error: {response.status_code}")
                    return ""
        except httpx.TimeoutException:
            logger.error(f"Ollama timeout after {self.timeout.read}s")
            return ""
        except Exception as e:
            logger.error(f"Ollama call failed: {e}")
            return ""

    async def run(self, query: str, history: Optional[List[Dict[str, str]]] = None, max_steps: int = 1) -> str:
        """
        Simplified agent - single step:
        1. Execute both searches
        2. Merge results with RRF
        3. Generate answer from context

        No planning step = much faster response.
        """
        # Check for greetings - respond directly without any LLM call
        query_lower = query.lower().strip()
        greetings = ["hi", "hello", "hey", "hola", "bonjour", "good morning", "good afternoon", "good evening"]
        if any(query_lower.startswith(g) for g in greetings) or query_lower in greetings:
            return "Hello! I'm Ahmed's portfolio assistant. How can I help you learn about his experience and skills?"

        logger.info(f"[RAG] Query: {query[:50]}...")

        # Step 1: Execute BOTH searches (hybrid)
        semantic_results = await self.semantic_tool.execute(query=query, limit=10)
        keyword_results = await self.keyword_tool.execute(query=query, limit=10)

        # Step 2: Merge with RRF and log which path was used
        if semantic_results and keyword_results:
            merged_docs = reciprocal_rank_fusion(semantic_results, keyword_results)
            logger.info(f"[RAG] Path: HYBRID (semantic={len(semantic_results)}, keyword={len(keyword_results)}, merged={len(merged_docs)})")
        elif semantic_results:
            merged_docs = semantic_results
            logger.info(f"[RAG] Path: SEMANTIC_ONLY ({len(semantic_results)} results)")
        elif keyword_results:
            merged_docs = keyword_results
            logger.info(f"[RAG] Path: KEYWORD_ONLY ({len(keyword_results)} results)")
        else:
            logger.info("[RAG] Path: NO_RESULTS")
            return "I don't have any information about that in the uploaded documents. Please upload relevant documents first."

        # Log retrieved docs for debugging
        for i, doc in enumerate(merged_docs[:3]):
            source = doc.get('metadata', {}).get('source', 'unknown')
            preview = doc.get('content', '')[:80].replace('\n', ' ')
            logger.info(f"Doc {i+1}: {source} - {preview}...")

        # Step 3: Build context and generate answer (use top 8 chunks for better coverage)
        context_parts = []
        for doc in merged_docs[:8]:
            source = doc.get('metadata', {}).get('source', 'unknown')
            content = doc.get('content', '')
            if content:
                context_parts.append(f"[{source}]\n{content}")

        context = "\n\n---\n\n".join(context_parts)

        if not context:
            return "I couldn't find relevant information to answer your question."

        # Build messages for answer generation
        messages = [
            {"role": "system", "content": self._get_answer_system_prompt()},
        ]

        # Add conversation history if provided
        if history:
            messages.extend(history)

        # Add context and question
        messages.append({
            "role": "user",
            "content": f"""Based on the following information from Ahmed's documents, answer the question.

DOCUMENTS:
{context}

QUESTION: {query}

Answer based ONLY on the documents above. If the information is not in the documents, say so."""
        })

        # Generate answer
        logger.info("Generating answer from context...")
        answer = await self._call_ollama(messages, max_tokens=300)

        if not answer:
            return "I'm having trouble generating a response. Please try again."

        return answer

    def _get_answer_system_prompt(self) -> str:
        """System prompt for answer generation."""
        return """You are a friendly assistant on Ahmed Oublihi's portfolio website. You talk about Ahmed as if you know him well.

PERSONALITY:
- Warm and conversational, like chatting with a friend
- Enthusiastic about Ahmed's work
- Never robotic or formal

STRICT RULES:
1. NEVER say "According to", "Based on the documents", "resume says", or similar phrases
2. Just state facts directly as if you know Ahmed personally
3. Use bullet points for lists (skills, languages, etc.)
4. Keep responses short (2-4 sentences or a brief list)
5. If you don't have the info, say "I'm not sure - feel free to ask Ahmed directly!"

GOOD examples:
- "Ahmed's really skilled in React, Node.js, and Python!"
- "He speaks 5 languages - Berber and Arabic natively, plus German, English, and French."

BAD examples (NEVER do this):
- "According to his resume, Ahmed knows React..."
- "Based on the documents provided..."
- "The resume indicates..."

Sound natural and friendly!"""
