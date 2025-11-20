<template>
  <div class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
    <div class="flex justify-between items-start mb-3">
      <div>
        <h3 class="text-xl font-bold text-gray-900">{{ experience.position }}</h3>
        <p class="text-primary-600 font-medium">{{ experience.company }}</p>
      </div>
      <span class="text-gray-500 text-sm">
        {{ formatDate(experience.start_date) }} - {{ experience.current ? 'Atual' : formatDate(experience.end_date) }}
      </span>
    </div>

    <p class="text-gray-700 mb-4">{{ experience.description }}</p>

    <div class="flex flex-wrap gap-2">
      <span
        v-for="tech in experience.technologies"
        :key="tech"
        class="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm"
      >
        {{ tech }}
      </span>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'

defineProps({
  experience: {
    type: Object,
    required: true
  }
})

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const [year, month] = dateStr.split('-')
  const months = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
  return `${months[parseInt(month) - 1]} ${year}`
}
</script>
