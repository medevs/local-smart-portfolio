/**
 * Technical skills organized by category
 */

export interface SkillCategory {
  category: string;
  skills: string[];
}

export const skillCategories: SkillCategory[] = [
  {
    category: "Frontend Development",
    skills: [
      "JavaScript",
      "TypeScript",
      "React",
      "Next.js",
      "Material UI",
      "Tailwind CSS",
    ],
  },
  {
    category: "Backend Development",
    skills: ["Node.js", "PHP", "Python", "Express.js"],
  },
  {
    category: "Databases",
    skills: ["MySQL", "PostgreSQL", "MongoDB"],
  },
  {
    category: "APIs and Interfaces",
    skills: ["RESTful APIs", "tRPC", "WebSockets"],
  },
  {
    category: "AI Technologies",
    skills: ["Langchain", "LangGraph", "OpenAI API", "RAG"],
  },
  {
    category: "Development Tools",
    skills: ["Git", "Docker", "Jest", "Agile Methodologies"],
  },
];

