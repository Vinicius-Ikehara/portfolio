<template>
  <div class="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow">
    <div v-if="project.image_url" class="h-48 bg-gray-200">
      <img :src="project.image_url" :alt="project.title" class="w-full h-full object-cover">
    </div>
    <div class="p-6">
      <h3 class="text-xl font-bold text-gray-900 mb-2">{{ project.title }}</h3>
      <p class="text-gray-600 mb-4">{{ project.description }}</p>

      <div class="flex flex-wrap gap-2 mb-4">
        <span
          v-for="tech in project.technologies"
          :key="tech"
          class="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-sm"
        >
          {{ tech }}
        </span>
      </div>

      <div class="flex gap-4">
        <a
          v-if="project.project_url"
          :href="project.project_url"
          target="_blank"
          class="text-primary-600 hover:text-primary-800 font-medium"
        >
          Ver Projeto →
        </a>
        <a
          v-if="project.github_url"
          :href="project.github_url"
          target="_blank"
          class="text-gray-600 hover:text-gray-800 font-medium"
        >
          GitHub →
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'

defineProps({
  project: {
    type: Object,
    required: true
  }
})
</script>
