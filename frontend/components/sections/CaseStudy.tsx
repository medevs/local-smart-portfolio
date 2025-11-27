"use client";

import { motion } from "framer-motion";
import { Shield, ChevronRight } from "lucide-react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

const infrastructure = [
  "Docker containerization for all services",
  "Traefik reverse proxy with SSL",
  "Prometheus + Grafana monitoring",
  "Ollama for LLM serving",
];

const security = [
  "UFW firewall configuration",
  "SSH hardening with key-based auth",
  "Fail2ban for intrusion prevention",
  "Regular security audits",
];

export function CaseStudy() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.4 }}
    >
      <Card className="bg-gradient-to-br from-amber-950/40 to-amber-900/20 border-amber-700/30">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-amber-100 text-2xl">
            <Shield className="w-6 h-6 text-amber-500" />
            Case Study: Local AI Deployment
          </CardTitle>
          <CardDescription className="text-amber-200/60">
            Building a production-grade homelab for LLM inference
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-amber-100">
                Infrastructure
              </h3>
              <ul className="space-y-2 text-amber-200/80">
                {infrastructure.map((item) => (
                  <li key={item} className="flex items-start gap-2">
                    <ChevronRight className="w-4 h-4 mt-1 text-amber-500" />
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-amber-100">Security</h3>
              <ul className="space-y-2 text-amber-200/80">
                {security.map((item) => (
                  <li key={item} className="flex items-start gap-2">
                    <ChevronRight className="w-4 h-4 mt-1 text-amber-500" />
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}

