import { Brain, Server, Code, TrendingUp } from "lucide-react";
import { ReactNode } from "react";

// Quick Facts
export interface QuickFact {
  icon: ReactNode;
  title: string;
  subtitle: string;
}

export const quickFacts: QuickFact[] = [
  {
    icon: <Brain className="w-5 h-5 text-amber-500 mt-1" />,
    title: "Local AI/LLM Specialist",
    subtitle: "Self-hosted LLMs, RAG, Ollama",
  },
  {
    icon: <Server className="w-5 h-5 text-amber-500 mt-1" />,
    title: "Full Stack Developer",
    subtitle: "PHP, JavaScript, TypeScript",
  },
  {
    icon: <Code className="w-5 h-5 text-amber-500 mt-1" />,
    title: "Production AI Systems",
    subtitle: "Python, Langchain, Generative AI",
  },
  {
    icon: <TrendingUp className="w-5 h-5 text-amber-500 mt-1" />,
    title: "4+ Years Experience",
    subtitle: "Enterprise & AI Solutions",
  },
];

// Journey Text (additional paragraphs for About page)
export const journeyText = {
  currentWork: "Currently working as a Full Stack Developer at ePhilos AG, where I develop and optimize enterprise software using PHP, MySQL, and JavaScript. I specialize in WebSocket implementations for real-time functionality and actively mentor apprentices while improving code quality through refactoring.",
  currentFocus: "My current focus is on Local AI/LLM systems and Generative AI, developing innovative solutions like TalkTheDoc and Docspresso. I'm passionate about building production-ready AI systems with self-hosted LLMs, maintaining full control over deployment and data privacy. I specialize in RAG systems, local AI deployment, and modern web applications that leverage AI while keeping everything self-hosted.",
};

