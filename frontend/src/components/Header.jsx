import useTheme from '../hooks/useTheme'
import { MenuIcon, MoonIcon, SunIcon } from './icons'

function Header({ onToggleSidebar }) {
  const { theme, toggleTheme } = useTheme()
  const isDark = theme === 'dark'

  return (
    <header className="flex h-14 shrink-0 items-center gap-3 border-b border-slate-200 bg-white px-4 dark:border-slate-700 dark:bg-slate-900">
      <button
        type="button"
        onClick={onToggleSidebar}
        aria-label="Open document sidebar"
        className="rounded-md p-1.5 text-slate-500 transition hover:bg-slate-100 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 dark:text-slate-400 dark:hover:bg-slate-800 dark:focus-visible:outline-indigo-400 md:hidden"
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
          <p className="text-sm leading-tight font-semibold text-slate-900 dark:text-slate-50">
            DocuMind AI
          </p>
          <p className="text-xs leading-tight text-slate-500 dark:text-slate-400">
            AI Document Assistant
          </p>
        </div>
      </div>

      <span className="ml-auto hidden rounded-full border border-slate-200 bg-slate-50 px-2.5 py-1 text-xs text-slate-500 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-400 sm:inline-block">
        RAG · FAISS · MCP
      </span>

      <button
        type="button"
        onClick={toggleTheme}
        aria-label={
          isDark ? 'Switch to light mode' : 'Switch to dark mode'
        }
        title={isDark ? 'Switch to light mode' : 'Switch to dark mode'}
        className="ml-auto rounded-md p-1.5 text-slate-500 transition hover:bg-slate-100 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 dark:text-slate-400 dark:hover:bg-slate-800 dark:focus-visible:outline-indigo-400 sm:ml-0"
      >
        {isDark ? (
          <SunIcon className="h-5 w-5" />
        ) : (
          <MoonIcon className="h-5 w-5" />
        )}
      </button>
    </header>
  )
}

export default Header
