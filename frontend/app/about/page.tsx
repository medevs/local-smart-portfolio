"use client";

import { motion } from "framer-motion";
import { User } from "lucide-react";
import { AboutCard, Timeline, TechStack } from "@/components/sections";

/**
 * About Page - Personal information and experience
 * Route: /about
 */
export default function AboutPage() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="space-y-8"
    >
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-amber-100 mb-4 flex items-center justify-center gap-3">
          <User className="w-10 h-10 text-amber-500" />
          About Me
        </h1>
        <p className="text-lg text-amber-200/70 max-w-2xl mx-auto">
          Software engineer passionate about local AI, LLMs, and building
          production-grade systems
        </p>
      </div>

      <AboutCard />
      <Timeline />
      <TechStack />
    </motion.div>
  );
}
