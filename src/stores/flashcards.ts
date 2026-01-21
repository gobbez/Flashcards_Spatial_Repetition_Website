import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export interface Flashcard {
  id: number
  front: string
  back: string
  subject: number
  subject_name: string
  order: number
  last_seen: string
}

const API_BASE = import.meta.env.VITE_API_BASE || 'https://flashcardsspatialrepetition.pythonanywhere.com/api'

export const useFlashcardStore = defineStore('flashcards', () => {
  const cards = ref<Flashcard[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Fetch cards from backend
  async function fetchCards() {
    isLoading.value = true
    error.value = null
    try {
      const response = await fetch(`${API_BASE}/flashcards/`)
      if (!response.ok) throw new Error('Failed to fetch cards')
      const data = await response.json()
      cards.value = data
    } catch (err: any) {
      error.value = err.message
      console.error(err)
    } finally {
      isLoading.value = false
    }
  }

  // Get the current card (first in the ordered list)
  const currentCard = computed(() => {
    return cards.value.length > 0 ? cards.value[0] : null
  })

  // Process the current card with a given rating via API
  async function processCard(rating: 'study_more' | 'so_so' | 'understood') {
    if (!currentCard.value) return

    const cardId = currentCard.value.id
    try {
      const response = await fetch(`${API_BASE}/flashcards/${cardId}/rate/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ rating }),
      })

      if (!response.ok) throw new Error('Failed to update card rating')
      
      // Re-fetch all cards to get the new order from backend
      await fetchCards()
      
    } catch (err: any) {
      error.value = err.message
      console.error(err)
    }
  }

  return { 
    cards, 
    isLoading,
    error,
    currentCard,
    fetchCards, 
    processCard 
  }
})
