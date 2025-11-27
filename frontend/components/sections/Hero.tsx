"use client";

import { motion } from "framer-motion";
import { Coffee, Download, ChevronRight, Terminal } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useTerminalAnimation } from "@/hooks";

const TERMINAL_TEXT = `> Initializing AI Portfolio...
> Loading LLM Models...
> System Ready ✓`;

export function Hero() {
  const { displayText, showCursor } = useTerminalAnimation({
    text: TERMINAL_TEXT,
  });

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-amber-900/20 via-amber-800/10 to-amber-950/20 border border-amber-700/30 p-12"
    >
      <div className="pattern-grid absolute inset-0 opacity-30" />

      <div className="relative z-10">
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-amber-900/30 border border-amber-700/50 mb-6"
        >
          <Coffee className="w-4 h-4 text-amber-500" />
          <span className="text-sm text-amber-200">
            Available for opportunities
          </span>
        </motion.div>

        <h1 className="text-5xl md:text-7xl font-bold mb-4 bg-gradient-to-r from-amber-200 via-amber-100 to-amber-300 bg-clip-text text-transparent">
          Software Engineer
        </h1>
        <p className="text-2xl md:text-3xl text-amber-200/80 mb-6">
          Local AI & LLM Specialist
        </p>
        <p className="text-lg text-amber-100/60 max-w-2xl mb-8">
          Building intelligent systems with self-hosted LLMs, RAG architectures,
          and production-grade AI infrastructure
        </p>

        <div className="flex flex-wrap gap-4">
          <Button
            size="lg"
            className="bg-amber-700 hover:bg-amber-600 text-white"
          >
            <Download className="w-4 h-4 mr-2" />
            Download Resume
          </Button>
          <Button
            size="lg"
            variant="outline"
            className="border-amber-700/50 text-amber-200 hover:bg-amber-900/30"
          >
            View Projects
            <ChevronRight className="w-4 h-4 ml-2" />
          </Button>
        </div>
      </div>

      {/* Terminal Animation */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.5 }}
        className="mt-8 bg-black/40 backdrop-blur-sm rounded-lg p-4 border border-amber-700/30 font-mono text-sm"
      >
        <div className="flex items-center gap-2 mb-2">
          <Terminal className="w-4 h-4 text-amber-500" />
          <span className="text-amber-400">system@ai-portfolio</span>
        </div>
        <pre className="text-amber-200/80 whitespace-pre-wrap">
          {displayText}
          {showCursor && <span className="text-amber-500">▊</span>}
        </pre>
      </motion.div>
    </motion.div>
  );
}

