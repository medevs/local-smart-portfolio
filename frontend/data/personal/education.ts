/**
 * Education history for Ahmed Oublihi
 */

export interface Education {
  institution: string;
  degree: string;
  period: string;
  location: string;
  website?: string;
  description?: string;
  certifications?: string[];
}

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

