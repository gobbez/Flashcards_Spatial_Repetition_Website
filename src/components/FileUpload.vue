<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useFlashcardStore, type Flashcard } from '@/stores/flashcards'

const store = useFlashcardStore()
const router = useRouter()
const fileInput = ref<HTMLInputElement | null>(null)
const file = ref<File | null>(null)
const error = ref<string | null>(null)

function triggerInput() {
  fileInput.value?.click()
}

function handleFileChange(event: Event) {
  const target = event.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    file.value = target.files[0]
    error.value = null
  }
}

function handleDrop(event: DragEvent) {
  if (event.dataTransfer?.files && event.dataTransfer.files.length > 0) {
    const droppedFile = event.dataTransfer.files[0]
    if (droppedFile.type === 'text/plain' || droppedFile.name.endsWith('.txt')) {
      file.value = droppedFile
      error.value = null
    } else {
      error.value = 'Please upload a .txt file'
    }
  }
}

async function processFile() {
  if (!file.value) return

  const text = await file.value.text()
  parseAndLoad(text)
}

function parseAndLoad(content: string) {
  const lines = content.split('\n')
  const cards: Flashcard[] = []
  
  let currentFront: string | null = null
  let currentBack: string | null = null

  // Regex to match "F: content" or 'F: "content"'
  // We want to capture everything after "X:" handling optional quotes
  const parseLine = (line: string, prefix: string) => {
    const trimmed = line.trim()
    if (!trimmed.startsWith(prefix)) return null
    
    let content = trimmed.substring(prefix.length).trim()
    // Remove surrounding quotes if present
    if (content.startsWith('"') && content.endsWith('"')) {
      content = content.slice(1, -1)
    }
    return content
  }

  for (const line of lines) {
    if (!line.trim()) continue

    const front = parseLine(line, 'F:')
    if (front) {
      currentFront = front
      currentBack = null // Reset back
      continue
    }

    const back = parseLine(line, 'B:')
    if (back && currentFront) {
      currentBack = back
      cards.push({
        id: crypto.randomUUID(),
        front: currentFront,
        back: currentBack
      })
      // Reset for next pair
      currentFront = null
      currentBack = null
    }
  }

  if (cards.length === 0) {
    error.value = 'No valid flashcards found. Check the file format.'
    return
  }

  store.loadCards(cards)
  router.push('/study')
}
</script>

<template>
  <div class="upload-wrapper">
    <div class="card glass">
      <h1>Upload Flashcards</h1>
      <p class="subtitle">Upload your .txt file to start training</p>

      <div 
        class="drop-zone" 
        :class="{ 'has-file': file }"
        @click="triggerInput" 
        @drop.prevent="handleDrop" 
        @dragover.prevent
      >
        <div v-if="!file" class="placeholder">
          <span class="icon">📄</span>
          <span>Click or Drag & Drop .txt file here</span>
        </div>
        <div v-else class="file-info">
          <span class="icon">✅</span>
          <span>{{ file.name }}</span>
        </div>
        
        <input 
          type="file" 
          ref="fileInput" 
          accept=".txt" 
          class="hidden-input"
          @change="handleFileChange"
        >
      </div>

      <div v-if="error" class="error-msg">
        {{ error }}
      </div>

      <button 
        class="btn-primary" 
        :disabled="!file" 
        @click="processFile"
      >
        Start Studying
      </button>
    </div>
  </div>
</template>

<style scoped>
.upload-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  flex: 1;
  padding: 2rem;
}

.card {
  background: var(--color-surface);
  padding: 3rem;
  border-radius: var(--radius);
  box-shadow: var(--shadow-lg);
  max-width: 500px;
  width: 100%;
  text-align: center;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.glass {
  background: rgba(30, 41, 59, 0.7);
  backdrop-filter: blur(10px);
}

h1 {
  margin-bottom: 0.5rem;
  font-size: 2rem;
  background: linear-gradient(135deg, #60a5fa, #a855f7);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.subtitle {
  color: var(--color-text-muted);
  margin-bottom: 2rem;
}

.drop-zone {
  border: 2px dashed var(--color-text-muted);
  border-radius: var(--radius);
  padding: 3rem 2rem;
  cursor: pointer;
  margin-bottom: 2rem;
  transition: all 0.2s;
}

.drop-zone:hover, .drop-zone.has-file {
  border-color: var(--color-primary);
  background: rgba(59, 130, 246, 0.1);
}

.placeholder, .file-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.icon {
  font-size: 2rem;
}

.hidden-input {
  display: none;
}

.btn-primary {
  background: var(--color-primary);
  color: white;
  padding: 1rem 2rem;
  border-radius: var(--radius);
  font-size: 1.1rem;
  font-weight: 600;
  width: 100%;
  transition: background 0.2s;
}

.btn-primary:hover:not(:disabled) {
  background: var(--color-primary-hover);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.error-msg {
  color: var(--color-danger);
  margin-bottom: 1rem;
}
</style>
