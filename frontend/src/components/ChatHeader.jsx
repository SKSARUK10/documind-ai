import { FileIcon } from './icons'

function ChatHeader({ selectedDocument, isThinking }) {
  return (
    <div className="flex items-center gap-3 border-b border-slate-200 bg-white px-4 py-3 sm:px-6">
      <div className="min-w-0">
        <h1 className="text-base font-semibold text-slate-900">Chat</h1>
        <div className="mt-0.5 flex items-center gap-1.5 text-xs text-slate-500">
          <FileIcon className="h-3.5 w-3.5 shrink-0" />
          <span className="truncate">
            {selectedDocument
              ? selectedDocument.document_name
              : 'No document selected'}
          </span>
        </div>
      </div>

      <span className="ml-auto flex shrink-0 items-center gap-2 text-xs text-slate-500">
        <span
          className={`h-2 w-2 rounded-full ${
            isThinking ? 'animate-pulse bg-indigo-500' : 'bg-emerald-500'
          }`}
        />
        {isThinking ? 'Thinking...' : 'Ready'}
      </span>
    </div>
  )
}

export default ChatHeader
