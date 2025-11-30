/**
 * Featured projects (shown on home page)
 */

import { Project } from "@/types";

export const featuredProjects: Project[] = [
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
];

