<template>
  <Card class="h-full overflow-hidden hover:shadow-xl transition-all">
    <template #header>
      <div v-if="project.image_url" class="h-48 overflow-hidden">
        <Image :src="project.image_url" :alt="project.title" image-class="w-full h-full object-cover hover:scale-105 transition-transform duration-300" preview />
      </div>
      <div v-else class="h-48 bg-gradient-to-br from-primary-400 to-primary-600 flex items-center justify-center">
        <i class="pi pi-folder text-6xl text-white opacity-50"></i>
      </div>
    </template>
    <template #title>
      <div class="flex items-start gap-2">
        <i class="pi pi-code text-primary-600"></i>
        <span>{{ project.title }}</span>
      </div>
    </template>
    <template #content>
      <p class="text-surface-600 dark:text-surface-300 mb-4">{{ project.description }}</p>

      <div class="flex flex-wrap gap-2 mb-4">
        <Chip
          v-for="tech in project.technologies"
          :key="tech"
          :label="tech"
          class="bg-primary-50 text-primary-700"
        />
      </div>
    </template>
    <template #footer>
      <div class="flex gap-3">
        <Button
          v-if="project.project_url"
          :label="'View Project'"
          icon="pi pi-external-link"
          @click="openUrl(project.project_url)"
          outlined
          severity="primary"
          size="small"
        />
        <Button
          v-if="project.github_url"
          :label="'GitHub'"
          icon="pi pi-github"
          @click="openUrl(project.github_url)"
          outlined
          severity="secondary"
          size="small"
        />
      </div>
    </template>
  </Card>
</template>

<script setup>
import Card from 'primevue/card'
import Button from 'primevue/button'
import Chip from 'primevue/chip'
import Image from 'primevue/image'

defineProps({
  project: {
    type: Object,
    required: true
  }
})

const openUrl = (url) => {
  window.open(url, '_blank')
}
</script>
