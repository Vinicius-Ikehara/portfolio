<template>
  <nav class="bg-white shadow-lg">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <div class="flex items-center">
          <router-link to="/" class="text-2xl font-bold text-primary-600">
            {{ profile?.name || 'Portfólio' }}
          </router-link>
        </div>
        <div class="flex items-center space-x-8">
          <a href="#about" class="text-gray-700 hover:text-primary-600 transition">Sobre</a>
          <a href="#experience" class="text-gray-700 hover:text-primary-600 transition">Experiência</a>
          <a href="#projects" class="text-gray-700 hover:text-primary-600 transition">Projetos</a>
          <a href="#contact" class="text-gray-700 hover:text-primary-600 transition">Contato</a>
          <router-link to="/admin" class="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition">
            Admin
          </router-link>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { defineProps } from 'vue'

defineProps({
  profile: Object
})
</script>
