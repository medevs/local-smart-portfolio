import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

// Mock the ChatInput component props
interface ChatInputProps {
  value: string
  onChange: (value: string) => void
  onSend: () => void
  disabled?: boolean
  placeholder?: string
}

// Simple ChatInput component for testing
function ChatInput({ value, onChange, onSend, disabled = false, placeholder = 'Type a message...' }: ChatInputProps) {
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey && !disabled) {
      e.preventDefault()
      onSend()
    }
  }

  return (
    <div className="flex gap-2">
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={handleKeyDown}
        disabled={disabled}
        placeholder={placeholder}
        data-testid="chat-input"
      />
      <button
        onClick={onSend}
        disabled={disabled || !value.trim()}
        data-testid="send-button"
      >
        Send
      </button>
    </div>
  )
}

describe('ChatInput', () => {
  it('renders input field with placeholder', () => {
    const onChange = vi.fn()
    const onSend = vi.fn()

    render(
      <ChatInput
        value=""
        onChange={onChange}
        onSend={onSend}
        placeholder="Ask about Ahmed..."
      />
    )

    const input = screen.getByTestId('chat-input')
    expect(input).toBeInTheDocument()
    expect(input).toHaveAttribute('placeholder', 'Ask about Ahmed...')
  })

  it('calls onChange when typing', async () => {
    const onChange = vi.fn()
    const onSend = vi.fn()
    const user = userEvent.setup()

    render(
      <ChatInput
        value=""
        onChange={onChange}
        onSend={onSend}
      />
    )

    const input = screen.getByTestId('chat-input')
    await user.type(input, 'Hello')

    expect(onChange).toHaveBeenCalled()
  })

  it('calls onSend when Enter is pressed', async () => {
    const onChange = vi.fn()
    const onSend = vi.fn()
    const user = userEvent.setup()

    render(
      <ChatInput
        value="Test message"
        onChange={onChange}
        onSend={onSend}
      />
    )

    const input = screen.getByTestId('chat-input')
    await user.type(input, '{Enter}')

    expect(onSend).toHaveBeenCalled()
  })

  it('does not call onSend when disabled', async () => {
    const onChange = vi.fn()
    const onSend = vi.fn()
    const user = userEvent.setup()

    render(
      <ChatInput
        value="Test message"
        onChange={onChange}
        onSend={onSend}
        disabled={true}
      />
    )

    const button = screen.getByTestId('send-button')
    await user.click(button)

    expect(onSend).not.toHaveBeenCalled()
  })

  it('disables send button when input is empty', () => {
    const onChange = vi.fn()
    const onSend = vi.fn()

    render(
      <ChatInput
        value=""
        onChange={onChange}
        onSend={onSend}
      />
    )

    const button = screen.getByTestId('send-button')
    expect(button).toBeDisabled()
  })

  it('enables send button when input has text', () => {
    const onChange = vi.fn()
    const onSend = vi.fn()

    render(
      <ChatInput
        value="Test message"
        onChange={onChange}
        onSend={onSend}
      />
    )

    const button = screen.getByTestId('send-button')
    expect(button).not.toBeDisabled()
  })
})
