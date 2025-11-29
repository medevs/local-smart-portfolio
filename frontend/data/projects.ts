/**
 * Projects data for the portfolio.
 * Based on actual projects from resume.
 */

import { Project } from "@/types";

export const projects: Project[] = [
  {
    title: "TalkTheDoc",
    description:
      "AI application for real-time communication with document contents. Voice and text-based app for natural real-time communication with documents using Retrieval-Augmented Generation (RAG) for fast and context-accurate answers.",
    image:
      "https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=800&h=600&fit=crop",
    tags: ["Convex", "Next.js", "TypeScript", "AI SDK", "RAG", "Real-time"],
    github: undefined,
    live: "https://talkthedoc.com",
  },
  {
    title: "Docspresso",
    description:
      "AI application for automated creation of technical documentation. Systematically generates PRDs, architecture plans, and technical specifications to support AI Coding Agents during app development.",
    image:
      "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=600&fit=crop",
    tags: ["Langchain", "Next.js", "PostgreSQL", "TypeScript", "AI"],
    github: undefined,
    live: "https://docspresso.dev",
  },
  {
    title: "Your Daily Way",
    description:
      "SEO-optimized blog with 100% Google PageSpeed Score. Markdown-based CMS with focus on maximum performance and user-friendliness.",
    image:
      "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=800&h=600&fit=crop",
    tags: ["Astro", "React", "TypeScript", "MDX", "SEO"],
    github: undefined,
    live: "http://yourdailyway.com/",
  },
  {
    title: "AI-Powered Portfolio",
    description:
      "Self-hosted portfolio website with AI assistant powered by local LLMs and RAG technology. Features document ingestion, streaming chat, and admin dashboard. Fully deployed on homelab with CI/CD automation.",
    image:
      "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&h=600&fit=crop",
    tags: ["Next.js", "FastAPI", "Ollama", "ChromaDB", "Docker", "RAG"],
    github: undefined,
    live: "https://portfolio.medevs.local",
  },
];

