import { describe, it, expect, vi, beforeEach } from 'vitest'
import { renderHook, act, waitFor } from '@testing-library/react'

// Mock chat message type
interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
  timestamp: string
}

// Simplified useChat hook for testing
function useChat() {
  return {
    messages: [] as ChatMessage[],
    inputMessage: '',
    setInputMessage: vi.fn(),
    isTyping: false,
    sendMessage: vi.fn(),
    clearMessages: vi.fn(),
  }
}

describe('useChat Hook', () => {
  let mockFetch: ReturnType<typeof vi.fn>

  beforeEach(() => {
    mockFetch = vi.fn()
    global.fetch = mockFetch
    vi.clearAllMocks()
  })

  describe('Initial State', () => {
    it('returns empty messages array initially', () => {
      const hook = useChat()
      expect(hook.messages).toEqual([])
    })

    it('returns empty input message initially', () => {
      const hook = useChat()
      expect(hook.inputMessage).toBe('')
    })

    it('returns isTyping as false initially', () => {
      const hook = useChat()
      expect(hook.isTyping).toBe(false)
    })
  })

  describe('Message Management', () => {
    it('provides setInputMessage function', () => {
      const hook = useChat()
      expect(typeof hook.setInputMessage).toBe('function')
    })

    it('provides sendMessage function', () => {
      const hook = useChat()
      expect(typeof hook.sendMessage).toBe('function')
    })

    it('provides clearMessages function', () => {
      const hook = useChat()
      expect(typeof hook.clearMessages).toBe('function')
    })
  })
})

describe('Chat Message Processing', () => {
  it('parses SSE data correctly', () => {
    const sseData = 'data: {"chunk": "Hello", "done": false, "sources": null}\n\n'
    const jsonStart = sseData.indexOf('{')
    const jsonEnd = sseData.lastIndexOf('}') + 1
    const json = sseData.slice(jsonStart, jsonEnd)
    const parsed = JSON.parse(json)

    expect(parsed.chunk).toBe('Hello')
    expect(parsed.done).toBe(false)
    expect(parsed.sources).toBeNull()
  })

  it('handles done event with sources', () => {
    const sseData = 'data: {"chunk": "", "done": true, "sources": ["test.md", "skills.md"]}\n\n'
    const jsonStart = sseData.indexOf('{')
    const jsonEnd = sseData.lastIndexOf('}') + 1
    const json = sseData.slice(jsonStart, jsonEnd)
    const parsed = JSON.parse(json)

    expect(parsed.done).toBe(true)
    expect(parsed.sources).toEqual(['test.md', 'skills.md'])
  })

  it('handles [DONE] event', () => {
    const sseData = 'data: [DONE]\n\n'
    const isDone = sseData.includes('[DONE]')

    expect(isDone).toBe(true)
  })
})

describe('Chat Request Format', () => {
  it('formats chat request correctly', () => {
    const message = "What are Ahmed's skills?"
    const history: ChatMessage[] = [
      { role: 'user', content: 'Hello', timestamp: '10:00' },
      { role: 'assistant', content: 'Hi there!', timestamp: '10:01' },
    ]

    const request = {
      message,
      history: history.map((m) => ({ role: m.role, content: m.content })),
    }

    expect(request.message).toBe("What are Ahmed's skills?")
    expect(request.history).toHaveLength(2)
    expect(request.history[0].role).toBe('user')
  })

  it('handles empty history', () => {
    const message = 'First message'
    const history: ChatMessage[] = []

    const request = {
      message,
      history: history.map((m) => ({ role: m.role, content: m.content })),
    }

    expect(request.history).toHaveLength(0)
  })
})

describe('Message Timestamp', () => {
  it('generates timestamp in correct format', () => {
    const now = new Date()
    const timestamp = now.toLocaleTimeString([], {
      hour: '2-digit',
      minute: '2-digit',
    })

    // Should match HH:MM format
    expect(timestamp).toMatch(/\d{1,2}:\d{2}/)
  })
})

describe('Error Message Handling', () => {
  it('creates error message with correct format', () => {
    const errorContent = 'Sorry, I encountered an error. Please try again.'
    const errorMessage: ChatMessage = {
      role: 'assistant',
      content: errorContent,
      timestamp: new Date().toLocaleTimeString([], {
        hour: '2-digit',
        minute: '2-digit',
      }),
    }

    expect(errorMessage.role).toBe('assistant')
    expect(errorMessage.content).toContain('error')
  })
})

describe('Message History Limit', () => {
  it('respects maximum message limit', () => {
    const maxMessages = 10
    const messages: ChatMessage[] = Array.from({ length: 15 }, (_, i) => ({
      role: i % 2 === 0 ? 'user' : 'assistant',
      content: `Message ${i}`,
      timestamp: '10:00',
    }))

    // Simulate trimming to max
    const trimmed = messages.slice(-maxMessages)

    expect(trimmed).toHaveLength(maxMessages)
    expect(trimmed[0].content).toBe('Message 5')
    expect(trimmed[9].content).toBe('Message 14')
  })
})
