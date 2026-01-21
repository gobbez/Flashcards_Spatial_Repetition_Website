<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<template>
  <div class="home-container">
    <div class="hero">
      <h1>Spatial Repetition</h1>
      <p>Master your knowledge with scientifically proven dual-card learning.</p>
    </div>
    
    <div class="actions">
      <button @click="router.push('/study')" class="btn-start">
        Start Study session
      </button>
      
      <a href="http://localhost:8000/admin" target="_blank" class="btn-admin">
        Go to Django Admin
      </a>
    </div>

    <div class="stats-preview">
       <!-- We could add charts here later since 'charts' was mentioned in the spec -->
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
  margin-bottom: 4rem;
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
  gap: 1.5rem;
  width: 100%;
  max-width: 300px;
}

.btn-start {
  background: var(--color-primary);
  color: white;
  padding: 1.25rem;
  border-radius: 1rem;
  font-weight: 700;
  font-size: 1.1rem;
  border: none;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 10px 20px -5px rgba(124, 77, 255, 0.4);
}

.btn-start:hover {
  transform: translateY(-2px);
  box-shadow: 0 15px 30px -5px rgba(124, 77, 255, 0.5);
  filter: brightness(1.1);
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
</style>
