const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || 'http://localhost:3000/api'

export const GENERIC_ERROR_MESSAGE =
  'Unable to get a response. Please try again.'

export async function sendChatMessage(messages, documentIds) {
  let response

  try {
    response = await fetch(`${API_BASE_URL}/ai/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        messages,
        document_ids: documentIds,
      }),
    })
  } catch (error) {
    throw new Error('Network error: the server could not be reached.', {
      cause: error,
    })
  }

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`)
  }

  let data

  try {
    data = await response.json()
  } catch (error) {
    throw new Error('The server returned an invalid response.', {
      cause: error,
    })
  }

  if (!data || typeof data.answer !== 'string' || !data.answer.trim()) {
    throw new Error('The server returned an empty response.')
  }

  return {
    answer: data.answer,
    sources: Array.isArray(data.sources) ? data.sources : [],
  }
}
