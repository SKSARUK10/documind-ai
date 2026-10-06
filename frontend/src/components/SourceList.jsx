import { useState } from 'react'
import { ChevronIcon, FileIcon } from './icons'

function SourceList({ sources }) {
  const [isOpen, setIsOpen] = useState(true)

  return (
    <div className="mt-2 rounded-xl border border-slate-200 bg-slate-50">
      <button
        type="button"
        onClick={() => setIsOpen((open) => !open)}
        aria-expanded={isOpen}
        className="flex w-full items-center gap-2 px-3 py-2 text-xs font-medium text-slate-600 transition hover:text-slate-900 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
      >
        Sources ({sources.length})
        <ChevronIcon
          className={`ml-auto h-4 w-4 text-slate-400 transition-transform ${
            isOpen ? '' : '-rotate-90'
          }`}
        />
      </button>

      {isOpen && (
        <ul className="space-y-1.5 border-t border-slate-200 px-3 py-2.5">
          {sources.map((source, index) => (
            <li
              key={`${source.document_id ?? 'source'}-${source.page ?? 0}-${index}`}
              className="flex items-center gap-2 text-xs text-slate-600"
            >
              <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-md border border-slate-200 bg-white text-slate-400">
                <FileIcon className="h-3.5 w-3.5" />
              </span>
              <span className="truncate">
                {source.document_name || 'Document'}
                {source.page != null ? ` · Page ${source.page}` : ''}
              </span>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

export default SourceList
