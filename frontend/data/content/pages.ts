/**
 * Page content - titles, descriptions, and metadata for all pages
 */

export interface PageContent {
  title: string;
  description?: string;
  subtitle?: string;
}

// Home Page
export const homePageContent: PageContent = {
  title: "Featured Projects",
  description: "A collection of AI and full-stack projects showcasing local LLM deployment, RAG systems, and modern web development",
};

// Projects Page
export const projectsPageContent: PageContent = {
  title: "Projects Portfolio",
  description: "A collection of AI and full-stack projects showcasing local LLM deployment, RAG systems, and modern web development",
};

// About Page
export const aboutPageContent: PageContent = {
  title: "About Me",
  description: undefined, // Uses personalInfo.bio
};

// Contact Page
export const contactPageContent: PageContent = {
  title: "Get In Touch",
  description: "Have a project in mind or want to collaborate? I'd love to hear from you.",
};

