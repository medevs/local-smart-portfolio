/**
 * Skills data exports
 * Includes both technical skills and the skills array for SkillsCard
 */

import { Brain, Database, Layers, Code, Server, Cpu } from "lucide-react";
import { Skill } from "@/types";

export * from "./technical";
export * from "./languages";

// Skills array for SkillsCard component (backward compatibility)
export const skills: Skill[] = [
  { name: "JavaScript/TypeScript", icon: <Code className="w-6 h-6" />, level: 95 },
  { name: "React/Next.js", icon: <Code className="w-6 h-6" />, level: 90 },
  { name: "PHP/MySQL", icon: <Database className="w-6 h-6" />, level: 90 },
  { name: "Python/AI", icon: <Brain className="w-6 h-6" />, level: 85 },
  { name: "Docker/DevOps", icon: <Server className="w-6 h-6" />, level: 88 },
  { name: "RAG Systems", icon: <Layers className="w-6 h-6" />, level: 85 },
];

