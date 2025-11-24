<template>
  <nav class="bg-white sticky top-0 z-50 shadow-sm" style="border-bottom: 1px solid #e5e7eb;">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Logo/Name -->
        <a href="#about" class="flex items-center gap-2 text-xl font-bold transition-colors" style="color: #0369a1;">
          <div class="w-8 h-8 rounded-lg flex items-center justify-center" style="background-color: #0284c7;">
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
            class="font-medium transition-colors flex items-center gap-2"
            style="color: #374151;"
          >
            <i :class="item.icon" class="text-sm"></i>
            <span>{{ item.label }}</span>
          </a>
        </div>

        <!-- Mobile Menu Button -->
        <button
          @click="mobileMenuOpen = !mobileMenuOpen"
          class="md:hidden p-2 rounded-lg transition-colors"
          style="color: #374151;"
        >
          <i :class="mobileMenuOpen ? 'pi pi-times' : 'pi pi-bars'" class="text-xl"></i>
        </button>
      </div>

      <!-- Mobile Menu -->
      <div
        v-show="mobileMenuOpen"
        class="md:hidden py-4 space-y-2"
        style="border-top: 1px solid #e5e7eb;"
      >
        <a
          v-for="item in menuItems"
          :key="item.id"
          :href="item.route"
          @click="mobileMenuOpen = false"
          class="flex items-center gap-3 px-4 py-3 rounded-lg font-medium transition-colors"
          style="color: #374151;"
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
