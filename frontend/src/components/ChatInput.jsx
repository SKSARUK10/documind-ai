import { useRef, useState } from 'react'
import { SendIcon } from './icons'

function ChatInput({ onSend, disabled }) {
  const [text, setText] = useState('')
  const textareaRef = useRef(null)

  function resizeTextarea() {
    const textarea = textareaRef.current

    if (!textarea) return

    textarea.style.height = 'auto'
    textarea.style.height = `${Math.min(textarea.scrollHeight, 176)}px`
  }

  function handleChange(event) {
    setText(event.target.value)
    resizeTextarea()
  }

  function handleSubmit(event) {
    event.preventDefault()

    const trimmed = text.trim()

    if (!trimmed || disabled) return

    onSend(trimmed)
    setText('')

    const textarea = textareaRef.current

    if (textarea) textarea.style.height = 'auto'
  }

  function handleKeyDown(event) {
    if (
      event.key === 'Enter' &&
      !event.shiftKey &&
      !event.nativeEvent.isComposing
    ) {
      event.preventDefault()
      event.currentTarget.form?.requestSubmit()
    }
  }

  return (
    <div className="shrink-0 border-t border-slate-200 bg-white px-4 py-4 sm:px-6">
      <form onSubmit={handleSubmit} className="mx-auto max-w-3xl">
        <div className="flex items-end gap-2 rounded-2xl border border-slate-300 bg-white p-2 shadow-sm transition focus-within:border-indigo-500 focus-within:ring-2 focus-within:ring-indigo-100">
          <label htmlFor="chat-input" className="sr-only">
            Ask about your document
          </label>
          <textarea
            id="chat-input"
            ref={textareaRef}
            rows={1}
            value={text}
            onChange={handleChange}
            onKeyDown={handleKeyDown}
            disabled={disabled}
            placeholder="Ask about your document..."
            className="max-h-44 min-h-9 flex-1 resize-none bg-transparent px-2 py-1.5 text-sm text-slate-800 placeholder:text-slate-400 focus:outline-none disabled:cursor-not-allowed"
          />
          <button
            type="submit"
            disabled={disabled || !text.trim()}
            aria-label="Send message"
            className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-indigo-600 text-white transition hover:bg-indigo-700 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 disabled:cursor-not-allowed disabled:opacity-50"
          >
            <SendIcon className="h-4 w-4" />
          </button>
        </div>

        <p className="mt-1.5 text-center text-[11px] text-slate-400">
          Enter to send · Shift + Enter for a new line
        </p>
      </form>
    </div>
  )
}

export default ChatInput
