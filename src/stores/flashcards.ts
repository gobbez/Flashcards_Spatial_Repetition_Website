import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export interface Flashcard {
  id: string
  front: string
  back: string
}

export const useFlashcardStore = defineStore('flashcards', () => {
  const cards = ref<Flashcard[]>([])
  const queue = ref<Flashcard[]>([])

  // Load new cards and reset queue
  function loadCards(newCards: Flashcard[]) {
    cards.value = newCards
    queue.value = [...newCards]
  }

  // Get the next card in line (without removing it yet, usually used for display)
  const currentCard = computed(() => {
    return queue.value.length > 0 ? queue.value[0] : null
  })

  // Process the current card with a given rating
  // rating: 'study_more' (10%), 'so_so' (30%), 'understood' (90%)
  function processCard(rating: 'study_more' | 'so_so' | 'understood') {
    const card = queue.value.shift()
    if (!card) return

    let percentile = 0.5
    switch (rating) {
        case 'study_more':
            percentile = 0.1
            break
        case 'so_so':
            percentile = 0.3
            break
        case 'understood':
            percentile = 0.9
            break
    }

    // Calculate insert index
    // We insert into the REMAINING queue. 
    // Example: 100 cards. shift -> 99 cards. 
    // 10% -> index 9.
    const index = Math.floor(queue.value.length * percentile)
    
    // Insert
    queue.value.splice(index, 0, card)
  }

  return { 
    cards, 
    queue, 
    currentCard,
    loadCards, 
    processCard 
  }
})
