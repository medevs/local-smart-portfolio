/**
 * Personal information for Ahmed Oublihi
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

