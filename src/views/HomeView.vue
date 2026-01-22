<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useQuizStore } from '../stores/quiz'

const router = useRouter()
const quizStore = useQuizStore()

const uploadType = ref<'flashcards' | 'quizzes'>('flashcards')
const uploadSubject = ref('General')
const fileInput = ref<HTMLInputElement | null>(null)
const uploadMessage = ref('')
const isUploading = ref(false)

async function handleFileUpload() {
  const file = fileInput.value?.files?.[0]
  if (!file) {
    uploadMessage.value = 'Please select a file first.'
    return
  }

  isUploading.value = true
  uploadMessage.value = 'Uploading...'
  
  try {
    const res = await quizStore.uploadFile(
      file,
      uploadType.value,
      uploadSubject.value
    )
    uploadMessage.value = res.message || 'Successfully uploaded!'
    if (fileInput.value) {
      fileInput.value.value = '' // Clear input
    }
  } catch (err: any) {
    uploadMessage.value = `Error: ${err.message}`
  } finally {
    isUploading.value = false
  }
}
</script>

<template>
  <div class="home-container">
    <div class="hero">
      <h1>Spatial Repetition</h1>
      <p>Master your knowledge with scientifically proven dual-card learning.</p>
    </div>
    
    <div class="actions">
      <button @click="router.push('/study')" class="btn-primary">
        Start Study session
      </button>

      <button @click="router.push('/quiz')" class="btn-secondary">
        Start Quiz
      </button>
      
      <a href="http://localhost:8000/admin" target="_blank" class="btn-admin">
        Go to Django Admin
      </a>
    </div>

    <div class="upload-section">
      <h3>Quick Upload</h3>
      <div class="upload-controls">
        <select v-model="uploadType" class="upload-select">
          <option value="flashcards">Flashcards</option>
          <option value="quizzes">Quizzes</option>
        </select>
        
        <input 
          v-model="uploadSubject" 
          type="text" 
          placeholder="Subject name"
          class="upload-input"
        >
      </div>

      <div class="file-drop">
        <input 
          type="file" 
          ref="fileInput" 
          accept=".txt"
          @change="handleFileUpload"
          id="file-upload"
          class="hidden-input"
        >
        <label for="file-upload" class="file-label">
          <span v-if="!isUploading">Click to upload .txt file</span>
          <span v-else>Uploading...</span>
        </label>
      </div>
      
      <p v-if="uploadMessage" class="upload-status" :class="{ error: uploadMessage.includes('Error') }">
        {{ uploadMessage }}
      </p>
    </div>
  </div>
</template>

<style scoped>
.home-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  background: radial-gradient(circle at top right, rgba(124, 77, 255, 0.05) 0%, transparent 40%),
              radial-gradient(circle at bottom left, rgba(0, 255, 231, 0.05) 0%, transparent 40%);
}

.hero {
  text-align: center;
  margin-bottom: 3rem;
}

h1 {
  font-size: 4rem;
  font-weight: 800;
  margin-bottom: 1rem;
  background: linear-gradient(135deg, var(--color-primary), #a78bfa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

p {
  font-size: 1.25rem;
  color: var(--color-text-muted);
  max-width: 500px;
}

.actions {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  width: 100%;
  max-width: 350px;
  margin-bottom: 4rem;
}

.btn-primary, .btn-secondary {
  padding: 1.25rem;
  border-radius: 1rem;
  font-weight: 700;
  font-size: 1.1rem;
  border: none;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.btn-primary {
  background: var(--color-primary);
  color: white;
  box-shadow: 0 10px 20px -5px rgba(124, 77, 255, 0.4);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 15px 30px -5px rgba(124, 77, 255, 0.5);
  filter: brightness(1.1);
}

.btn-secondary {
  background: rgba(124, 77, 255, 0.1);
  color: var(--color-primary);
  border: 1px solid rgba(124, 77, 255, 0.2);
}

.btn-secondary:hover {
  background: rgba(124, 77, 255, 0.2);
  transform: translateY(-2px);
}

.btn-admin {
  text-align: center;
  padding: 1rem;
  border-radius: 1rem;
  font-weight: 600;
  color: var(--color-text-muted);
  text-decoration: none;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s;
}

.btn-admin:hover {
  background: rgba(255, 255, 255, 0.05);
  color: var(--color-text);
  border-color: rgba(255, 255, 255, 0.2);
}

.upload-section {
  width: 100%;
  max-width: 450px;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 1.5rem;
  text-align: center;
}

.upload-section h3 {
  margin-bottom: 1.5rem;
  font-size: 1.25rem;
  color: var(--color-text-muted);
}

.upload-controls {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.upload-select, .upload-input {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: var(--color-text);
  padding: 0.75rem;
  border-radius: 0.75rem;
  outline: none;
}

.upload-select {
  flex: 1;
}

.upload-input {
  flex: 2;
}

.file-drop {
  border: 2px dashed rgba(255, 255, 255, 0.1);
  border-radius: 1rem;
  transition: all 0.3s;
}

.file-drop:hover {
  border-color: var(--color-primary);
  background: rgba(124, 77, 255, 0.03);
}

.hidden-input {
  display: none;
}

.file-label {
  display: block;
  padding: 2rem;
  cursor: pointer;
  color: var(--color-text-muted);
  font-weight: 500;
}

.upload-status {
  margin-top: 1rem;
  font-size: 0.9rem;
  color: var(--color-success);
}

.upload-status.error {
  color: var(--color-danger);
}
</style>
