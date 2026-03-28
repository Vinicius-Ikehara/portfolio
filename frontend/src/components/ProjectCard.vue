<template>
  <div class="h-full rounded-xl overflow-hidden transition-all hover:scale-105 flex flex-col" style="background-color: #1e293b; border: 1px solid #334155;">
    <!-- Header Image -->
    <div v-if="project.image_url" class="h-48 overflow-hidden">
      <img :src="project.image_url" :alt="project.title" class="w-full h-full object-cover" />
    </div>
    <!-- Pokedex Project Cover -->
    <div v-else-if="project.slug === 'pokedex'" class="h-48 flex items-center justify-center" style="background: linear-gradient(135deg, #e74c3c 0%, #c0392b 50%, #922b21 100%);">
      <svg class="w-24 h-24 opacity-50" viewBox="0 0 512 512">
        <circle cx="256" cy="256" r="256" fill="#FF6B6B"/>
        <path d="M256 0C145.929 0 52.094 69.472 15.923 166.957h480.154C459.906 69.472 366.071 0 256 0z" fill="#E85A5A"/>
        <circle cx="256" cy="256" r="256" fill="#FFFFFF" style="clip-path: polygon(0 50%, 100% 50%, 100% 100%, 0 100%)"/>
        <rect x="0" y="230" width="512" height="52" fill="#4A5568"/>
        <circle cx="256" cy="256" r="75" fill="#4A5568"/>
        <circle cx="256" cy="256" r="45" fill="#E5E5E5"/>
        <circle cx="256" cy="256" r="35" fill="#FFFFFF"/>
      </svg>
    </div>
    <!-- FAQ Bot Project Cover -->
    <div v-else-if="project.slug === 'faq-bot'" class="h-48 flex flex-col items-center justify-center gap-4" style="background: linear-gradient(135deg, #10b981 0%, #059669 50%, #047857 100%);">
      <div class="flex gap-3">
        <div class="w-16 h-16 rounded-full flex items-center justify-center" style="background-color: rgba(255, 255, 255, 0.2); backdrop-filter: blur(10px);">
          <i class="pi pi-comments text-3xl text-white"></i>
        </div>
        <div class="w-16 h-16 rounded-full flex items-center justify-center" style="background-color: rgba(255, 255, 255, 0.15); backdrop-filter: blur(10px);">
          <i class="pi pi-question-circle text-3xl text-white opacity-75"></i>
        </div>
      </div>
      <div class="text-white text-sm font-medium opacity-90">Powered by Dialogflow</div>
    </div>
    <!-- AI Ops Dashboard Project Cover -->
    <div v-else-if="project.slug === 'ai-ops'" class="h-48 flex items-center justify-center gap-6" style="background: linear-gradient(135deg, #4c1d95 0%, #1e1b4b 50%, #1e3a5f 100%);">
      <div class="flex items-center justify-center w-20 h-20 rounded-full" style="background-color: rgba(139, 92, 246, 0.2); border: 2px solid #8b5cf6;">
        <i class="pi pi-chart-line text-4xl" style="color: #8b5cf6;"></i>
      </div>
      <div class="flex flex-col gap-2">
        <div class="flex gap-2 items-end">
          <div class="h-10 w-8 rounded" style="background: linear-gradient(to top, #8b5cf6, #6d28d9);"></div>
          <div class="h-16 w-8 rounded" style="background: linear-gradient(to top, #3b82f6, #2563eb);"></div>
          <div class="h-12 w-8 rounded" style="background: linear-gradient(to top, #8b5cf6, #6d28d9);"></div>
          <div class="h-20 w-8 rounded" style="background: linear-gradient(to top, #3b82f6, #2563eb);"></div>
        </div>
      </div>
    </div>
    <!-- Acidentes H3 Project Cover -->
    <div v-else-if="project.slug === 'acidentes-h3'" class="h-48 flex items-center justify-center relative overflow-hidden" style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);">
      <!-- Road -->
      <div class="absolute inset-0">
        <div class="absolute left-1/2 -translate-x-1/2 h-full w-28" style="background: linear-gradient(180deg, #374151, #1f2937);"></div>
        <div class="absolute left-1/2 -translate-x-1/2 h-full w-0.5 opacity-50" style="background: repeating-linear-gradient(180deg, #fbbf24 0px, #fbbf24 12px, transparent 12px, transparent 24px);"></div>
      </div>
      <!-- Hexagon with warning sign -->
      <svg class="relative z-10" width="110" height="120" viewBox="0 0 110 120">
        <polygon points="55,5 100,27 100,72 55,95 10,72 10,27" fill="rgba(220,38,38,0.25)" stroke="#ef4444" stroke-width="2"/>
        <polygon points="55,18 88,35 88,65 55,82 22,65 22,35" fill="rgba(239,68,68,0.15)" stroke="rgba(239,68,68,0.4)" stroke-width="1"/>
        <!-- Warning triangle -->
        <polygon points="55,32 75,68 35,68" fill="none" stroke="#fbbf24" stroke-width="2.5" stroke-linejoin="round"/>
        <text x="55" y="62" text-anchor="middle" fill="#fbbf24" font-size="20" font-weight="bold">!</text>
        <!-- H3 label -->
        <text x="55" y="110" text-anchor="middle" fill="rgba(255,255,255,0.5)" font-size="11" font-family="monospace">H3</text>
      </svg>
    </div>
    <!-- Default Project Cover -->
    <div v-else class="h-48 flex items-center justify-center" style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 50%, #1d4ed8 100%);">
      <i class="pi pi-code text-6xl text-white opacity-40"></i>
    </div>

    <!-- Content -->
    <div class="p-6 flex flex-col flex-1">
      <div class="flex items-start justify-between gap-2 mb-3">
        <div class="flex items-start gap-2">
          <i class="pi pi-code text-lg" style="color: #38bdf8;"></i>
          <h3 class="text-xl font-bold" style="color: #ffffff;">{{ project.title }}</h3>
        </div>
        <!-- In Progress Badge -->
        <span
          v-if="project.status === 'in-progress'"
          class="px-3 py-1 rounded-full text-xs font-semibold whitespace-nowrap"
          style="background-color: rgba(251, 191, 36, 0.15); color: #fbbf24; border: 1px solid rgba(251, 191, 36, 0.3);"
        >
          <i class="pi pi-clock mr-1"></i>
          In Progress
        </span>
      </div>

      <p class="mb-4 leading-relaxed flex-1" style="color: #cbd5e1; min-height: 120px;">{{ project.description }}</p>

      <div class="flex flex-wrap gap-2 mb-4">
        <span
          v-for="tech in project.technologies"
          :key="tech"
          class="px-2 py-1 rounded text-xs font-medium"
          style="background-color: rgba(56, 189, 248, 0.15); color: #7dd3fc; border: 1px solid rgba(56, 189, 248, 0.3);"
        >
          {{ tech }}
        </span>
      </div>

      <div class="flex gap-3 pt-4" style="border-top: 1px solid #334155;">
        <!-- Coming Soon Badge (no buttons) -->
        <span
          v-if="project.comingSoon"
          class="flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium"
          style="background-color: rgba(251, 191, 36, 0.15); color: #fbbf24; border: 1px solid rgba(251, 191, 36, 0.3);"
        >
          <i class="pi pi-clock"></i>
          Coming Soon
        </span>
        <!-- Open Chat button -->
        <button
          v-else-if="project.project_url === 'open-chat'"
          @click="openChat"
          class="flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors hover:opacity-90"
          style="background-color: #0284c7; color: #ffffff;"
        >
          <i class="pi pi-comments"></i>
          Try it Now
        </button>
        <!-- Internal link (router-link) -->
        <router-link
          v-else-if="project.project_url && project.project_url.startsWith('/')"
          :to="project.project_url"
          class="flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors hover:opacity-90"
          style="background-color: #0284c7; color: #ffffff;"
        >
          <i class="pi pi-play"></i>
          Try it Now
        </router-link>
        <!-- External link -->
        <a
          v-else-if="project.project_url"
          :href="project.project_url"
          target="_blank"
          rel="noopener noreferrer"
          class="flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors"
          style="background-color: #0284c7; color: #ffffff;"
        >
          <i class="pi pi-external-link"></i>
          View Project
        </a>
        <a
          v-if="project.github_url && !project.comingSoon"
          :href="project.github_url"
          target="_blank"
          rel="noopener noreferrer"
          class="flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors"
          style="background-color: transparent; color: #cbd5e1; border: 1px solid #475569;"
        >
          <i class="pi pi-github"></i>
          GitHub
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  project: {
    type: Object,
    required: true
  }
})

const openChat = () => {
  // Procura pelo elemento do Dialogflow Messenger
  const dfMessenger = document.querySelector('df-messenger')
  if (!dfMessenger) return

  // Tenta múltiplas formas de abrir o chat
  if (dfMessenger.shadowRoot) {
    // Método 1: Procura pelo botão do chat bubble no shadow DOM
    const chatButton = dfMessenger.shadowRoot.querySelector('[opened]')
      ? null
      : dfMessenger.shadowRoot.querySelector('button, .chat-bubble-button, df-messenger-chat-bubble')

    if (chatButton) {
      chatButton.click()
      return
    }
  }

  // Método 2: Tenta abrir usando o atributo
  dfMessenger.setAttribute('opened', 'true')

  // Método 3: Dispara evento de clique no próprio elemento
  setTimeout(() => {
    dfMessenger.click()
  }, 100)
}
</script>
