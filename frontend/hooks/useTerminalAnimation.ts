/**
 * Custom hook for terminal typing animation effect.
 */

import { useState, useEffect } from "react";

interface UseTerminalAnimationOptions {
  text: string;
  typingSpeed?: number;
  cursorBlinkSpeed?: number;
}

interface UseTerminalAnimationReturn {
  displayText: string;
  showCursor: boolean;
  isComplete: boolean;
}

export function useTerminalAnimation({
  text,
  typingSpeed = 50,
  cursorBlinkSpeed = 500,
}: UseTerminalAnimationOptions): UseTerminalAnimationReturn {
  const [displayText, setDisplayText] = useState("");
  const [showCursor, setShowCursor] = useState(true);
  const [isComplete, setIsComplete] = useState(false);

  useEffect(() => {
    let index = 0;
    
    const typingInterval = setInterval(() => {
      if (index <= text.length) {
        setDisplayText(text.slice(0, index));
        index++;
      } else {
        setIsComplete(true);
        clearInterval(typingInterval);
      }
    }, typingSpeed);

    const cursorInterval = setInterval(() => {
      setShowCursor((prev) => !prev);
    }, cursorBlinkSpeed);

    return () => {
      clearInterval(typingInterval);
      clearInterval(cursorInterval);
    };
  }, [text, typingSpeed, cursorBlinkSpeed]);

  return { displayText, showCursor, isComplete };
}

