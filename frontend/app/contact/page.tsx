"use client";

import { motion } from "framer-motion";
import { Mail } from "lucide-react";
import { ContactForm } from "@/components/sections";

/**
 * Contact Page - Contact form and social links
 * Route: /contact
 */
export default function ContactPage() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="space-y-8"
    >
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-amber-100 mb-4 flex items-center justify-center gap-3">
          <Mail className="w-10 h-10 text-amber-500" />
          Get In Touch
        </h1>
        <p className="text-lg text-amber-200/70 max-w-2xl mx-auto">
          Have a project in mind or want to discuss AI infrastructure? I&apos;d
          love to hear from you
        </p>
      </div>

      <ContactForm />
    </motion.div>
  );
}
