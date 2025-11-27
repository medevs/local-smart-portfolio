/**
 * Projects data for the portfolio.
 */

import { Project } from "@/types";

export const projects: Project[] = [
  {
    title: "TalkTheDoc",
    description:
      "Real-time RAG system for document chat with streaming responses and vector embeddings",
    image:
      "https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=800&h=600&fit=crop",
    tags: ["RAG", "LangChain", "FastAPI", "ChromaDB"],
    github: "https://github.com",
    live: "https://demo.com",
  },
  {
    title: "Docspresso",
    description:
      "AI-powered documentation generator using local LLMs with markdown support",
    image:
      "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=600&fit=crop",
    tags: ["LLM", "Python", "Next.js", "Ollama"],
    github: "https://github.com",
    live: "https://demo.com",
  },
  {
    title: "Homelab AI System",
    description:
      "Self-hosted LLM infrastructure with Docker, reverse proxy, and monitoring",
    image:
      "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=800&h=600&fit=crop",
    tags: ["Docker", "Traefik", "Prometheus", "Ollama"],
    github: "https://github.com",
  },
  {
    title: "AI Agent Playground",
    description:
      "Interactive platform for testing document summarization and code explanation agents",
    image:
      "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&h=600&fit=crop",
    tags: ["LangChain", "React", "FastAPI", "WebSocket"],
    github: "https://github.com",
  },
];

