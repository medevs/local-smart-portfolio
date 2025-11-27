"use client";

import { Metadata } from "next";
import { motion } from "framer-motion";
import { Code2 } from "lucide-react";
import {
  Hero,
  SkillsCard,
  SystemMetricsCard,
  ProjectCard,
  BenchmarksCard,
} from "@/components/sections";
import { projects } from "@/data/projects";

/**
 * Home Page - Main landing page of the portfolio
 * Route: /
 */
export default function HomePage() {
  // Show only first 2 projects on home page
  const featuredProjects = projects.slice(0, 2);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="space-y-8"
    >
      <Hero />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <SkillsCard />
        <SystemMetricsCard />
      </div>

      <section>
        <h2 className="text-3xl font-bold text-amber-100 mb-6 flex items-center gap-2">
          <Code2 className="w-8 h-8 text-amber-500" />
          Featured Projects
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {featuredProjects.map((project, index) => (
            <ProjectCard key={project.title} project={project} index={index} />
          ))}
        </div>
      </section>

      <BenchmarksCard />
    </motion.div>
  );
}
