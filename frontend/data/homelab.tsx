import { Server, Cpu, Database, Network, Shield, Zap } from "lucide-react";
import { ReactNode } from "react";

// Homelab Overview
export interface HomelabOverview {
  hardware: string[];
  software: string[];
}

export const homelabOverview: HomelabOverview = {
  hardware: [
    "CPU: Intel Core i5 (4th Gen)",
    "RAM: 16GB DDR3",
    "Storage: 1× SSD",
    "Networking: Ethernet + Wi-Fi (TP-Link USB)",
  ],
  software: [
    "OS: Ubuntu Server 22.04 LTS",
    "Containerization: Docker & Docker Compose",
    "Reverse Proxy: Nginx Proxy Manager",
    "Monitoring: Prometheus, Grafana, cAdvisor",
  ],
};

// Journey Milestones
export interface JourneyMilestone {
  day: string;
  title: string;
  description: string;
  achievements?: string[];
  badge?: string;
}

export const journeyMilestones: JourneyMilestone[] = [
  {
    day: "Day 1-3",
    title: "Initial Setup & Docker",
    description: "Installed Ubuntu Server 22.04 LTS, configured networking, and set up Docker with Docker Compose.",
    achievements: [
      "Created first containerized app (nginx-demo)",
      "Set up SSH key-based authentication",
      "Configured projects folder structure",
    ],
  },
  {
    day: "Day 4-7",
    title: "Security Hardening",
    description: "Implemented comprehensive security measures for production-grade setup.",
    achievements: [
      "SSH key-only authentication (ED25519)",
      "Changed SSH port to 2222",
      "Configured UFW firewall",
      "Set up Fail2ban",
      "Enabled unattended upgrades",
    ],
    badge: "Security",
  },
  {
    day: "Day 8",
    title: "Monitoring Stack",
    description: "Deployed complete monitoring infrastructure with Prometheus, Grafana, and cAdvisor.",
    achievements: [
      "Prometheus metrics collection",
      "Grafana dashboards (CPU, RAM, Disk)",
      "cAdvisor container metrics",
      "Local domain configuration (grafana.local)",
    ],
    badge: "Monitoring",
  },
  {
    day: "Day 9",
    title: "Wi-Fi Migration",
    description: "Migrated from Ethernet to Wi-Fi for flexible server placement.",
    achievements: [
      "TP-Link USB Wi-Fi adapter setup",
      "NetworkManager configuration",
      "Static DHCP reservations",
      "Safe failover implementation",
    ],
  },
  {
    day: "Day 10",
    title: "Portfolio Deployment",
    description: "Fully deployed AI Portfolio application with SSL and custom domains.",
    achievements: [
      "Docker Compose deployment",
      "Nginx Proxy Manager integration",
      "SSL certificate generation (SAN)",
      "Custom domains (portfolio.medevs.local)",
    ],
    badge: "Deployment",
  },
  {
    day: "Day 11",
    title: "CI/CD Automation",
    description: "Implemented fully automated CI/CD pipeline with GitHub Actions and Watchtower.",
    achievements: [
      "GitHub Actions workflow",
      "GitHub Container Registry (GHCR)",
      "Watchtower auto-updates",
      "Zero-touch deployments",
    ],
    badge: "DevOps",
  },
];

// Services
export interface HomelabService {
  name: string;
  description: string;
  port?: string;
  icon: ReactNode;
}

export const homelabServices: HomelabService[] = [
  {
    name: "Nginx Proxy Manager",
    description: "Reverse proxy and SSL management",
    port: "80, 81, 443",
    icon: <Network className="w-5 h-5 text-amber-500" />,
  },
  {
    name: "Portainer",
    description: "Container management UI",
    icon: <Cpu className="w-5 h-5 text-amber-500" />,
  },
  {
    name: "Dashy",
    description: "Homelab dashboard",
    port: "8081",
    icon: <Server className="w-5 h-5 text-amber-500" />,
  },
  {
    name: "Prometheus",
    description: "Metrics collection and storage",
    port: "9090",
    icon: <Database className="w-5 h-5 text-amber-500" />,
  },
  {
    name: "Grafana",
    description: "Monitoring and visualization",
    port: "3000",
    icon: <Zap className="w-5 h-5 text-amber-500" />,
  },
  {
    name: "cAdvisor",
    description: "Container metrics",
    port: "8082",
    icon: <Cpu className="w-5 h-5 text-amber-500" />,
  },
  {
    name: "Ollama",
    description: "Local LLM server",
    port: "11434",
    icon: <Zap className="w-5 h-5 text-amber-500" />,
  },
  {
    name: "Watchtower",
    description: "Automatic container updates",
    icon: <Server className="w-5 h-5 text-amber-500" />,
  },
  {
    name: "Portfolio App",
    description: "This portfolio website",
    port: "3100",
    icon: <Server className="w-5 h-5 text-amber-500" />,
  },
];

// Security Features
export interface SecurityFeature {
  name: string;
  description: string;
  icon: ReactNode;
}

export const securityFeatures: SecurityFeature[] = [
  {
    name: "SSH Hardening",
    description: "Key-only authentication, custom port (2222), password disabled",
    icon: <Shield className="w-5 h-5" />,
  },
  {
    name: "Firewall (UFW)",
    description: "Configured rules for SSH, HTTP, HTTPS",
    icon: <Shield className="w-5 h-5" />,
  },
  {
    name: "Fail2ban",
    description: "Intrusion prevention and automated blocking",
    icon: <Shield className="w-5 h-5" />,
  },
  {
    name: "Auto Updates",
    description: "Unattended security updates enabled",
    icon: <Shield className="w-5 h-5" />,
  },
];

// Page Content
export interface HomelabPageContent {
  title: string;
  subtitle: string;
  overviewTitle: string;
  overviewDescription: string;
  timelineTitle: string;
  timelineDescription: string;
  servicesTitle: string;
  servicesDescription: string;
  securityTitle: string;
}

export const homelabPageContent: HomelabPageContent = {
  title: "My Homelab Journey",
  subtitle: "A comprehensive journey from zero to a production-grade homelab infrastructure with monitoring, CI/CD, and self-hosted AI systems",
  overviewTitle: "Homelab Overview",
  overviewDescription: "Complete infrastructure setup and journey",
  timelineTitle: "Journey Timeline",
  timelineDescription: "Key milestones in building the homelab",
  servicesTitle: "Services & Infrastructure",
  servicesDescription: "All services running on the homelab",
  securityTitle: "Security Hardening",
};

