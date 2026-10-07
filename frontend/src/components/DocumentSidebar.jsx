import { useRef } from 'react'
import { CloseIcon, FileIcon, PlusIcon } from './icons'

function DocumentSidebar({
  documents,
  documentsError,
  selectedDocumentId,
  isOpen,
  onSelect,
  onClose,
  onUpload,
  isUploading,
  uploadError,
}) {
  const fileInputRef = useRef(null)

  function handleUploadClick() {
    fileInputRef.current?.click()
  }

  function handleFileChange(event) {
    const file = event.target.files?.[0]

    if (!file) return

    onUpload(file)

    event.target.value = ''
  }

  return (
    <aside
      className={`fixed top-14 right-auto bottom-0 left-0 z-40 flex w-72 flex-col border-r border-slate-200 bg-white transition-transform dark:border-slate-700 dark:bg-slate-900 md:static md:z-auto md:translate-x-0 ${
        isOpen ? 'translate-x-0' : '-translate-x-full'
      }`}
    >
      <div className="flex items-center justify-between border-b border-slate-200 px-4 py-3 dark:border-slate-700">
        <h2 className="text-sm font-semibold text-slate-900 dark:text-slate-50">
          Documents
        </h2>

        <button
          type="button"
          onClick={onClose}
          aria-label="Close document sidebar"
          className="rounded-md p-1 text-slate-400 transition hover:bg-slate-100 hover:text-slate-600 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 dark:text-slate-500 dark:hover:bg-slate-800 dark:hover:text-slate-300 dark:focus-visible:outline-indigo-400 md:hidden"
        >
          <CloseIcon className="h-4 w-4" />
        </button>
      </div>

      <div className="px-4 py-3">
        <input
          ref={fileInputRef}
          type="file"
          accept="application/pdf"
          onChange={handleFileChange}
          className="hidden"
        />

        <button
          type="button"
          onClick={handleUploadClick}
          disabled={isUploading}
          className="flex w-full items-center justify-center gap-2 rounded-lg bg-indigo-600 px-3 py-2 text-sm font-medium text-white transition hover:bg-indigo-700 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 dark:focus-visible:outline-indigo-400 disabled:cursor-not-allowed disabled:opacity-60"
        >
          <PlusIcon className="h-4 w-4" />

          {isUploading ? 'Uploading...' : 'Upload document'}
        </button>

        <p className="mt-1.5 text-center text-[11px] text-slate-400 dark:text-slate-500">
          PDF files only
        </p>

        {uploadError && (
          <p className="mt-2 text-center text-xs font-medium text-red-600 dark:text-red-400">
            {uploadError}
          </p>
        )}
      </div>

      <ul className="flex-1 space-y-1 overflow-y-auto px-2 pb-4">
        {documentsError && (
          <li className="px-2 py-3 text-center text-xs font-medium text-red-600 dark:text-red-400">
            {documentsError}
          </li>
        )}

        {!documentsError && documents.length === 0 ? (
          <li className="px-2 py-8 text-center text-sm text-slate-400 dark:text-slate-500">
            No documents yet
          </li>
        ) : (
          documents.map((document) => {
            const isSelected =
              document.document_id === selectedDocumentId

            return (
              <li key={document.document_id}>
                <button
                  type="button"
                  onClick={() => onSelect(document.document_id)}
                  aria-current={isSelected ? 'true' : undefined}
                  className={`flex w-full items-center gap-2.5 rounded-lg border px-3 py-2.5 text-left text-sm transition focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 dark:focus-visible:outline-indigo-400 ${
                    isSelected
                      ? 'border-indigo-200 bg-indigo-50 text-indigo-700 dark:border-indigo-500/50 dark:bg-indigo-500/15 dark:text-indigo-300'
                      : 'border-transparent text-slate-600 hover:border-slate-200 hover:bg-slate-50 dark:text-slate-300 dark:hover:border-slate-700 dark:hover:bg-slate-800'
                  }`}
                >
                  <FileIcon className="h-4 w-4 shrink-0" />
                  <span className="truncate">
                    {document.document_name}
                  </span>
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