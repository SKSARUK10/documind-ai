import { useEffect, useRef } from 'react'
import ChatMessage from './ChatMessage'
import LoadingMessage from './LoadingMessage'

function ChatMessages({ messages, isThinking }) {
  const endRef = useRef(null)

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isThinking])

  if (messages.length === 0) {
    return (
      <section className="flex flex-1 items-center justify-center overflow-y-auto px-6 py-10">
        <div className="max-w-md text-center">
          <img
            src="/documind-logo.svg"
            alt=""
            className="mx-auto h-12 w-12 rounded-xl"
            width="48"
            height="48"
          />
          <h2 className="mt-4 text-lg font-semibold text-slate-900">
            Ask questions about your documents
          </h2>
          <p className="mt-2 text-sm leading-6 text-slate-500">
            DocuMind AI uses retrieval-augmented generation to answer questions
            using your uploaded documents.
          </p>
        </div>
      </section>
    )
  }

  return (
    <section
      className="flex-1 overflow-y-auto px-4 py-6 sm:px-6"
      aria-label="Conversation"
    >
      <div className="mx-auto flex max-w-3xl flex-col gap-5">
        {messages.map((message) => (
          <ChatMessage key={message.id} message={message} />
        ))}
        {isThinking && <LoadingMessage />}
        <div ref={endRef} />
      </div>
    </section>
  )
}

export default ChatMessages
