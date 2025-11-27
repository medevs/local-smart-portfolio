"use client";

import { motion } from "framer-motion";
import { Home, ArrowLeft, Search } from "lucide-react";
import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function NotFoundPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-950 via-black to-amber-900 flex items-center justify-center p-4">
      <div className="text-center space-y-8 max-w-md mx-auto">
        {/* Animated 404 */}
        <motion.div
          initial={{ scale: 0, rotate: -180 }}
          animate={{ scale: 1, rotate: 0 }}
          transition={{
            type: "spring",
            stiffness: 200,
            damping: 20,
            duration: 0.8
          }}
          className="relative"
        >
          <div className="text-8xl md:text-9xl font-bold text-amber-500/20 select-none">
            404
          </div>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="absolute inset-0 flex items-center justify-center"
          >
            <Search className="w-12 h-12 md:w-16 md:h-16 text-amber-400" />
          </motion.div>
        </motion.div>

        {/* Content */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="space-y-4"
        >
          <h1 className="text-3xl md:text-4xl font-bold text-amber-100">
            Page Not Found
          </h1>
          <p className="text-lg text-amber-200/70 leading-relaxed">
            Looks like this page got lost in the digital void. The page you&apos;re looking for doesn&apos;t exist or has been moved.
          </p>
        </motion.div>

        {/* Action Buttons */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="flex flex-col sm:flex-row gap-4 justify-center"
        >
          <Link href="/">
            <Button
              size="lg"
              className="bg-amber-700 hover:bg-amber-600 text-white px-8 py-3 text-lg font-medium transition-all duration-200 hover:scale-105"
            >
              <Home className="w-5 h-5 mr-2" />
              Go Home
            </Button>
          </Link>

          <Button
            variant="outline"
            size="lg"
            onClick={() => window.history.back()}
            className="border-amber-700/50 text-amber-200 hover:bg-amber-900/30 px-8 py-3 text-lg font-medium transition-all duration-200 hover:scale-105"
          >
            <ArrowLeft className="w-5 h-5 mr-2" />
            Go Back
          </Button>
        </motion.div>

        {/* Additional Help */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.9 }}
          className="pt-8 border-t border-amber-800/30"
        >
          <p className="text-sm text-amber-300/50 mb-4">
            Try one of these instead:
          </p>
          <div className="flex flex-wrap justify-center gap-2 text-sm">
            <Link
              href="/"
              className="text-amber-400 hover:text-amber-300 transition-colors underline underline-offset-4"
            >
              Home
            </Link>
            <span className="text-amber-600/50">•</span>
            <Link
              href="/projects"
              className="text-amber-400 hover:text-amber-300 transition-colors underline underline-offset-4"
            >
              Projects
            </Link>
            <span className="text-amber-600/50">•</span>
            <Link
              href="/about"
              className="text-amber-400 hover:text-amber-300 transition-colors underline underline-offset-4"
            >
              About
            </Link>
            <span className="text-amber-600/50">•</span>
            <Link
              href="/contact"
              className="text-amber-400 hover:text-amber-300 transition-colors underline underline-offset-4"
            >
              Contact
            </Link>
          </div>
        </motion.div>

        {/* Subtle background effect */}
        <div className="absolute inset-0 -z-10 overflow-hidden">
          <div className="absolute top-1/4 left-1/4 w-64 h-64 bg-amber-500/5 rounded-full blur-3xl animate-pulse" />
          <div className="absolute bottom-1/4 right-1/4 w-48 h-48 bg-amber-400/5 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }} />
        </div>
      </div>
    </div>
  );
}
