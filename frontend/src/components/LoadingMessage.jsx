function LoadingMessage() {
  return (
    <div className="flex gap-3" role="status">
      <span
        aria-hidden="true"
        className="mt-1 flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-indigo-600 text-white"
      >
        <span className="h-2 w-2 animate-ping rounded-full bg-white" />
      </span>
      <div className="rounded-2xl rounded-tl-md border border-slate-200 bg-white px-4 py-3 text-sm text-slate-500 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-400">
        Thinking...
      </div>
    </div>
  )
}

export default LoadingMessage
