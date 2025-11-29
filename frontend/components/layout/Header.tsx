"use client";

import { motion } from "framer-motion";
import { MessageSquare } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Button } from "@/components/ui/button";

interface HeaderProps {
  onChatOpen: () => void;
}

const navItems = [
  { href: "/", label: "Home" },
  { href: "/projects", label: "Projects" },
  { href: "/about", label: "About" },
  { href: "/homelab", label: "Homelab" },
  { href: "/contact", label: "Contact" },
  { href: "/admin", label: "Admin" },
];

export function Header({ onChatOpen }: HeaderProps) {
  const pathname = usePathname();

  return (
    <nav className="sticky top-0 z-40 backdrop-blur-lg bg-amber-950/80 border-b border-amber-700/30">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex items-center gap-2"
          >
            <Link href="/" className="flex items-center gap-2">
              <img 
                src="/logo.svg" 
                alt="Local AI/LLM Specialist Logo" 
                className="w-10 h-10"
              />
              <span className="text-xl font-bold text-amber-100">
                Ahmed Oublihi
              </span>
            </Link>
          </motion.div>

          {/* Navigation Links */}
          <div className="hidden md:flex items-center gap-1">
            {navItems.map((item) => {
              const isActive = pathname === item.href;
              return (
                <Link key={item.href} href={item.href}>
                  <Button
                    variant={isActive ? "default" : "ghost"}
                    className={
                      isActive
                        ? "bg-amber-700 text-white hover:bg-amber-600"
                        : "text-amber-200 hover:bg-amber-900/30"
                    }
                  >
                    {item.label}
                  </Button>
                </Link>
              );
            })}
          </div>

          {/* Chat Button */}
          <Button
            size="sm"
            className="bg-amber-700 hover:bg-amber-600 text-white"
            onClick={onChatOpen}
          >
            <MessageSquare className="w-4 h-4 mr-2" />
            AI Chat
          </Button>
        </div>
      </div>
    </nav>
  );
}
