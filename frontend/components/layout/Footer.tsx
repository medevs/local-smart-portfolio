"use client";

import { Coffee, Github, Linkedin, Mail } from "lucide-react";
import { Button } from "@/components/ui/button";
import { personalInfo } from "@/data/personal";

export function Footer() {
  return (
    <footer className="border-t border-amber-700/30 bg-amber-950/50 backdrop-blur-sm mt-20">
      <div className="container mx-auto px-4 py-8">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2 text-amber-200/60">
            <Coffee className="w-5 h-5 text-amber-500" />
            <span>© 2025 {personalInfo.name}. Built with Next.js & Local LLMs</span>
          </div>
          <div className="flex items-center gap-4">
            {personalInfo.github && (
              <Button
                variant="ghost"
                size="icon"
                className="text-amber-200 hover:bg-amber-900/30"
                aria-label="GitHub"
                onClick={() => window.open(personalInfo.github, '_blank')}
              >
                <Github className="w-5 h-5" />
              </Button>
            )}
            {personalInfo.linkedin && (
              <Button
                variant="ghost"
                size="icon"
                className="text-amber-200 hover:bg-amber-900/30"
                aria-label="LinkedIn"
                onClick={() => window.open(personalInfo.linkedin, '_blank')}
              >
                <Linkedin className="w-5 h-5" />
              </Button>
            )}
            <Button
              variant="ghost"
              size="icon"
              className="text-amber-200 hover:bg-amber-900/30"
              aria-label="Email"
              onClick={() => window.location.href = `mailto:${personalInfo.email}`}
            >
              <Mail className="w-5 h-5" />
            </Button>
          </div>
        </div>
      </div>
    </footer>
  );
}

