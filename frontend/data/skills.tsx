/**
 * Skills data for the portfolio.
 */

import { Brain, Database, Layers, Code, Server, Cpu } from "lucide-react";
import { Skill } from "@/types";

export const skills: Skill[] = [
  { name: "Local LLMs", icon: <Brain className="w-6 h-6" />, level: 95 },
  { name: "RAG Systems", icon: <Database className="w-6 h-6" />, level: 90 },
  { name: "MLOps", icon: <Layers className="w-6 h-6" />, level: 85 },
  { name: "Full Stack", icon: <Code className="w-6 h-6" />, level: 90 },
  { name: "DevOps", icon: <Server className="w-6 h-6" />, level: 88 },
  { name: "Docker/K8s", icon: <Cpu className="w-6 h-6" />, level: 85 },
];

