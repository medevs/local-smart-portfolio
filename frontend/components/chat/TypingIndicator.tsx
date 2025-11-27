"use client";

import { motion } from "framer-motion";
import { Loader2 } from "lucide-react";

export function TypingIndicator() {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="flex justify-start"
    >
      <div className="bg-amber-950/50 border border-amber-700/30 rounded-lg p-3">
        <div className="flex items-center gap-2 text-amber-300">
          <Loader2 className="w-4 h-4 animate-spin" />
          <span className="text-sm">Thinking...</span>
        </div>
      </div>
    </motion.div>
  );
}

