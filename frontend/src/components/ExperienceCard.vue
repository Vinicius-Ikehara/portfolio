<template>
  <div class="bg-white rounded-xl shadow-md hover:shadow-xl transition-all duration-300 overflow-hidden border border-gray-100">
    <div class="flex flex-col lg:flex-row">
      <!-- Left side - Company info -->
      <div class="lg:w-64 p-6 text-white flex flex-col justify-center" style="background: linear-gradient(135deg, #1f2937 0%, #111827 50%, #0c4a6e 100%);">
        <div class="flex items-center gap-3 mb-3">
          <div class="w-12 h-12 rounded-full flex items-center justify-center" style="background-color: rgba(255,255,255,0.1);">
            <i class="pi pi-briefcase text-xl" style="color: #38bdf8;"></i>
          </div>
          <div v-if="experience.current" class="px-3 py-1 rounded-full text-xs font-bold uppercase" style="background-color: #22c55e; color: #ffffff;">
            Current
          </div>
        </div>
        <h3 class="text-xl font-bold mb-1" style="color: #ffffff;">{{ experience.company }}</h3>
        <div class="flex items-center gap-2 text-sm" style="color: #7dd3fc;">
          <i class="pi pi-calendar"></i>
          <span>{{ formatDate(experience.start_date) }} - {{ experience.current ? 'Present' : formatDate(experience.end_date) }}</span>
        </div>
      </div>

      <!-- Right side - Details -->
      <div class="flex-1 p-6">
        <h4 class="text-2xl font-bold text-gray-900 mb-3">{{ experience.position }}</h4>

        <div class="mb-4">
          <p
            class="text-gray-600 leading-relaxed"
            :class="{ 'line-clamp-3': !expanded && isLongText }"
          >
            {{ experience.description }}
          </p>
          <button
            v-if="isLongText"
            @click="expanded = !expanded"
            class="text-primary-600 text-sm font-semibold mt-3 hover:text-primary-700 flex items-center gap-1 transition-colors"
          >
            <i :class="expanded ? 'pi pi-chevron-up' : 'pi pi-chevron-down'" class="text-xs"></i>
            {{ expanded ? 'Show less' : 'Show more' }}
          </button>
        </div>

        <div class="flex flex-wrap gap-2">
          <span
            v-for="tech in experience.technologies"
            :key="tech"
            class="px-3 py-1.5 bg-gray-100 text-gray-700 rounded-lg text-sm font-medium hover:bg-primary-100 hover:text-primary-700 transition-colors"
          >
            <i class="pi pi-tag text-xs mr-1"></i>
            {{ tech }}
          </span>
        </div>
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
  return props.experience.description && props.experience.description.length > 200
})

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const [year, month] = dateStr.split('-')
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
  return `${months[parseInt(month) - 1]} ${year}`
}
</script>

<style scoped>
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
