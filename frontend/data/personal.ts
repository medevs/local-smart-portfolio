/**
 * Personal information and professional data for Ahmed Oublihi
 * Based on actual resume (ahmed-resume.pdf)
 */

export interface PersonalInfo {
  name: string;
  title: string;
  bio: string;
  location?: string;
  email?: string;
  phone?: string;
  website?: string;
  github?: string;
  linkedin?: string;
  twitter?: string;
}

export interface Experience {
  company: string;
  role: string;
  period: string;
  location: string;
  website?: string;
  description: string;
  technologies: string[];
  achievements?: string[];
}

export interface Education {
  institution: string;
  degree: string;
  period: string;
  location: string;
  website?: string;
  description?: string;
  certifications?: string[];
}

export interface Project {
  title: string;
  year: string;
  description: string;
  url: string;
  technologies: string[];
  features?: string[];
}

export interface Certification {
  name: string;
  issuer: string;
  date: string;
  description?: string;
  credentialId?: string;
  link?: string;
}

// Personal Information
export const personalInfo: PersonalInfo = {
  name: "Ahmed Oublihi",
  title: "Software Engineer | Local AI/LLM Specialist",
  bio: "I help founders build production-ready AI systems with self-hosted LLMs, reducing costs by up to 90% while maintaining complete data privacy and control. Specialized in Local AI deployment, RAG systems, and modern web applications that deliver enterprise-grade performance without vendor lock-in.",
  location: "Pommernstraße 17, 27749 Delmenhorst, Germany",
  email: "oublihi.a@gmail.com",
  phone: "+49 157 51239715",
  website: "https://ahmed-oublihi.vercel.app",
  github: "https://github.com/medevs",
  linkedin: undefined,
  twitter: undefined,
};

// Professional Experience
export const experiences: Experience[] = [
  {
    company: "ePhilos AG",
    role: "Full Stack Entwickler",
    period: "May 2024 – June 2025",
    location: "Bremen, Germany",
    website: "https://ephilos.de",
    description:
      "Further development and optimization of the enterprise software Comfortmarkt with PHP, MySQL, and JavaScript. Implementation of new features and improvement of user experience.",
    technologies: ["PHP", "MySQL", "JavaScript", "WebSockets"],
    achievements: [
      "WebSocket implementation for optimal real-time search and system notifications",
      "Code refactoring and improvement of code quality",
      "Code reviews and mentoring of apprentices",
    ],
  },
  {
    company: "ePhilos AG",
    role: "Auszubildender Fachinformatiker",
    period: "Aug. 2021 – May 2024",
    location: "Bremen, Germany",
    website: "https://ephilos.de",
    description:
      "Dual apprenticeship with focus on Full Stack Development. Active participation in agile development teams.",
    technologies: ["PHP", "JavaScript", "MySQL", "Agile Methodologies"],
    achievements: [
      "Completed professional training in application development (IHK)",
      "Worked in agile development teams",
      "Gained hands-on experience in enterprise software development",
    ],
  },
  {
    company: "Freiberufliche Tätigkeit",
    role: "Webentwickler",
    period: "March 2020 – June 2021",
    location: "Remote, Morocco",
    description:
      "Development of responsive websites for local businesses and tourism providers. SEO optimization and improvement of search engine rankings.",
    technologies: ["HTML5", "CSS3", "Bootstrap", "jQuery", "WordPress"],
    achievements: [
      "Developed responsive websites for local businesses",
      "SEO optimization and search engine ranking improvements",
      "Worked with WordPress and modern web technologies",
    ],
  },
  {
    company: "HM Communication",
    role: "Node.js Entwickler (Praktikum)",
    period: "July 2019 – Sep. 2019",
    location: "Marrakech, Morocco",
    description:
      "Development of web applications with Node.js, Express.js, and MongoDB. Implementation of RESTful APIs for mobile and web-based applications.",
    technologies: ["Node.js", "Express.js", "MongoDB", "RESTful APIs"],
    achievements: [
      "Developed web applications with Node.js and Express.js",
      "Implemented RESTful APIs for mobile and web applications",
      "Worked with MongoDB database systems",
    ],
  },
];

