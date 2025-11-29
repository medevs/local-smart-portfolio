// Case Study Data
export interface CaseStudyData {
  title: string;
  description: string;
  infrastructure: string[];
  security: string[];
}

export const caseStudyData: CaseStudyData = {
  title: "Case Study: Local AI Deployment",
  description: "Building a production-grade homelab for LLM inference",
  infrastructure: [
    "Docker containerization for all services",
    "Nginx Proxy Manager reverse proxy with SSL",
    "Prometheus + Grafana monitoring",
    "Ollama for LLM serving",
  ],
  security: [
    "UFW firewall configuration",
    "SSH hardening with key-based auth",
    "Fail2ban for intrusion prevention",
    "Regular security audits",
  ],
};

