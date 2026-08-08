<template>
  <!-- Header Image -->
  <div v-if="project.image_url" :class="[s.height, 'overflow-hidden']">
    <img :src="project.image_url" :alt="project.title" class="w-full h-full object-cover" />
  </div>

  <!-- Pokedex Project Cover -->
  <div
    v-else-if="project.slug === 'pokedex'"
    :class="[s.height, 'flex items-center justify-center']"
    style="background: linear-gradient(135deg, #e74c3c 0%, #c0392b 50%, #922b21 100%);"
  >
    <svg :class="[s.pokeball, 'opacity-50']" viewBox="0 0 512 512">
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
  <div
    v-else-if="project.slug === 'faq-bot'"
    :class="[s.height, 'flex flex-col items-center justify-center gap-2']"
    style="background: linear-gradient(135deg, #10b981 0%, #059669 50%, #047857 100%);"
  >
    <div class="flex gap-2">
      <div :class="[s.bubble, 'rounded-full flex items-center justify-center']" style="background-color: rgba(255,255,255,0.2); backdrop-filter: blur(10px);">
        <i class="pi pi-comments text-white" :class="s.bubbleIcon"></i>
      </div>
      <div :class="[s.bubble, 'rounded-full flex items-center justify-center']" style="background-color: rgba(255,255,255,0.15); backdrop-filter: blur(10px);">
        <i class="pi pi-question-circle text-white opacity-75" :class="s.bubbleIcon"></i>
      </div>
    </div>
    <div v-if="size === 'lg'" class="text-white text-sm font-medium opacity-90">Powered by Dialogflow</div>
  </div>

  <!-- AI Ops Dashboard Project Cover -->
  <div
    v-else-if="project.slug === 'ai-ops'"
    :class="[s.height, 'flex items-center justify-center']"
    :style="`background: linear-gradient(135deg, #4c1d95 0%, #1e1b4b 50%, #1e3a5f 100%); gap: ${s.gap};`"
  >
    <div :class="[s.aiCircle, 'flex items-center justify-center rounded-full']" style="background-color: rgba(139, 92, 246, 0.2); border: 2px solid #8b5cf6;">
      <i class="pi pi-chart-line" :class="s.aiIcon" style="color: #8b5cf6;"></i>
    </div>
    <div class="flex gap-1.5 items-end">
      <div :class="[s.barW, s.bar1]" style="background: linear-gradient(to top, #8b5cf6, #6d28d9); border-radius: 2px;"></div>
      <div :class="[s.barW, s.bar2]" style="background: linear-gradient(to top, #3b82f6, #2563eb); border-radius: 2px;"></div>
      <div :class="[s.barW, s.bar3]" style="background: linear-gradient(to top, #8b5cf6, #6d28d9); border-radius: 2px;"></div>
      <div :class="[s.barW, s.bar4]" style="background: linear-gradient(to top, #3b82f6, #2563eb); border-radius: 2px;"></div>
    </div>
  </div>

  <!-- Acidentes H3 Project Cover -->
  <div
    v-else-if="project.slug === 'acidentes-h3'"
    :class="[s.height, 'flex items-center justify-center relative overflow-hidden']"
    style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);"
  >
    <!-- Road -->
    <div class="absolute inset-0">
      <div :class="[s.road, 'absolute left-1/2 -translate-x-1/2 h-full']" style="background: linear-gradient(180deg, #374151, #1f2937);"></div>
      <div class="absolute left-1/2 -translate-x-1/2 h-full w-0.5 opacity-50" style="background: repeating-linear-gradient(180deg, #fbbf24 0px, #fbbf24 12px, transparent 12px, transparent 24px);"></div>
    </div>
    <!-- Hexagon with warning sign -->
    <svg class="relative z-10" :width="s.hexSize" :height="s.hexSize * 1.083" viewBox="0 0 120 130">
      <polygon points="60,5 108,30 108,80 60,105 12,80 12,30" fill="rgba(220,38,38,0.25)" stroke="#ef4444" stroke-width="2"/>
      <polygon points="60,30 85,72 35,72" fill="none" stroke="#fbbf24" stroke-width="2.5" stroke-linejoin="round"/>
      <text x="60" y="66" text-anchor="middle" fill="#fbbf24" font-size="22" font-weight="bold">!</text>
      <text x="60" y="122" text-anchor="middle" fill="rgba(255,255,255,0.5)" font-size="12" font-family="monospace">H3</text>
    </svg>
  </div>

  <!-- Default Project Cover -->
  <div v-else :class="[s.height, 'flex items-center justify-center']" style="background: linear-gradient(135deg, #c8703f 0%, #874726 100%);">
    <i class="pi pi-code text-white opacity-40" :class="s.defaultIcon"></i>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  project: { type: Object, required: true },
  size: { type: String, default: 'lg' } // 'lg' | 'md' | 'sm'
})

const scales = {
  lg: {
    height: 'h-48', pokeball: 'w-24 h-24', bubble: 'w-16 h-16', bubbleIcon: 'text-3xl',
    gap: '1.5rem', aiCircle: 'w-20 h-20', aiIcon: 'text-4xl',
    barW: 'w-8', bar1: 'h-10', bar2: 'h-16', bar3: 'h-12', bar4: 'h-20',
    road: 'w-28', hexSize: 120, defaultIcon: 'text-6xl'
  },
  md: {
    height: 'h-28', pokeball: 'w-14 h-14', bubble: 'w-11 h-11', bubbleIcon: 'text-xl',
    gap: '1rem', aiCircle: 'w-12 h-12', aiIcon: 'text-2xl',
    barW: 'w-5', bar1: 'h-6', bar2: 'h-10', bar3: 'h-8', bar4: 'h-12',
    road: 'w-16', hexSize: 72, defaultIcon: 'text-4xl'
  },
  sm: {
    height: 'h-36', pokeball: 'w-14 h-14', bubble: 'w-10 h-10', bubbleIcon: 'text-lg',
    gap: '0.75rem', aiCircle: 'w-11 h-11', aiIcon: 'text-xl',
    barW: 'w-3', bar1: 'h-4', bar2: 'h-7', bar3: 'h-6', bar4: 'h-9',
    road: 'w-12', hexSize: 60, defaultIcon: 'text-3xl'
  }
}

const s = computed(() => scales[props.size] || scales.lg)
</script>
