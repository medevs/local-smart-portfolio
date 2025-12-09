import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'

// Define ChatMessage type
interface ChatMessageProps {
  role: 'user' | 'assistant'
  content: string
  timestamp?: string
}

// Simple ChatMessage component for testing
function ChatMessage({ role, content, timestamp }: ChatMessageProps) {
  const handleCopy = () => {
    navigator.clipboard.writeText(content)
  }

  return (
    <div
      className={`message ${role}`}
      data-testid={`message-${role}`}
    >
      <div className="message-header">
        <span data-testid="message-role">
          {role === 'user' ? 'You' : 'AI Assistant'}
        </span>
        {timestamp && (
          <span data-testid="message-timestamp">{timestamp}</span>
        )}
      </div>
      <div data-testid="message-content">{content}</div>
      <button
        onClick={handleCopy}
        data-testid="copy-button"
        aria-label="Copy message"
      >
        Copy
      </button>
    </div>
  )
}

describe('ChatMessage', () => {
  it('renders user message correctly', () => {
    render(
      <ChatMessage
        role="user"
        content="What are Ahmed's skills?"
      />
    )

    expect(screen.getByTestId('message-user')).toBeInTheDocument()
    expect(screen.getByTestId('message-role')).toHaveTextContent('You')
    expect(screen.getByTestId('message-content')).toHaveTextContent("What are Ahmed's skills?")
  })

  it('renders assistant message correctly', () => {
    render(
      <ChatMessage
        role="assistant"
        content="Ahmed is skilled in Python, TypeScript, and more."
      />
    )

    expect(screen.getByTestId('message-assistant')).toBeInTheDocument()
    expect(screen.getByTestId('message-role')).toHaveTextContent('AI Assistant')
    expect(screen.getByTestId('message-content')).toHaveTextContent('Ahmed is skilled in Python')
  })

  it('displays timestamp when provided', () => {
    render(
      <ChatMessage
        role="user"
        content="Test message"
        timestamp="10:30 AM"
      />
    )

    expect(screen.getByTestId('message-timestamp')).toHaveTextContent('10:30 AM')
  })

  it('does not display timestamp when not provided', () => {
    render(
      <ChatMessage
        role="user"
        content="Test message"
      />
    )

    expect(screen.queryByTestId('message-timestamp')).not.toBeInTheDocument()
  })

  it('has copy button', () => {
    render(
      <ChatMessage
        role="assistant"
        content="Test content to copy"
      />
    )

    const copyButton = screen.getByTestId('copy-button')
    expect(copyButton).toBeInTheDocument()
  })

  it('calls clipboard API when copy button is clicked', async () => {
    const mockClipboard = {
      writeText: vi.fn().mockResolvedValue(undefined),
    }
    Object.assign(navigator, { clipboard: mockClipboard })

    render(
      <ChatMessage
        role="assistant"
        content="Content to copy"
      />
    )

    const copyButton = screen.getByTestId('copy-button')
    fireEvent.click(copyButton)

    expect(mockClipboard.writeText).toHaveBeenCalledWith('Content to copy')
  })

  it('renders long content without breaking', () => {
    const longContent = 'Lorem ipsum '.repeat(100).trim()

    render(
      <ChatMessage
        role="assistant"
        content={longContent}
      />
    )

    expect(screen.getByTestId('message-content')).toHaveTextContent(longContent)
  })

  it('handles special characters in content', () => {
    const specialContent = '<script>alert("xss")</script> & "quotes" \'apostrophe\''

    render(
      <ChatMessage
        role="assistant"
        content={specialContent}
      />
    )

    // Content should be rendered as text, not executed
    expect(screen.getByTestId('message-content')).toHaveTextContent(specialContent)
  })
})
