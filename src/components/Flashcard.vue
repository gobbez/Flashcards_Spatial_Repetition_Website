<script setup lang="ts">
import type { Flashcard } from '@/stores/flashcards'

defineProps<{
  card: Flashcard
  showBack: boolean
}>()
</script>

<template>
  <div class="flashcard-container">
    <div class="subject-tag">{{ card.subject_name }}</div>
    <div class="flashcard" :class="{ flipped: showBack }">
      <div class="front">
        <div class="content">{{ card.front }}</div>
        <div class="label">Front</div>
      </div>
      <div class="back">
        <div class="content">{{ card.back }}</div>
        <div class="label">Back</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.flashcard-container {
  perspective: 1000px;
  width: 100%;
  max-width: 600px;
  height: 400px; /* Fixed height for consistency */
  margin: 0 auto;
}

.subject-tag {
  text-align: center;
  font-size: 0.85rem;
  color: var(--color-primary);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 0.75rem;
  font-weight: 600;
  opacity: 0.8;
}

.flashcard {
  position: relative;
  width: 100%;
  height: 100%;
  text-align: center;
  transition: transform 0.6s;
  transform-style: preserve-3d;
  cursor: default;
}

.flashcard.flipped {
  transform: rotateY(180deg);
}

.front, .back {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  border-radius: var(--radius);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  box-shadow: var(--shadow-lg);
  background: var(--color-surface);
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.back {
  transform: rotateY(180deg);
  background: #1e293b; /* Slightly different shade or gradient? */
  border: 1px solid var(--color-primary);
}

.content {
  font-size: 1.5rem;
  font-weight: 500;
  margin-bottom: 1rem;
  line-height: 1.4;
  white-space: pre-wrap; /* Preserve newlines if any */
}

.label {
  position: absolute;
  bottom: 1rem;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--color-text-muted);
}
</style>
