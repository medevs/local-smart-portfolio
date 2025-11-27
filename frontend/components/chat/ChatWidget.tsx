"use client";

import { motion, AnimatePresence } from "framer-motion";
import { X, MessageSquare } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { useChat } from "@/hooks";
import { ChatMessage } from "./ChatMessage";
import { ChatInput } from "./ChatInput";
import { TypingIndicator } from "./TypingIndicator";

interface ChatWidgetProps {
  isOpen: boolean;
  onClose: () => void;
}

export function ChatWidget({ isOpen, onClose }: ChatWidgetProps) {
  const {
    messages,
    inputMessage,
    setInputMessage,
    isTyping,
    sendMessage,
    messagesEndRef,
  } = useChat();

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0, y: 100, scale: 0.9 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: 100, scale: 0.9 }}
          className="fixed bottom-6 right-6 w-96 h-[600px] z-50"
        >
          <Card className="h-full flex flex-col bg-gradient-to-br from-amber-950 to-amber-900 border-amber-700/50 shadow-2xl">
            <CardHeader className="border-b border-amber-700/30">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                  <CardTitle className="text-amber-100">
                    AI Assistant
                  </CardTitle>
                </div>
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={onClose}
                  className="text-amber-200 hover:bg-amber-900/30"
                  aria-label="Close chat"
                >
                  <X className="w-4 h-4" />
                </Button>
              </div>
              <CardDescription className="text-amber-200/60">
                Powered by local LLM
              </CardDescription>
            </CardHeader>

            <ScrollArea className="flex-1 p-4">
              <div className="space-y-4">
                {messages.map((message, index) => (
                  <ChatMessage key={index} message={message} index={index} />
                ))}
                {isTyping && <TypingIndicator />}
                <div ref={messagesEndRef} />
              </div>
            </ScrollArea>

            <ChatInput
              value={inputMessage}
              onChange={setInputMessage}
              onSend={sendMessage}
              disabled={isTyping}
            />
          </Card>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

// Floating button component for when chat is closed
export function ChatFloatingButton({ onClick }: { onClick: () => void }) {
  return (
    <motion.div
      initial={{ scale: 0 }}
      animate={{ scale: 1 }}
      className="fixed bottom-6 right-6 z-40"
    >
      <Button
        size="lg"
        onClick={onClick}
        className="rounded-full w-14 h-14 bg-amber-700 hover:bg-amber-600 text-white shadow-lg"
        aria-label="Open chat"
      >
        <MessageSquare className="w-6 h-6" />
      </Button>
    </motion.div>
  );
}

