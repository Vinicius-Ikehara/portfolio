<template>
  <nav class="sticky top-0 z-50 shadow-lg" style="background-color: #0f172a; border-bottom: 1px solid #1e293b;">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Logo/Name -->
        <a href="#about" class="flex items-center gap-2 text-xl font-bold transition-colors" style="color: #38bdf8;">
          <Logo :size="32" />
          <span class="hidden sm:block" style="color: #ffffff;">{{ profile?.name || 'Portfolio' }}</span>
        </a>

        <!-- Desktop Navigation -->
        <div class="hidden md:flex items-center gap-8">
          <a
            v-for="item in menuItems"
            :key="item.id"
            :href="item.route"
            class="font-medium transition-colors flex items-center gap-2 hover:text-sky-400"
            style="color: #cbd5e1;"
          >
            <i :class="item.icon" class="text-sm" style="color: #38bdf8;"></i>
            <span>{{ item.label }}</span>
          </a>
        </div>

        <!-- Mobile Menu Button -->
        <button
          @click="mobileMenuOpen = !mobileMenuOpen"
          class="md:hidden p-2 rounded-lg transition-colors"
          style="color: #cbd5e1;"
        >
          <i :class="mobileMenuOpen ? 'pi pi-times' : 'pi pi-bars'" class="text-xl"></i>
        </button>
      </div>

      <!-- Mobile Menu -->
      <div
        v-show="mobileMenuOpen"
        class="md:hidden py-4 space-y-2"
        style="border-top: 1px solid #1e293b;"
      >
        <a
          v-for="item in menuItems"
          :key="item.id"
          :href="item.route"
          @click="mobileMenuOpen = false"
          class="flex items-center gap-3 px-4 py-3 rounded-lg font-medium transition-colors"
          style="color: #cbd5e1;"
        >
          <i :class="item.icon" style="color: #38bdf8;"></i>
          <span>{{ item.label }}</span>
        </a>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import Logo from './Logo.vue'

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
