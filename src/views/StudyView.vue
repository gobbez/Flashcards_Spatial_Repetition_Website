<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useFlashcardStore } from '@/stores/flashcards'
import FlashcardComponent from '@/components/Flashcard.vue'

const store = useFlashcardStore()
const router = useRouter()

const showBack = ref(false)

const currentCard = computed(() => store.currentCard)

function toggleSide() {
  showBack.value = !showBack.value
}

function rate(rating: 'understood' | 'so_so' | 'study_more') {
  store.processCard(rating)
  showBack.value = false
}

// Redirect if no cards
onMounted(() => {
  if (store.cards.length === 0) {
    router.push('/')
  }
})

function downloadCards() {
  const content = store.queue.map(card => {
    return `F: "${card.front}"\nB: "${card.back}"`
  }).join('\n\n')
  
  const blob = new Blob([content], { type: 'text/plain' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `flashcards_session_${new Date().toISOString().slice(0, 10)}.txt`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}
</script>

<template>
  <div class="study-container">
    <header>
      <div class="progress">
        Queue: {{ store.queue.length }} cards
      </div>
      <div class="actions">
        <button class="btn-icon" @click="downloadCards" title="Download Flashcards">⬇️</button>
        <button class="btn-icon" @click="router.push('/')" title="Exit">✕</button>
      </div>
    </header>

    <main v-if="currentCard">
      <FlashcardComponent 
        :card="currentCard" 
        :show-back="showBack" 
      />

      <div class="controls">
        <button class="btn-toggle" @click="toggleSide">
          {{ showBack ? 'Show Front' : 'Show Back' }}
        </button>

        <div class="ratings">
          <button @click="rate('understood')" class="btn-rate success">
            Understood
            <span class="hint">~90%</span>
          </button>
          <button @click="rate('so_so')" class="btn-rate warning">
            So and So
            <span class="hint">~30%</span>
          </button>
          <button @click="rate('study_more')" class="btn-rate danger">
            Study More
            <span class="hint">~10%</span>
          </button>
        </div>
      </div>
    </main>
    
    <div v-else class="empty-state">
      <h2>Session Complete!</h2>
      <button @click="router.push('/')" class="btn-primary">Upload New File</button>
    </div>
  </div>
</template>

<style scoped>
.study-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  padding: 1rem;
  max-width: 800px;
  margin: 0 auto;
  width: 100%;
}

header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding: 1rem 0;
}

.progress {
  font-weight: 600;
  color: var(--color-primary);
}

.actions {
  display: flex;
  gap: 1rem;
}

.btn-icon {
  background: transparent;
  color: var(--color-text-muted);
  font-size: 1.5rem;
  padding: 0.5rem;
}

.controls {
  margin-top: 3rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
}

.btn-toggle {
  background: var(--color-surface);
  color: var(--color-text);
  padding: 1rem 3rem;
  border-radius: 2rem;
  font-weight: 600;
  border: 1px solid var(--color-text-muted);
  transition: all 0.2s;
}

.btn-toggle:hover {
  background: var(--color-text);
  color: var(--color-background);
}

.ratings {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  width: 100%;
}

.btn-rate {
  padding: 1rem;
  border-radius: var(--radius);
  font-weight: 600;
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
  transition: transform 0.1s, filter 0.2s;
}

.btn-rate:active {
  transform: scale(0.95);
}

.btn-rate:hover {
  filter: brightness(1.1);
}

.success { background-color: var(--color-success); }
.warning { background-color: var(--color-warning); }
.danger { background-color: var(--color-danger); }

.hint {
  font-size: 0.75rem;
  opacity: 0.8;
  font-weight: normal;
}

.empty-state {
  text-align: center;
  margin-top: 5rem;
}
</style>
