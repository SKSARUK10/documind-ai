import { useEffect, useState } from 'react'
import ChatHeader from './components/ChatHeader'
import ChatInput from './components/ChatInput'
import ChatMessages from './components/ChatMessages'
import DocumentSidebar from './components/DocumentSidebar'
import Header from './components/Header'
import { GENERIC_ERROR_MESSAGE, sendChatMessage } from './services/api'
import { getDocuments, uploadDocument } from './services/documents'

function App() {
  const [messages, setMessages] = useState([])
  const [isThinking, setIsThinking] = useState(false)
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)

  const [documents, setDocuments] = useState([])
  const [documentsError, setDocumentsError] = useState(null)
  const [selectedDocumentId, setSelectedDocumentId] = useState(null)

  const [isUploading, setIsUploading] = useState(false)
  const [uploadError, setUploadError] = useState(null)

  async function loadDocuments() {
    try {
      const data = await getDocuments()

      setDocuments(data)
      setDocumentsError(null)

      if (data.length > 0) {
        setSelectedDocumentId(
          (currentId) => currentId ?? data[0].document_id,
        )
      }

      return true
    } catch (error) {
      console.error('Failed to load documents:', error)
      setDocumentsError('Failed to load documents')

      return false
    }
  }

  // Fetch the document list once on mount; handleUpload refreshes it
  // explicitly after a successful upload. setState runs only after the
  // network promise resolves, so this cannot cascade renders.
  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    loadDocuments()
  }, [])

  async function handleUpload(file) {
    if (isUploading) return

    setIsUploading(true)
    setUploadError(null)

    try {
      const uploadedDocument = await uploadDocument(file)

      const reloadSucceeded = await loadDocuments()

      if (reloadSucceeded) {
        setSelectedDocumentId(uploadedDocument.document_id)
      }
    } catch (error) {
      console.error('Document upload failed:', error)
      setUploadError('Failed to upload document')
    } finally {
      setIsUploading(false)
    }
  }

  const selectedDocument =
    documents.find(
      (document) => document.document_id === selectedDocumentId,
    ) ?? null

  async function handleSend(text) {
    if (isThinking) return

    const nextMessages = [
      ...messages,
      {
        id: crypto.randomUUID(),
        role: 'user',
        content: text,
      },
    ]

    setMessages(nextMessages)
    setIsThinking(true)

    try {
      const history = nextMessages
        .filter((message) => !message.error)
        .map(({ role, content }) => ({ role, content }))

      const response = await sendChatMessage(
        history,
        selectedDocumentId ? [selectedDocumentId] : [],
      )

      setMessages((previous) => [
        ...previous,
        {
          id: crypto.randomUUID(),
          role: 'assistant',
          content: response.answer,
          sources: response.sources,
        },
      ])
    } catch (error) {
      console.error('Chat request failed:', error)

      setMessages((previous) => [
        ...previous,
        {
          id: crypto.randomUUID(),
          role: 'assistant',
          content: GENERIC_ERROR_MESSAGE,
          error: true,
        },
      ])
    } finally {
      setIsThinking(false)
    }
  }

  function handleSelectDocument(documentId) {
    setSelectedDocumentId(documentId)
    setIsSidebarOpen(false)
  }

  return (
    <div className="flex h-dvh flex-col bg-slate-50 text-slate-800 dark:bg-slate-950 dark:text-slate-100">
      <Header
        onToggleSidebar={() => setIsSidebarOpen((open) => !open)}
      />

      <div className="flex min-h-0 flex-1">
        {isSidebarOpen && (
          <button
            type="button"
            aria-label="Close document sidebar"
            onClick={() => setIsSidebarOpen(false)}
            className="fixed top-14 right-0 bottom-0 left-0 z-30 bg-slate-900/40 dark:bg-black/60 md:hidden"
          />
        )}

        <DocumentSidebar
          documents={documents}
          documentsError={documentsError}
          selectedDocumentId={selectedDocumentId}
          isOpen={isSidebarOpen}
          onSelect={handleSelectDocument}
          onClose={() => setIsSidebarOpen(false)}
          onUpload={handleUpload}
          isUploading={isUploading}
          uploadError={uploadError}
        />

        <main className="flex min-w-0 flex-1 flex-col bg-white dark:border-slate-700 dark:bg-slate-900 md:border-l md:border-slate-200">
          <ChatHeader
            selectedDocument={selectedDocument}
            isThinking={isThinking}
          />

          <ChatMessages
            messages={messages}
            isThinking={isThinking}
          />

          <ChatInput
            onSend={handleSend}
            disabled={isThinking}
          />
        </main>
      </div>
    </div>
  )
}

export default App