/**
 * Skills data for the portfolio.
 * Based on actual skills from resume.
 */

import { Brain, Database, Layers, Code, Server, Cpu } from "lucide-react";
import { Skill } from "@/types";

export const skills: Skill[] = [
  { name: "JavaScript/TypeScript", icon: <Code className="w-6 h-6" />, level: 95 },
  { name: "React/Next.js", icon: <Code className="w-6 h-6" />, level: 90 },
  { name: "PHP/MySQL", icon: <Database className="w-6 h-6" />, level: 90 },
  { name: "Python/AI", icon: <Brain className="w-6 h-6" />, level: 85 },
  { name: "Docker/DevOps", icon: <Server className="w-6 h-6" />, level: 88 },
  { name: "RAG Systems", icon: <Layers className="w-6 h-6" />, level: 85 },
];

