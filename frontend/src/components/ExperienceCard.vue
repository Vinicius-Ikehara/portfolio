<template>
  <Timeline :value="[experience]" class="customized-timeline">
    <template #marker>
      <span class="flex w-8 h-8 items-center justify-center text-white rounded-full z-10 shadow-lg" :style="{ backgroundColor: experience.current ? '#10b981' : '#3b82f6' }">
        <i class="pi pi-briefcase"></i>
      </span>
    </template>
    <template #content>
      <Card class="mt-3 hover:shadow-lg transition-shadow">
        <template #title>
          <div class="flex justify-between items-start flex-wrap gap-2">
            <div>
              <div class="text-xl font-bold text-gray-900 mb-1">{{ experience.position }}</div>
              <div class="flex items-center gap-2 text-primary-600 font-medium">
                <i class="pi pi-building"></i>
                <span>{{ experience.company }}</span>
              </div>
            </div>
            <Tag :value="experience.current ? 'Current' : formatDate(experience.end_date)" :severity="experience.current ? 'success' : 'info'" icon="pi pi-calendar">
              <template #default>
                <div class="flex items-center gap-2">
                  <i class="pi pi-calendar"></i>
                  <span>{{ formatDate(experience.start_date) }} - {{ experience.current ? 'Current' : formatDate(experience.end_date) }}</span>
                </div>
              </template>
            </Tag>
          </div>
        </template>
        <template #content>
          <p class="text-surface-700 dark:text-surface-200 mb-4 leading-relaxed">{{ experience.description }}</p>

          <div class="flex flex-wrap gap-2">
            <Chip
              v-for="tech in experience.technologies"
              :key="tech"
              :label="tech"
              icon="pi pi-tag"
              class="bg-surface-100 text-surface-700"
            />
          </div>
        </template>
      </Card>
    </template>
  </Timeline>
</template>

<script setup>
import Timeline from 'primevue/timeline'
import Card from 'primevue/card'
import Tag from 'primevue/tag'
import Chip from 'primevue/chip'

defineProps({
  experience: {
    type: Object,
    required: true
  }
})

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const [year, month] = dateStr.split('-')
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
  return `${months[parseInt(month) - 1]} ${year}`
}
</script>

<style scoped>
:deep(.p-timeline-event-content) {
  padding-left: 1rem;
}
</style>
