import { ref } from 'vue'
import { defineStore } from 'pinia'

export interface Quiz {
  id: number
  question: string
  answer1: string
  answer2: string
  answer3: string
  answer4: string
  solution: number
  subject: number
  subject_name: string
  points: number
}

const API_BASE = import.meta.env.VITE_API_BASE || 'https://flashcardsspatialrepetition.pythonanywhere.com/api'

export const useQuizStore = defineStore('quiz', () => {
  const currentQuiz = ref<Quiz | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  async function fetchRandomQuiz() {
    isLoading.value = true
    error.value = null
    try {
      const response = await fetch(`${API_BASE}/quizzes/random/`)
      if (!response.ok) throw new Error('Failed to fetch random quiz')
      const data = await response.json()
      currentQuiz.value = data
    } catch (err: any) {
      error.value = err.message
      console.error(err)
    } finally {
      isLoading.value = false
    }
  }

  async function submitAnswer(answer: number) {
    if (!currentQuiz.value) return null

    try {
      const response = await fetch(`${API_BASE}/quizzes/${currentQuiz.value.id}/submit_answer/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ answer }),
      })

      if (!response.ok) throw new Error('Failed to submit answer')
      return await response.json()
    } catch (err: any) {
      error.value = err.message
      console.error(err)
      return null
    }
  }

  async function uploadFile(file: File, type: 'flashcards' | 'quizzes', subject: string) {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('subject', subject)

    const endpoint = type === 'flashcards' ? 'flashcards/upload/' : 'quizzes/upload/'
    
    try {
      const response = await fetch(`${API_BASE}/${endpoint}`, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) throw new Error('Failed to upload file')
      return await response.json()
    } catch (err: any) {
      error.value = err.message
      console.error(err)
      throw err
    }
  }

  return {
    currentQuiz,
    isLoading,
    error,
    fetchRandomQuiz,
    submitAnswer,
    uploadFile
  }
})
