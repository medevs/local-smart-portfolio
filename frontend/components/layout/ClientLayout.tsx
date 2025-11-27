"use client";

import { useState } from "react";
import { Header } from "./Header";
import { Footer } from "./Footer";
import { ChatWidget, ChatFloatingButton } from "@/components/chat";

interface ClientLayoutProps {
  children: React.ReactNode;
}

/**
 * Client-side layout wrapper that handles:
 * - Header with navigation
 * - Footer
 * - Chat widget state
 * 
 * This wraps the page content and provides consistent layout across all pages.
 */
export function ClientLayout({ children }: ClientLayoutProps) {
  const [isChatOpen, setIsChatOpen] = useState(false);

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-950 via-black to-amber-900 text-white">
      {/* Header Navigation */}
      <Header onChatOpen={() => setIsChatOpen(true)} />

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {children}
      </main>

      {/* Footer */}
      <Footer />

      {/* Chat Widget */}
      <ChatWidget isOpen={isChatOpen} onClose={() => setIsChatOpen(false)} />

      {/* Floating Chat Button (when chat is closed) */}
      {!isChatOpen && (
        <ChatFloatingButton onClick={() => setIsChatOpen(true)} />
      )}
    </div>
  );
}

