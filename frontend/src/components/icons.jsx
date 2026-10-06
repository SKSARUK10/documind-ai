const baseProps = {
  viewBox: '0 0 24 24',
  fill: 'none',
  stroke: 'currentColor',
  strokeWidth: 2,
  strokeLinecap: 'round',
  strokeLinejoin: 'round',
  'aria-hidden': 'true',
}

export function MenuIcon({ className }) {
  return (
    <svg className={className} {...baseProps}>
      <path d="M4 6h16M4 12h16M4 18h16" />
    </svg>
  )
}

export function CloseIcon({ className }) {
  return (
    <svg className={className} {...baseProps}>
      <path d="M6 6l12 12M18 6L6 18" />
    </svg>
  )
}

export function PlusIcon({ className }) {
  return (
    <svg className={className} {...baseProps}>
      <path d="M12 5v14M5 12h14" />
    </svg>
  )
}

export function FileIcon({ className }) {
  return (
    <svg className={className} {...baseProps}>
      <path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z" />
      <path d="M14 3v5h5" />
    </svg>
  )
}

export function ChevronIcon({ className }) {
  return (
    <svg className={className} {...baseProps}>
      <path d="m6 9 6 6 6-6" />
    </svg>
  )
}

export function SendIcon({ className }) {
  return (
    <svg className={className} {...baseProps}>
      <path d="M12 19V5M5 12l7-7 7 7" />
    </svg>
  )
}

export function AlertIcon({ className }) {
  return (
    <svg className={className} {...baseProps}>
      <path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z" />
      <path d="M12 9v4M12 17h.01" />
    </svg>
  )
}
