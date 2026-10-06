import { useState } from 'react'
import ChatHeader from './components/ChatHeader'
import ChatInput from './components/ChatInput'
import ChatMessages from './components/ChatMessages'
import DocumentSidebar from './components/DocumentSidebar'
import Header from './components/Header'
import { GENERIC_ERROR_MESSAGE, sendChatMessage } from './services/api'
import { TEMP_DOCUMENTS } from './services/documents'

function App() {
  const [messages, setMessages] = useState([])
  const [isThinking, setIsThinking] = useState(false)
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)
  const [selectedDocumentId, setSelectedDocumentId] = useState(
    TEMP_DOCUMENTS[0]?.document_id ?? null,
  )

  const selectedDocument =
    TEMP_DOCUMENTS.find(
      (document) => document.document_id === selectedDocumentId,
    ) ?? null

  async function handleSend(text) {
    if (isThinking) return

    const nextMessages = [
      ...messages,
      { id: crypto.randomUUID(), role: 'user', content: text },
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
    <div className="flex h-dvh flex-col bg-slate-50 text-slate-800">
      <Header onToggleSidebar={() => setIsSidebarOpen((open) => !open)} />

      <div className="flex min-h-0 flex-1">
        {isSidebarOpen && (
          <button
            type="button"
            aria-label="Close document sidebar"
            onClick={() => setIsSidebarOpen(false)}
            className="fixed top-14 right-0 bottom-0 left-0 z-30 bg-slate-900/40 md:hidden"
          />
        )}

        <DocumentSidebar
          documents={TEMP_DOCUMENTS}
          selectedDocumentId={selectedDocumentId}
          isOpen={isSidebarOpen}
          onSelect={handleSelectDocument}
          onClose={() => setIsSidebarOpen(false)}
        />

        <main className="flex min-w-0 flex-1 flex-col bg-white md:border-l md:border-slate-200">
          <ChatHeader
            selectedDocument={selectedDocument}
            isThinking={isThinking}
          />
          <ChatMessages messages={messages} isThinking={isThinking} />
          <ChatInput onSend={handleSend} disabled={isThinking} />
        </main>
      </div>
    </div>
  )
}

export default App
