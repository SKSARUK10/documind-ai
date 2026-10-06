import SourceList from './SourceList'
import { AlertIcon } from './icons'

function ChatMessage({ message }) {
  if (message.role === 'user') {
    return (
      <div className="flex justify-end">
        <div className="max-w-[85%] rounded-2xl rounded-br-md bg-indigo-600 px-4 py-2.5 text-sm leading-6 whitespace-pre-wrap text-white">
          {message.content}
        </div>
      </div>
    )
  }

  return (
    <div className="flex gap-3">
      <img
        src="/documind-logo.svg"
        alt=""
        aria-hidden="true"
        className="mt-1 h-8 w-8 shrink-0 rounded-lg"
        width="32"
        height="32"
      />

      <div className="min-w-0 max-w-[85%] flex-1">
        <div
          className={`rounded-2xl rounded-tl-md px-4 py-3 text-sm leading-6 whitespace-pre-wrap ${
            message.error
              ? 'border border-red-200 bg-red-50 text-red-700'
              : 'border border-slate-200 bg-white text-slate-700'
          }`}
        >
          {message.error && (
            <AlertIcon className="mr-1.5 inline h-4 w-4 align-[-2px]" />
          )}
          {message.content}
        </div>

        {!message.error && message.sources?.length > 0 && (
          <SourceList sources={message.sources} />
        )}
      </div>
    </div>
  )
}

export default ChatMessage
