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
    "Networking: Wi-Fi (TP-Link TL-WN821N v5/v6) + Ethernet fallback",
    "GPU: None (CPU-only inference)",
  ],
  software: [
    "OS: Ubuntu Server 22.04 LTS",
    "Containerization: Docker & Docker Compose",
    "Reverse Proxy: Nginx Proxy Manager",
    "Monitoring: Prometheus, Grafana, cAdvisor",
    "CI/CD: GitHub Actions + GHCR",
    "LLM: Ollama (local models)",
    "Vector DB: ChromaDB",
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
    day: "Day 1",
    title: "Ubuntu Server Installation & Initial Setup",
    description: "Installed Ubuntu Server 22.04 LTS on an old PC converted to a server. Chose server edition for better resource allocation and to force command-line learning. Installed essential tools: git, python3, htop, neofetch, and net-tools.",
    achievements: [
      "Installed Ubuntu Server 22.04 LTS",
      "Set up essential development tools",
      "First login via keyboard and monitor",
      "System update and package installation",
    ],
  },
  {
    day: "Day 2",
    title: "Networking Troubleshooting & Netplan Configuration",
    description: "Encountered major networking issues - no IP address, no DHCP, no connectivity. Troubleshot step-by-step and fixed Netplan configuration to enable proper DHCP and internet connectivity.",
    achievements: [
      "Fixed Netplan configuration",
      "Resolved DHCP issues",
      "Restored internet connectivity",
      "Fixed Netplan permissions warnings",
    ],
  },
  {
    day: "Day 3",
    title: "SSH Setup & Docker Installation",
    description: "Successfully connected from main PC via SSH, making workflow much easier. Installed Docker correctly following official documentation, verified with hello-world container, and set up Docker Compose.",
    achievements: [
      "SSH connection from main PC",
      "Created projects folder structure",
      "Installed Docker Engine and Docker Compose",
      "Verified Docker installation",
      "Created first containerized app (nginx-demo)",
    ],
  },
  {
    day: "Day 4-7",
    title: "Security Hardening",
    description: "Implemented comprehensive security measures for production-grade setup. Hardened SSH, configured firewall, and set up intrusion prevention.",
    achievements: [
      "Generated ED25519 SSH key pair",
      "SSH key-only authentication enabled",
      "Password authentication disabled",
      "Changed SSH port to 2222",
      "Configured UFW firewall rules",
      "Set up Fail2ban for intrusion prevention",
      "Enabled unattended security updates",
    ],
    badge: "Security",
  },
  {
    day: "Day 8",
    title: "Monitoring Stack - Prometheus, Grafana & cAdvisor",
    description: "Deployed complete monitoring infrastructure. Created Grafana dashboards for CPU, RAM, and Disk usage. Configured local domain access through Nginx Proxy Manager.",
    achievements: [
      "Verified Prometheus + cAdvisor metrics",
      "Created CPU usage dashboard (PromQL)",
      "Created RAM usage dashboard",
      "Created Disk usage dashboard",
      "Configured local domain (grafana.local)",
      "Nginx Proxy Manager integration",
    ],
    badge: "Monitoring",
  },
  {
    day: "Day 9",
    title: "Wi-Fi Migration & NetworkManager",
    description: "Migrated from Ethernet to Wi-Fi using TP-Link USB adapter for flexible server placement. Configured NetworkManager, set up safe failover, and configured static DHCP reservations.",
    achievements: [
      "TP-Link USB Wi-Fi adapter detection",
      "NetworkManager installation and configuration",
      "Wi-Fi connection to FRITZ!Box",
      "Route metric optimization (Wi-Fi primary)",
      "Static DHCP reservations configured",
      "Safe failover implementation",
      "Server moved to kitchen location",
    ],
  },
  {
    day: "Day 10",
    title: "Portfolio Application Deployment",
    description: "Fully deployed AI Portfolio application stack (Frontend, Backend, Ollama) with SSL certificates and custom domains. Resolved CORS, environment variables, and Nginx Proxy Manager configuration.",
    achievements: [
      "Docker Compose deployment",
      "Backend health verification",
      "Fixed CORS configuration",
      "Nginx Proxy Manager integration",
      "Generated SAN SSL certificates",
      "Custom domains configured (portfolio.medevs.local)",
      "HTTPS with self-signed certificates",
      "Admin dashboard fully functional",
    ],
    badge: "Deployment",
  },
  {
    day: "Day 11",
    title: "CI/CD Automation with GitHub Actions",
    description: "Implemented fully automated CI/CD pipeline. GitHub Actions builds Docker images and pushes to GHCR for deployment.",
    achievements: [
      "GitHub Actions workflow created",
      "Docker images built automatically",
      "GitHub Container Registry (GHCR) setup",
      "Server authentication to GHCR",
      "Docker Compose updated to use GHCR images",
      "Automated deployment pipeline",
    ],
    badge: "DevOps",
  },
  {
    day: "Day 12",
    title: "Stabilization & Production Hardening",
    description: "Fixed CI/CD deployment issues, resolved CORS and DNS problems, synced server code with GitHub, and cleaned up Docker environment. Achieved production-grade stability.",
    achievements: [
      "GitHub-server code synchronization",
      "Fixed frontend port conflicts",
      "Resolved DNS resolution issues",
      "Validated CORS configuration",
      "Rebuilt frontend with correct API URL",
      "Docker disk cleanup and optimization",
      "Automated maintenance cron jobs",
      "Production-grade stability achieved",
    ],
    badge: "Production",
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
    name: "Portfolio App",
    description: "This portfolio website (Frontend + Backend)",
    port: "3000",
    icon: <Server className="w-5 h-5 text-amber-500" />,
  },
  {
    name: "Portfolio Backend API",
    description: "FastAPI backend with RAG and Ollama",
    port: "8000",
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
  subtitle: "A comprehensive journey from zero to a production-grade homelab infrastructure. From Ubuntu Server installation to full CI/CD automation, monitoring, and self-hosted AI systems. Every step documented, every problem solved.",
  overviewTitle: "Homelab Overview",
  overviewDescription: "Complete infrastructure setup - hardware, software stack, and services running 24/7",
  timelineTitle: "Journey Timeline",
  timelineDescription: "12 days of intensive learning, troubleshooting, and building. From networking issues to production-grade deployment.",
  servicesTitle: "Services & Infrastructure",
  servicesDescription: "All services running on the homelab - monitoring, reverse proxy, CI/CD, and AI applications",
  securityTitle: "Security Hardening",
};

