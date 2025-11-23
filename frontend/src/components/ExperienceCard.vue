<template>
  <div class="relative pl-8 pb-8 border-l-2 border-primary-200 last:pb-0">
    <!-- Timeline dot -->
    <div class="absolute -left-[9px] top-0 w-4 h-4 rounded-full bg-primary-600 border-2 border-white shadow"></div>

    <div class="bg-white rounded-lg shadow-md p-5 hover:shadow-lg transition-shadow">
      <!-- Header -->
      <div class="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-2 mb-3">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-lg bg-primary-100 flex items-center justify-center flex-shrink-0">
            <svg class="w-5 h-5 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          </div>
          <div>
            <h3 class="text-lg font-bold text-gray-900">{{ experience.position }}</h3>
            <p class="text-primary-600 font-medium text-sm">{{ experience.company }}</p>
          </div>
        </div>
        <span class="text-gray-500 text-sm whitespace-nowrap flex items-center gap-1">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          {{ formatDate(experience.start_date) }} - {{ experience.current ? 'Atual' : formatDate(experience.end_date) }}
        </span>
      </div>

      <!-- Description -->
      <div class="mb-4">
        <p
          class="text-gray-600 text-sm leading-relaxed"
          :class="{ 'line-clamp-2': !expanded }"
        >
          {{ experience.description }}
        </p>
        <button
          v-if="isLongText"
          @click="expanded = !expanded"
          class="text-primary-600 text-sm font-medium mt-2 hover:text-primary-700 flex items-center gap-1"
        >
          {{ expanded ? 'Ver menos' : 'Ver mais' }}
          <svg
            class="w-4 h-4 transition-transform"
            :class="{ 'rotate-180': expanded }"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
      </div>

      <!-- Technologies -->
      <div class="flex flex-wrap gap-1.5">
        <span
          v-for="tech in experience.technologies"
          :key="tech"
          class="px-2 py-0.5 bg-gray-100 text-gray-600 rounded text-xs font-medium"
        >
          {{ tech }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  experience: {
    type: Object,
    required: true
  }
})

const expanded = ref(false)

const isLongText = computed(() => {
  return props.experience.description && props.experience.description.length > 150
})

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const [year, month] = dateStr.split('-')
  const months = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
  return `${months[parseInt(month) - 1]} ${year}`
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
