import { MenuIcon } from './icons'

function Header({ onToggleSidebar }) {
  return (
    <header className="flex h-14 shrink-0 items-center gap-3 border-b border-slate-200 bg-white px-4">
      <button
        type="button"
        onClick={onToggleSidebar}
        aria-label="Open document sidebar"
        className="rounded-md p-1.5 text-slate-500 transition hover:bg-slate-100 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 md:hidden"
      >
        <MenuIcon className="h-5 w-5" />
      </button>

      <div className="flex items-center gap-2.5">
        <img
          src="/documind-logo.svg"
          alt=""
          className="h-8 w-8"
          width="32"
          height="32"
        />
        <div>
          <p className="text-sm leading-tight font-semibold text-slate-900">
            DocuMind AI
          </p>
          <p className="text-xs leading-tight text-slate-500">
            AI Document Assistant
          </p>
        </div>
      </div>

      <span className="ml-auto hidden rounded-full border border-slate-200 bg-slate-50 px-2.5 py-1 text-xs text-slate-500 sm:inline-block">
        RAG · FAISS · MCP
      </span>
    </header>
  )
}

export default Header
