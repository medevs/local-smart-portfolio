"use client";

import { motion } from "framer-motion";
import { Code2 } from "lucide-react";
import { ProjectCard, CaseStudy, BenchmarksCard } from "@/components/sections";
import { projects } from "@/data/projects";
import { projectsPageContent } from "@/data/pageContent";

// Note: metadata must be in a separate file or use generateMetadata for client components
// For now, metadata is set in layout or can use generateMetadata

/**
 * Projects Page - Showcase of all projects
 * Route: /projects
 */
export default function ProjectsPage() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="space-y-8"
    >
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-amber-100 mb-4 flex items-center justify-center gap-3">
          <Code2 className="w-10 h-10 text-amber-500" />
          {projectsPageContent.title}
        </h1>
        <p className="text-lg text-amber-200/70 max-w-2xl mx-auto">
          {projectsPageContent.description}
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {projects.map((project, index) => (
          <ProjectCard
            key={project.title}
            project={project}
            index={index}
            variant="full"
          />
        ))}
      </div>

      <CaseStudy />
      <BenchmarksCard />
    </motion.div>
  );
}
