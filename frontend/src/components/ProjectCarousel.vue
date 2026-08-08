<template>
  <div
    class="carousel-root"
    tabindex="0"
    role="group"
    aria-roledescription="carousel"
    aria-label="Featured projects"
    @keydown.left.prevent="goPrev"
    @keydown.right.prevent="goNext"
    @pointerdown="onPointerDown"
    @pointermove="onPointerMove"
    @pointerup="onPointerUp"
    @pointercancel="onPointerUp"
  >
    <!-- Palco: cards empilhados, o ativo no centro -->
    <div class="stage">
      <div
        v-for="(project, i) in projects"
        :key="project.id"
        class="card"
        :style="cardStyle(i)"
      >
        <button
          class="card-btn"
          :tabindex="offsetOf(i) === 0 ? 0 : -1"
          :aria-hidden="Math.abs(offsetOf(i)) > 2"
          :aria-label="offsetOf(i) === 0 ? `Open details for ${project.title}` : `Go to ${project.title}`"
          @click="onCardClick(i)"
        >
          <ProjectCover :project="project" size="lg" />
          <span class="card-title">{{ project.title }}</span>
        </button>
      </div>
    </div>

    <!-- Controles -->
    <div class="controls">
      <button class="arrow" aria-label="Previous project (pauses autoplay)" @click="goPrev">
        <i class="pi pi-chevron-left"></i>
      </button>

      <div class="dots" role="tablist" aria-label="Select project">
        <button
          v-for="(project, i) in projects"
          :key="project.id"
          class="dot"
          role="tab"
          :class="{ 'dot-active': i === active }"
          :aria-selected="i === active"
          :aria-label="project.title"
          @click="goTo(i)"
        ></button>
      </div>

      <button class="arrow" aria-label="Next project" @click="goNext">
        <i class="pi pi-chevron-right"></i>
      </button>
    </div>

    <!-- Detalhe do ativo: troca junto com o carrossel, sem clique -->
    <div class="active-info" aria-live="polite">
      <Transition name="fade" mode="out-in">
        <div :key="current.id">
          <h3 class="active-title">{{ current.title }}</h3>
          <p class="active-desc">{{ current.description }}</p>
          <div class="active-techs">
            <span v-for="tech in current.technologies.slice(0, 5)" :key="tech" class="tech">{{ tech }}</span>
          </div>
        </div>
      </Transition>

      <!-- Vai direto para o projeto. O destino varia por projeto: rota interna,
           widget de chat do Dialogflow ou link externo. -->
      <button
        v-if="current.project_url === 'open-chat'"
        class="details-btn"
        @click="emit('open-chat')"
      >
        See project
        <i class="pi pi-arrow-right text-xs"></i>
      </button>

      <router-link
        v-else-if="isInternal(current.project_url)"
        :to="current.project_url"
        class="details-btn"
      >
        See project
        <i class="pi pi-arrow-right text-xs"></i>
      </router-link>

      <a
        v-else-if="current.project_url"
        :href="current.project_url"
        target="_blank"
        rel="noopener noreferrer"
        class="details-btn"
      >
        See project
        <i class="pi pi-external-link text-xs"></i>
      </a>

      <!-- Sem link ainda: cai no modal, que ao menos mostra techs e GitHub -->
      <button v-else class="details-btn" @click="emit('open', current)">
        See details
        <i class="pi pi-arrow-right text-xs"></i>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import ProjectCover from './ProjectCover.vue'

const props = defineProps({
  projects: { type: Array, required: true }
})

const emit = defineEmits(['open', 'open-chat'])

const isInternal = (url) => Boolean(url) && url.startsWith('/')

const active = ref(0)
const current = computed(() => props.projects[active.value])

/**
 * Distância do card `i` até o ativo, normalizada de forma circular.
 * Com 5 projetos os offsets caem sempre em [-2, 2], então os cinco
 * ficam visíveis ao mesmo tempo e o carrossel dá a volta sem pular.
 */
const offsetOf = (i) => {
  const n = props.projects.length
  let o = i - active.value
  if (o > n / 2) o -= n
  if (o < -n / 2) o += n
  return o
}

// Posição por distância do centro: deslocamento (% da largura), escala, opacidade, z-index, blur
const POS = [
  { x: 0, s: 1, o: 1, z: 30, b: 0 },
  { x: 66, s: 0.82, o: 0.7, z: 20, b: 0.5 },
  { x: 118, s: 0.66, o: 0.32, z: 10, b: 1.5 }
]

const cardStyle = (i) => {
  const offset = offsetOf(i)
  const pos = POS[Math.abs(offset)]

  // Mais de 2 de distância (só acontece com >5 projetos): esconde atrás do centro
  if (!pos) {
    return { transform: 'translateX(-50%) scale(0.5)', opacity: 0, zIndex: 0, pointerEvents: 'none' }
  }

  const dir = Math.sign(offset)
  return {
    transform: `translateX(calc(-50% + ${dir * pos.x}%)) scale(${pos.s})`,
    opacity: pos.o,
    zIndex: pos.z,
    filter: pos.b ? `blur(${pos.b}px)` : 'none'
  }
}

