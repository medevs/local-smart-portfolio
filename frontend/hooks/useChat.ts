/**
 * Custom hook for chat functionality with streaming support.
 */

import { useState, useRef, useEffect, useCallback } from "react";
import { ChatMessage } from "@/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface UseChatOptions {
  initialMessages?: ChatMessage[];
  maxHistory?: number;
}

interface UseChatReturn {
  messages: ChatMessage[];
  inputMessage: string;
  setInputMessage: (message: string) => void;
  isTyping: boolean;
  sendMessage: () => Promise<void>;
  messagesEndRef: React.RefObject<HTMLDivElement | null>;
  clearMessages: () => void;
}

export function useChat({
  initialMessages = [],
  maxHistory = 10,
}: UseChatOptions = {}): UseChatReturn {
  const [messages, setMessages] = useState<ChatMessage[]>(initialMessages);
  const [isInitialized, setIsInitialized] = useState(false);

  // Initialize with welcome message on client side only (to avoid hydration mismatch)
  useEffect(() => {
    if (!isInitialized && messages.length === 0) {
      setMessages([
        {
          role: "assistant",
          content:
            "Hi! I'm an AI assistant powered by local LLM. Ask me anything about my creator's work, skills, or projects!",
          timestamp: new Date(),
        },
      ]);
      setIsInitialized(true);
    }
  }, [isInitialized, messages.length]);
  const [inputMessage, setInputMessage] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = useCallback(async () => {
    if (!inputMessage.trim()) return;

    const userMessage: ChatMessage = {
      role: "user",
      content: inputMessage,
      timestamp: new Date(),
    };

    const currentHistory = [...messages.slice(-maxHistory + 1), userMessage];
    setMessages(currentHistory);
    setInputMessage("");
    setIsTyping(true);

    try {
      const response = await fetch(`${API_BASE_URL}/chat/stream`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: userMessage.content,
          history: currentHistory.slice(0, -1).map((msg) => ({
            role: msg.role,
            content: msg.content,
          })),
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to get response");
      }

      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error("No response body");
      }

      const decoder = new TextDecoder();
      let buffer = "";
      let assistantContent = "";
      let messageAdded = false;

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop() || "";

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            const data = line.slice(6);
            if (data === "[DONE]") {
              break;
            }
            try {
              const chunk = JSON.parse(data);
              if (chunk.chunk) {
                assistantContent += chunk.chunk;
                
                // Only add message bubble when first chunk arrives
                if (!messageAdded) {
                  setMessages((prev) => [...prev, {
                    role: "assistant",
                    content: assistantContent,
                    timestamp: new Date(),
                  }]);
                  messageAdded = true;
                  setIsTyping(false); // Stop showing "Thinking..." only when content starts
                } else {
                  setMessages((prev) => {
                    const newMessages = [...prev];
                    if (newMessages.length > 0) {
                      newMessages[newMessages.length - 1] = {
                        ...newMessages[newMessages.length - 1],
                        content: assistantContent,
                      };
                    }
                    return newMessages;
                  });
                }
              }
            } catch {
              // Skip invalid JSON
            }
          }
        }
      }
      setIsTyping(false); // Ensure typing stops when stream ends
    } catch (error) {
      console.error("Chat error:", error);
      setIsTyping(false);
      const errorMessage: ChatMessage = {
        role: "assistant",
        content:
          "I'm sorry, I couldn't connect to the AI backend. Please make sure Ollama is running and try again.",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    }
  }, [inputMessage, messages, maxHistory]);

  const clearMessages = useCallback(() => {
    setMessages([
      {
        role: "assistant",
        content:
          "Hi! I'm an AI assistant powered by local LLM. Ask me anything about my creator's work, skills, or projects!",
        timestamp: new Date(),
      },
    ]);
  }, []);

  return {
    messages,
    inputMessage,
    setInputMessage,
    isTyping,
    sendMessage,
    messagesEndRef,
    clearMessages,
  };
}

