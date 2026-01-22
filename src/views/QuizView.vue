<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuizStore } from '../stores/quiz'

const router = useRouter()
const quizStore = useQuizStore()

const selectedAnswer = ref<number | null>(null)
const result = ref<{ correct: boolean; solution: number } | null>(null)

async function loadNewQuiz() {
  selectedAnswer.value = null
  result.value = null
  await quizStore.fetchRandomQuiz()
}

async function handleAnswer(index: number) {
  if (selectedAnswer.value !== null) return
  
  selectedAnswer.value = index
  const res = await quizStore.submitAnswer(index)
  if (res) {
    result.value = {
      correct: res.correct,
      solution: res.solution
    }
  }
}

onMounted(() => {
  quizStore.fetchRandomQuiz()
})
</script>

<template>
  <div class="quiz-container">
    <div class="header">
      <button @click="router.push('/')" class="btn-back">← Back</button>
      <div v-if="quizStore.currentQuiz" class="subject-tag">
        {{ quizStore.currentQuiz.subject_name }}
      </div>
    </div>

    <div v-if="quizStore.isLoading" class="loading">
      <div class="spinner"></div>
      <p>Loading random quiz...</p>
    </div>

    <div v-else-if="quizStore.error" class="error">
      <p>{{ quizStore.error }}</p>
      <button @click="loadNewQuiz" class="btn-retry">Retry</button>
    </div>

    <div v-else-if="quizStore.currentQuiz" class="quiz-card">
      <div class="question">
        <h2>{{ quizStore.currentQuiz.question }}</h2>
      </div>

      <div class="answers-grid">
        <button 
          v-for="i in 4" 
          :key="i"
          @click="handleAnswer(i)"
          class="answer-btn"
          :class="{
            'correct': result && i === result.solution,
            'wrong': result && selectedAnswer === i && !result.correct,
            'selected': selectedAnswer === i,
            'disabled': selectedAnswer !== null
          }"
        >
          <span class="index">{{ i }}</span>
          <span class="text">{{ (quizStore.currentQuiz as any)[`answer${i}`] }}</span>
        </button>
      </div>

      <div v-if="result" class="feedback">
        <p v-if="result.correct" class="success-msg">Correct! +{{ quizStore.currentQuiz.points }} points</p>
        <p v-else class="error-msg">Better luck next time!</p>
        
        <button @click="loadNewQuiz" class="btn-next">Next quiz</button>
      </div>
    </div>
    
    <div v-else class="empty">
      <p>No quizzes available. Go to Django Admin to add some!</p>
    </div>
  </div>
</template>

<style scoped>
.quiz-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
  min-height: 100vh;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.btn-back {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: var(--color-text-muted);
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-back:hover {
  background: rgba(255, 255, 255, 0.05);
  color: var(--color-text);
}

.subject-tag {
  background: rgba(124, 77, 255, 0.1);
  color: var(--color-primary);
  padding: 0.25rem 0.75rem;
  border-radius: 2rem;
  font-size: 0.85rem;
  font-weight: 600;
  border: 1px solid rgba(124, 77, 255, 0.2);
}

.quiz-card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 2rem;
  padding: 3rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

.question h2 {
  font-size: 2rem;
  margin-bottom: 3rem;
  text-align: center;
  line-height: 1.4;
}

.answers-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.answer-btn {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: var(--color-text);
  padding: 1.5rem;
  border-radius: 1rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  text-align: left;
  font-size: 1.1rem;
}

.answer-btn:not(.disabled):hover {
  background: rgba(255, 255, 255, 0.08);
  transform: translateY(-2px);
  border-color: var(--color-primary);
}

.answer-btn.correct {
  background: rgba(74, 222, 128, 0.1);
  border-color: #4ade80;
  box-shadow: 0 0 20px rgba(74, 222, 128, 0.2);
}

.answer-btn.wrong {
  background: rgba(248, 113, 113, 0.1);
  border-color: #f87171;
}

.answer-btn.selected {
  border-width: 2px;
}

.answer-btn.disabled {
  cursor: default;
}

.index {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  font-size: 0.9rem;
  font-weight: 700;
}

.feedback {
  margin-top: 3rem;
  text-align: center;
  animation: fadeIn 0.5s ease-out;
}

.success-msg {
  color: #4ade80;
  font-weight: 700;
  font-size: 1.25rem;
  margin-bottom: 2rem;
}

.error-msg {
  color: #f87171;
  font-weight: 700;
  font-size: 1.25rem;
  margin-bottom: 2rem;
}

.btn-next {
  background: var(--color-primary);
  color: white;
  padding: 1rem 2.5rem;
  border-radius: 1rem;
  font-weight: 700;
  border: none;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 1.1rem;
}

.btn-next:hover {
  transform: scale(1.05);
  box-shadow: 0 10px 20px rgba(124, 77, 255, 0.3);
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.loading, .empty, .error {
  text-align: center;
  padding: 4rem;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(255, 255, 255, 0.1);
  border-left-color: var(--color-primary);
  border-radius: 50%;
  margin: 0 auto 1.5rem;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 600px) {
  .answers-grid {
    grid-template-columns: 1fr;
  }
}
</style>
