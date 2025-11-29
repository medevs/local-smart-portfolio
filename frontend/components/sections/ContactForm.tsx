"use client";

import { motion } from "framer-motion";
import { Send, Github, Linkedin, Mail, FileText } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { personalInfo } from "@/data/personal";

export function ContactForm() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <motion.div
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: 0.1 }}
      >
        <Card className="h-full bg-gradient-to-br from-amber-950/40 to-amber-900/20 border-amber-700/30">
          <CardHeader>
            <CardTitle className="text-amber-100">Send a Message</CardTitle>
            <CardDescription className="text-amber-200/60">
              Fill out the form and I&apos;ll get back to you soon
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="text-sm font-medium text-amber-200 mb-2 block">
                Name
              </label>
              <Input
                placeholder="Your name"
                className="bg-amber-950/30 border-amber-700/50 text-amber-100 placeholder:text-amber-400/50"
              />
            </div>
            <div>
              <label className="text-sm font-medium text-amber-200 mb-2 block">
                Email
              </label>
              <Input
                type="email"
                placeholder="your.email@example.com"
                className="bg-amber-950/30 border-amber-700/50 text-amber-100 placeholder:text-amber-400/50"
              />
            </div>
            <div>
              <label className="text-sm font-medium text-amber-200 mb-2 block">
                Message
              </label>
              <Textarea
                placeholder="Your message..."
                rows={5}
                className="bg-amber-950/30 border-amber-700/50 text-amber-100 placeholder:text-amber-400/50"
              />
            </div>
            <Button className="w-full bg-amber-700 hover:bg-amber-600 text-white">
              <Send className="w-4 h-4 mr-2" />
              Send Message
            </Button>
          </CardContent>
        </Card>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: 0.2 }}
        className="space-y-6"
      >
        <Card className="bg-gradient-to-br from-amber-950/40 to-amber-900/20 border-amber-700/30">
          <CardHeader>
            <CardTitle className="text-amber-100">Connect With Me</CardTitle>
            <CardDescription className="text-amber-200/60">
              Find me on these platforms
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            <Button
              variant="outline"
              className="w-full justify-start border-amber-700/50 text-amber-200 hover:bg-amber-900/30"
            >
              <Github className="w-5 h-5 mr-3" />
              GitHub
            </Button>
            <Button
              variant="outline"
              className="w-full justify-start border-amber-700/50 text-amber-200 hover:bg-amber-900/30"
            >
              <Linkedin className="w-5 h-5 mr-3" />
              LinkedIn
            </Button>
            <Button
              variant="outline"
              className="w-full justify-start border-amber-700/50 text-amber-200 hover:bg-amber-900/30"
              onClick={() => window.location.href = `mailto:${personalInfo.email}`}
            >
              <Mail className="w-5 h-5 mr-3" />
              {personalInfo.email}
            </Button>
            <Button
              variant="outline"
              className="w-full justify-start border-amber-700/50 text-amber-200 hover:bg-amber-900/30"
            >
              <FileText className="w-5 h-5 mr-3" />
              Resume
            </Button>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-amber-950/40 to-amber-900/20 border-amber-700/30">
          <CardHeader>
            <CardTitle className="text-amber-100">
              Location & Availability
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3 text-amber-200/80">
            <p className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-green-500" />
              Available for opportunities
            </p>
            <p>{personalInfo.location}</p>
            <p>Phone: {personalInfo.phone}</p>
            <p>Email: {personalInfo.email}</p>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}

