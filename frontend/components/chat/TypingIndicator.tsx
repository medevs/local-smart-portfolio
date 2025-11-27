"use client";

import { motion } from "framer-motion";

export function TypingIndicator() {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="flex justify-start"
    >
      <div className="bg-amber-950/50 border border-amber-700/30 rounded-lg p-3">
        <div className="flex gap-1">
          <span
            className="w-2 h-2 rounded-full bg-amber-500 animate-bounce"
            style={{ animationDelay: "0ms" }}
          />
          <span
            className="w-2 h-2 rounded-full bg-amber-500 animate-bounce"
            style={{ animationDelay: "100ms" }}
          />
          <span
            className="w-2 h-2 rounded-full bg-amber-500 animate-bounce"
            style={{ animationDelay: "200ms" }}
          />
        </div>
      </div>
    </motion.div>
  );
}