const next = () => { active.value = (active.value + 1) % props.projects.length }
const prev = () => { active.value = (active.value - 1 + props.projects.length) % props.projects.length }

/* ---- Autoplay: avança sozinho para a direita a cada 4s ---- */

const AUTOPLAY_MS = 4000
const playing = ref(true)
let timer = null

const restartTimer = () => {
  clearInterval(timer)
  if (playing.value) timer = setInterval(next, AUTOPLAY_MS)
}

// Voltar é o gesto de "quero olhar isso com calma": para o autoplay de vez.
const pauseAutoplay = () => {
  playing.value = false
  clearInterval(timer)
  timer = null
}

// Avançar/escolher no ponto não para nada, só reinicia a contagem
// dos 4s — senão o slide trocaria de novo logo depois do clique.
const goNext = () => { next(); restartTimer() }
const goPrev = () => { prev(); pauseAutoplay() }
const goTo = (i) => { active.value = i; restartTimer() }

onMounted(restartTimer)
onUnmounted(() => clearInterval(timer))

const onCardClick = (i) => {
  if (suppressClick) { suppressClick = false; return }
  if (offsetOf(i) === 0) emit('open', props.projects[i])
  else goTo(i)
}

// Arrastar / deslizar no touch
let startX = 0
let dragging = false
let suppressClick = false

const onPointerDown = (e) => {
  startX = e.clientX
  dragging = true
}

const onPointerMove = (e) => {
  if (!dragging) return
  const dx = e.clientX - startX
  if (Math.abs(dx) < 60) return
  dx < 0 ? goNext() : goPrev()
  dragging = false
  suppressClick = true // não abre o modal ao soltar o dedo
}

const onPointerUp = () => { dragging = false }
</script>

<style scoped>
.carousel-root {
  outline: none;
}

.carousel-root:focus-visible {
  outline: 2px solid #c8703f;
  outline-offset: 6px;
  border-radius: 1rem;
}

.stage {
  position: relative;
  height: 300px;
  touch-action: pan-y;
}

.card {
  position: absolute;
  top: 0;
  left: 50%;
  width: clamp(200px, 58vw, 320px);
  transition: transform 0.45s cubic-bezier(0.22, 0.61, 0.36, 1),
              opacity 0.45s ease,
              filter 0.45s ease;
  will-change: transform;
}

.card-btn {
  display: flex;
  flex-direction: column;
  width: 100%;
  text-align: left;
  border-radius: 0.75rem;
  overflow: hidden;
  background-color: var(--bg-card);
  border: 1px solid var(--border-color);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.28);
  cursor: pointer;
}

.card-title {
  padding: 0.75rem 0.875rem;
  font-size: 0.875rem;
  font-weight: 600;
  line-height: 1.3;
  color: var(--text-heading);
}

.controls {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.25rem;
  margin-top: 1.25rem;
}

.arrow {
  width: 2.25rem;
  height: 2.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 9999px;
  border: 1px solid var(--border-color);
  background-color: var(--bg-card);
  color: var(--accent-text);
  transition: background-color 0.2s ease, transform 0.2s ease;
}

.arrow:hover {
  background-color: rgba(200, 112, 63, 0.15);
  transform: scale(1.08);
}

.dots {
  display: flex;
  gap: 0.5rem;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 9999px;
  background-color: var(--border-color);
  transition: background-color 0.2s ease, width 0.2s ease;
}

.dot-active {
  width: 22px;
  background-color: #c8703f;
}

.active-info {
  margin-top: 1.25rem;
  text-align: center;
  max-width: 34rem;
  margin-left: auto;
  margin-right: auto;
  /* Altura reservada: as descrições variam muito de tamanho e sem isso
     os controles pulavam para cima e para baixo a cada troca de projeto. */
  min-height: 15rem;
}

.active-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--text-heading);
  margin-bottom: 0.5rem;
}

.active-desc {
  font-size: 0.875rem;
  line-height: 1.55;
  color: var(--text-muted);
  margin-bottom: 0.75rem;
  /* Texto completo, sem corte. A altura reservada cabe a descrição mais longa
     (~380 caracteres), para os controles não pularem ao trocar de projeto. */
  min-height: 6.8rem;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.active-techs {
  display: flex;
  flex-wrap: wrap;
  gap: 0.375rem;
  justify-content: center;
  margin-bottom: 0.875rem;
}

.tech {
  padding: 0.2rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.6875rem;
  font-weight: 500;
  color: var(--accent-text);
  background-color: rgba(200, 112, 63, 0.12);
  border: 1px solid rgba(200, 112, 63, 0.28);
}

.details-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  background-color: #c8703f;
  color: #1c1a17;
  transition: opacity 0.2s ease;
}

.details-btn:hover {
  opacity: 0.9;
}

@media (prefers-reduced-motion: reduce) {
  .card,
  .arrow,
  .dot,
  .fade-enter-active,
  .fade-leave-active {
    transition: none;
  }
}
</style>
