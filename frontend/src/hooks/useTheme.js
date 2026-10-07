import { useEffect, useState } from 'react'

const THEME_STORAGE_KEY = 'documind-theme'

function readStoredTheme() {
  try {
    const stored = window.localStorage.getItem(THEME_STORAGE_KEY)

    return stored === 'light' || stored === 'dark' ? stored : null
  } catch {
    return null
  }
}

function writeStoredTheme(theme) {
  try {
    window.localStorage.setItem(THEME_STORAGE_KEY, theme)

    return true
  } catch {
    return false
  }
}

function getSystemTheme() {
  const prefersDark = window.matchMedia?.(
    '(prefers-color-scheme: dark)',
  )?.matches

  return prefersDark ? 'dark' : 'light'
}

function getInitialTheme() {
  return readStoredTheme() ?? getSystemTheme()
}

function applyTheme(theme) {
  document.documentElement.classList.toggle('dark', theme === 'dark')
}

function useTheme() {
  const [theme, setTheme] = useState(getInitialTheme)

  useEffect(() => {
    applyTheme(theme)
  }, [theme])

  function toggleTheme() {
    const nextTheme = theme === 'dark' ? 'light' : 'dark'

    writeStoredTheme(nextTheme)
    setTheme(nextTheme)
  }

  return { theme, toggleTheme }
}

export default useTheme
