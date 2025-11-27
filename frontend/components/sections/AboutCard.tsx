"use client";

import { motion } from "framer-motion";
import { Brain, Server, Code, TrendingUp } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";

const quickFacts = [
  {
    icon: <Brain className="w-5 h-5 text-amber-500 mt-1" />,
    title: "AI Specialist",
    subtitle: "Local LLMs & RAG",
  },
  {
    icon: <Server className="w-5 h-5 text-amber-500 mt-1" />,
    title: "DevOps Expert",
    subtitle: "Docker, K8s, CI/CD",
  },
  {
    icon: <Code className="w-5 h-5 text-amber-500 mt-1" />,
    title: "Full Stack Dev",
    subtitle: "React, Next.js, Python",
  },
  {
    icon: <TrendingUp className="w-5 h-5 text-amber-500 mt-1" />,
    title: "Always Learning",
    subtitle: "Latest AI trends",
  },
];

export function AboutCard() {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <motion.div
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: 0.1 }}
        className="lg:col-span-2"
      >
        <Card className="h-full bg-gradient-to-br from-amber-950/40 to-amber-900/20 border-amber-700/30">
          <CardHeader>
            <CardTitle className="text-amber-100 text-2xl">My Journey</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4 text-amber-200/80">
            <p>
              I&apos;m a software engineer specializing in local AI deployment and
              LLM infrastructure. My passion lies in building production-grade
              systems that leverage the power of large language models while
              maintaining full control over data privacy and deployment.
            </p>
            <p>
              With a strong foundation in full-stack development and DevOps,
              I&apos;ve evolved into the AI/ML space, focusing on RAG systems,
              vector databases, and efficient model serving. My homelab serves as
              both a learning environment and a production platform for
              experimenting with cutting-edge AI technologies.
            </p>
            <p>
              I believe in the power of self-hosted solutions and open-source
              technologies. My work demonstrates that enterprise-grade AI systems
              can be built and deployed locally, offering better privacy, control,
              and cost-efficiency.
            </p>
          </CardContent>
        </Card>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: 0.2 }}
      >
        <Card className="h-full bg-gradient-to-br from-amber-950/40 to-amber-900/20 border-amber-700/30">
          <CardHeader>
            <CardTitle className="text-amber-100">Quick Facts</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {quickFacts.map((fact, index) => (
              <div key={fact.title}>
                <div className="flex items-start gap-3">
                  {fact.icon}
                  <div>
                    <p className="font-medium text-amber-100">{fact.title}</p>
                    <p className="text-sm text-amber-200/60">{fact.subtitle}</p>
                  </div>
                </div>
                {index < quickFacts.length - 1 && (
                  <Separator className="bg-amber-800/30 mt-4" />
                )}
              </div>
            ))}
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}

