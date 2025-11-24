<template>
  <div class="h-full rounded-xl overflow-hidden transition-all hover:scale-105" style="background-color: #1e293b; border: 1px solid #334155;">
    <!-- Header Image -->
    <div v-if="project.image_url" class="h-48 overflow-hidden">
      <img :src="project.image_url" :alt="project.title" class="w-full h-full object-cover" />
    </div>
    <div v-else class="h-48 flex items-center justify-center" style="background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 50%, #0369a1 100%);">
      <i class="pi pi-folder text-6xl" style="color: rgba(255,255,255,0.5);"></i>
    </div>

    <!-- Content -->
    <div class="p-6">
      <div class="flex items-start gap-2 mb-3">
        <i class="pi pi-code text-lg" style="color: #38bdf8;"></i>
        <h3 class="text-xl font-bold" style="color: #ffffff;">{{ project.title }}</h3>
      </div>

      <p class="mb-4 leading-relaxed" style="color: #cbd5e1;">{{ project.description }}</p>

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
        <a
          v-if="project.project_url"
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
          v-if="project.github_url"
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
</script>
