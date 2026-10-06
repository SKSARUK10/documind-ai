const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:3000/api";

export async function getDocuments() {
  const response = await fetch(
    `${API_BASE_URL}/documents`
  )

  if (!response.ok){
     throw new Error("Failed to load documents");
  }
   return response.json();
}

export async function uploadDocument(file) {
  const formData = new FormData()

  formData.append('file', file)

  const response = await fetch(
    `${API_BASE_URL}/documents/upload`,
    {
      method: 'POST',
      body: formData,
    },
  )

  if (!response.ok) {
    throw new Error('Failed to upload document')
  }

  return response.json()
}