// Education
export const education: Education[] = [
  {
    institution: "Schulzentrum SII Utbremen",
    degree: "Fachinformatiker für Anwendungsentwicklung (IHK)",
    period: "Aug. 2021 – May 2024",
    location: "Bremen, Germany",
    website: "https://www.szut.de/",
    description:
      "Development of applications with Java, TypeScript, and Angular. Design and implementation of database solutions and system integration.",
    certifications: [
      "Final project: Development of a modular WebSocket system for real-time functionality",
    ],
  },
  {
    institution: "ESMA",
    degree: "Bachelor in Networks and Telecommunications",
    period: "Oct. 2018 – Nov. 2019",
    location: "Marrakech, Morocco",
    website: "https://esmamaroc.ma/",
    description:
      "Study of network administration, IT security, and telecommunications systems.",
    certifications: ["CISCO Certifications CCNA1-CCNA4"],
  },
  {
    institution: "OFPPT",
    degree: "Technician in Software Development",
    period: "Sep. 2016 – July 2018",
    location: "Ouarzazate, Morocco",
    website: "https://www.ofppt.ma/",
    description:
      "Fundamentals of programming, web development, and database management.",
  },
];

// Projects
export const personalProjects: Project[] = [
  {
    title: "TalkTheDoc",
    year: "2025",
    description:
      "AI application for real-time communication with document contents. Voice and text-based app for natural real-time communication with documents using Retrieval-Augmented Generation (RAG) for fast and context-accurate answers.",
    url: "https://talkthedoc.com",
    technologies: ["Convex", "Next.js", "TypeScript", "AI SDK", "RAG"],
    features: [
      "Real-time document communication",
      "Retrieval-Augmented Generation (RAG) for fast and context-accurate answers",
      "Voice and text-based interface",
    ],
  },
  {
    title: "Docspresso",
    year: "2025",
    description:
      "AI application for automated creation of technical documentation. Systematically generates PRDs, architecture plans, and technical specifications. Developed to support AI Coding Agents during app development.",
    url: "https://docspresso.dev",
    technologies: ["Langchain", "Next.js", "PostgreSQL", "tRPC", "TypeScript"],
    features: [
      "Automated technical documentation generation",
      "Supports AI Coding Agents during app development",
      "Systematic generation of PRDs and architecture plans",
    ],
  },
  {
    title: "Your Daily Way",
    year: "2024",
    description:
      "SEO-optimized blog with 100% Google PageSpeed Score. Markdown-based CMS with focus on maximum performance and user-friendliness.",
    url: "http://yourdailyway.com/",
    technologies: ["Astro", "React", "TypeScript", "MDX"],
    features: [
      "100% Google PageSpeed Score",
      "Markdown-based CMS",
      "Maximum performance optimization",
    ],
  },
];

// Certifications
export const certifications: Certification[] = [
  {
    name: "Microsoft Certified Professional",
    issuer: "Microsoft",
    date: "May 2018",
    description: "Web Development: HTML5, CSS3, JavaScript",
  },
];

// Languages
export interface Language {
  name: string;
  level: string;
}

export const languages: Language[] = [
  { name: "German", level: "Very Good (Sehr gute Kenntnisse)" },
  { name: "English", level: "Good (Gute Kenntnisse)" },
  { name: "French", level: "Basic (Grundkenntnisse)" },
  { name: "Tamazight (Berberisch)", level: "Native (Muttersprache)" },
  { name: "Arabic", level: "Native (Muttersprache)" },
];

// Skills (organized by category)
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

// Interests
export const interests: string[] = [
  "AI Agents and Machine Learning",
  "Software Architecture",
  "Open-Source Development",
];

