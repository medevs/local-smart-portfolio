"use client";

import { Send } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

interface ChatInputProps {
  value: string;
  onChange: (value: string) => void;
  onSend: () => void;
  disabled?: boolean;
}

export function ChatInput({ value, onChange, onSend, disabled }: ChatInputProps) {
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      onSend();
    }
  };

  return (
    <div className="p-4 border-t border-amber-700/30">
      <div className="flex gap-2">
        <Input
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask me anything..."
          className="bg-amber-950/30 border-amber-700/50 text-amber-100 placeholder:text-amber-400/50"
        />
        <Button
          onClick={onSend}
          disabled={!value.trim() || disabled}
          className="bg-amber-700 hover:bg-amber-600 text-white"
          aria-label="Send message"
        >
          <Send className="w-4 h-4" />
        </Button>
      </div>
      <p className="text-xs text-amber-200/40 mt-2">
        Connected to local LLM endpoint
      </p>
    </div>
  );
}

