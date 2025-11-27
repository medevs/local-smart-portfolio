"use client";

import { motion } from "framer-motion";
import { Github, ExternalLink } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Project } from "@/types";

interface ProjectCardProps {
  project: Project;
  index: number;
  variant?: "compact" | "full";
}

export function ProjectCard({
  project,
  index,
  variant = "compact",
}: ProjectCardProps) {
  const imageHeight = variant === "full" ? "h-64" : "h-48";

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.3 + index * 0.1 }}
    >
      <Card className="h-full bg-gradient-to-br from-amber-950/40 to-amber-900/20 border-amber-700/30 hover:border-amber-600/50 transition-all group overflow-hidden">
        <div className={`relative ${imageHeight} overflow-hidden`}>
          <img
            src={project.image}
            alt={project.title}
            className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-amber-950 to-transparent opacity-60" />
        </div>
        <CardHeader>
          <CardTitle
            className={`text-amber-100 ${variant === "full" ? "text-2xl" : ""}`}
          >
            {project.title}
          </CardTitle>
          <CardDescription
            className={`text-amber-200/60 ${variant === "full" ? "text-base" : ""}`}
          >
            {project.description}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-2 mb-4">
            {project.tags.map((tag) => (
              <Badge
                key={tag}
                variant="secondary"
                className="bg-amber-900/30 text-amber-300 border-amber-700/50"
              >
                {tag}
              </Badge>
            ))}
          </div>
          <div className="flex gap-2">
            {project.github && (
              <Button
                size="sm"
                variant="outline"
                className="border-amber-700/50 text-amber-200 hover:bg-amber-900/30"
              >
                <Github className="w-4 h-4 mr-1" />
                {variant === "full" ? "View Code" : "Code"}
              </Button>
            )}
            {project.live && (
              <Button
                size="sm"
                className="bg-amber-700 hover:bg-amber-600 text-white"
              >
                <ExternalLink className="w-4 h-4 mr-1" />
                {variant === "full" ? "Live Demo" : "Live"}
              </Button>
            )}
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}

