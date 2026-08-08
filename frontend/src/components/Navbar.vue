<template>
  <nav class="sticky top-0 z-50 shadow-lg" style="background-color: var(--bg-nav); border-bottom: 1px solid var(--border-color);">
    <div class="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Logo/Name -->
        <a href="#about" @click.prevent="scrollToSection('about')" class="flex items-center gap-2 text-xl font-bold transition-colors" style="color: #c8703f; font-family: ui-monospace, 'SF Mono', 'Cascadia Code', Consolas, monospace;">
          <Logo :size="32" />
          <span class="hidden sm:block" style="color: var(--text-heading);">{{ profile?.name || 'Portfolio' }}</span>
        </a>

        <!-- Desktop Navigation -->
        <div class="hidden md:flex items-center gap-6">
          <a
            v-for="item in menuItems"
            :key="item.id"
            :href="item.route"
            @click.prevent="scrollToSection(item.id)"
            class="font-medium transition-colors flex items-center gap-2 hover:opacity-70"
            style="color: var(--text-muted);"
          >
            <i :class="item.icon" class="text-sm" style="color: #c8703f;"></i>
            <span>{{ item.label }}</span>
          </a>

          <button
            @click="toggleTheme"
            class="w-9 h-9 rounded-lg flex items-center justify-center transition-colors"
            style="color: var(--text-muted); border: 1px solid var(--border-color);"
            :aria-label="theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'"
            :title="theme === 'dark' ? 'Light mode' : 'Dark mode'"
          >
            <i :class="theme === 'dark' ? 'pi pi-sun' : 'pi pi-moon'" style="color: #c8703f;"></i>
          </button>
        </div>

        <!-- Mobile Menu Button -->
        <div class="flex items-center gap-2 md:hidden">
          <button
            @click="toggleTheme"
            class="w-9 h-9 rounded-lg flex items-center justify-center transition-colors"
            style="color: var(--text-muted); border: 1px solid var(--border-color);"
            :aria-label="theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'"
          >
            <i :class="theme === 'dark' ? 'pi pi-sun' : 'pi pi-moon'" style="color: #c8703f;"></i>
          </button>
          <button
            @click="mobileMenuOpen = !mobileMenuOpen"
            class="p-2 rounded-lg transition-colors"
            style="color: var(--text-muted);"
          >
            <i :class="mobileMenuOpen ? 'pi pi-times' : 'pi pi-bars'" class="text-xl"></i>
          </button>
        </div>
      </div>

      <!-- Mobile Menu -->
      <div
        v-show="mobileMenuOpen"
        class="md:hidden py-4 space-y-2"
        style="border-top: 1px solid var(--border-color);"
      >
        <a
          v-for="item in menuItems"
          :key="item.id"
          :href="item.route"
          @click.prevent="scrollToSection(item.id)"
          class="flex items-center gap-3 px-4 py-3 rounded-lg font-medium transition-colors"
          style="color: var(--text-muted);"
        >
          <i :class="item.icon" style="color: #c8703f;"></i>
          <span>{{ item.label }}</span>
        </a>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import Logo from './Logo.vue'
import { useTheme } from '../composables/useTheme.js'

defineProps({
  profile: Object
})

const { theme, toggleTheme } = useTheme()

const mobileMenuOpen = ref(false)

const scrollToSection = (id) => {
  mobileMenuOpen.value = false
  const el = document.getElementById(id)
  if (!el) return

  el.scrollIntoView({ behavior: 'smooth', block: 'start' })

  el.classList.remove('nav-highlight-flash')
  void el.offsetWidth // restart animation if the same section is clicked again
  el.classList.add('nav-highlight-flash')
  setTimeout(() => el.classList.remove('nav-highlight-flash'), 1000)
}

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
