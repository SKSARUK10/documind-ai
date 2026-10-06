import { CloseIcon, FileIcon, PlusIcon } from './icons'

function DocumentSidebar({
  documents,
  selectedDocumentId,
  isOpen,
  onSelect,
  onClose,
}) {
  return (
    <aside
      className={`fixed top-14 right-auto bottom-0 left-0 z-40 flex w-72 flex-col border-r border-slate-200 bg-white transition-transform md:static md:z-auto md:translate-x-0 ${
        isOpen ? 'translate-x-0' : '-translate-x-full'
      }`}
    >
      <div className="flex items-center justify-between border-b border-slate-200 px-4 py-3">
        <h2 className="text-sm font-semibold text-slate-900">Documents</h2>
        <button
          type="button"
          onClick={onClose}
          aria-label="Close document sidebar"
          className="rounded-md p-1 text-slate-400 transition hover:bg-slate-100 hover:text-slate-600 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 md:hidden"
        >
          <CloseIcon className="h-4 w-4" />
        </button>
      </div>

      <div className="px-4 py-3">
        <button
          type="button"
          disabled
          title="Upload will be available soon"
          className="flex w-full items-center justify-center gap-2 rounded-lg bg-indigo-600 px-3 py-2 text-sm font-medium text-white transition hover:bg-indigo-700 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 disabled:cursor-not-allowed disabled:opacity-60"
        >
          <PlusIcon className="h-4 w-4" />
          Upload document
        </button>
        <p className="mt-1.5 text-center text-[11px] text-slate-400">
          Coming soon
        </p>
      </div>

      <ul className="flex-1 space-y-1 overflow-y-auto px-2 pb-4">
        {documents.length === 0 ? (
          <li className="px-2 py-8 text-center text-sm text-slate-400">
            No documents yet
          </li>
        ) : (
          documents.map((document) => {
            const isSelected = document.document_id === selectedDocumentId

            return (
              <li key={document.document_id}>
                <button
                  type="button"
                  onClick={() => onSelect(document.document_id)}
                  aria-current={isSelected ? 'true' : undefined}
                  className={`flex w-full items-center gap-2.5 rounded-lg border px-3 py-2.5 text-left text-sm transition focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 ${
                    isSelected
                      ? 'border-indigo-200 bg-indigo-50 text-indigo-700'
                      : 'border-transparent text-slate-600 hover:border-slate-200 hover:bg-slate-50'
                  }`}
                >
                  <FileIcon className="h-4 w-4 shrink-0" />
                  <span className="truncate">{document.document_name}</span>
                </button>
              </li>
            )
          })
        )}
      </ul>
    </aside>
  )
}

export default DocumentSidebar
