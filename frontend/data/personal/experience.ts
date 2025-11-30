/**
 * Professional experience for Ahmed Oublihi
 */

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

