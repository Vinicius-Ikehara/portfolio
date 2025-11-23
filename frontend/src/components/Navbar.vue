<template>
  <nav class="bg-white border-b border-surface-200 sticky top-0 z-50 shadow-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Logo/Name -->
        <a href="#about" class="flex items-center gap-2 text-xl font-bold text-primary-700 hover:text-primary-800 transition-colors">
          <div class="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
            <span class="text-white font-bold text-sm">{{ getInitials(profile?.name) }}</span>
          </div>
          <span class="hidden sm:block">{{ profile?.name || 'Portfolio' }}</span>
        </a>

        <!-- Desktop Navigation -->
        <div class="hidden md:flex items-center gap-8">
          <a
            v-for="item in menuItems"
            :key="item.id"
            :href="item.route"
            class="text-surface-700 hover:text-primary-700 font-medium transition-colors flex items-center gap-2"
          >
            <i :class="item.icon" class="text-sm"></i>
            <span>{{ item.label }}</span>
          </a>
        </div>

        <!-- Mobile Menu Button -->
        <button
          @click="mobileMenuOpen = !mobileMenuOpen"
          class="md:hidden p-2 rounded-lg hover:bg-surface-100 transition-colors"
        >
          <i :class="mobileMenuOpen ? 'pi pi-times' : 'pi pi-bars'" class="text-xl text-surface-700"></i>
        </button>
      </div>

      <!-- Mobile Menu -->
      <div
        v-show="mobileMenuOpen"
        class="md:hidden py-4 border-t border-surface-200 space-y-2"
      >
        <a
          v-for="item in menuItems"
          :key="item.id"
          :href="item.route"
          @click="mobileMenuOpen = false"
          class="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-surface-50 text-surface-700 hover:text-primary-700 font-medium transition-colors"
        >
          <i :class="item.icon"></i>
          <span>{{ item.label }}</span>
        </a>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  profile: Object
})

const mobileMenuOpen = ref(false)

const menuItems = [
  {
    id: 'about',
    label: 'About',
    icon: 'pi pi-user',
    route: '#about'
  },
  {
    id: 'experience',
    label: 'Experience',
    icon: 'pi pi-briefcase',
    route: '#experience'
  },
  {
    id: 'projects',
    label: 'Projects',
    icon: 'pi pi-folder-open',
    route: '#projects'
  },
  {
    id: 'contact',
    label: 'Contact',
    icon: 'pi pi-send',
    route: '#contact'
  }
]

const getInitials = (name) => {
  if (!name) return 'VI'
  const parts = name.split(' ')
  if (parts.length >= 2) {
    return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
  }
  return name.substring(0, 2).toUpperCase()
}
</script>
