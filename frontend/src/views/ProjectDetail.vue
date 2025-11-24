<template>
  <div class="min-h-screen" style="background-color: #111827;">
    <!-- Header -->
    <header class="sticky top-0 z-50 shadow-lg" style="background-color: #0f172a; border-bottom: 1px solid #1e293b;">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <router-link to="/" class="flex items-center gap-2 text-xl font-bold transition-colors" style="color: #38bdf8;">
            <i class="pi pi-arrow-left"></i>
            <span>Back to Portfolio</span>
          </router-link>
        </div>
      </div>
    </header>

    <!-- Project Content -->
    <main class="py-12">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <!-- Project Header -->
        <div class="text-center mb-12">
          <h1 class="text-4xl md:text-5xl font-bold mb-4" style="color: #ffffff;">
            {{ project.title }}
          </h1>
          <div class="w-24 h-1 mx-auto mb-6" style="background-color: #38bdf8;"></div>
          <p class="text-lg max-w-3xl mx-auto mb-8" style="color: #cbd5e1;">
            {{ project.description }}
          </p>

          <!-- Technologies -->
          <div class="flex flex-wrap gap-2 justify-center mb-8">
            <span
              v-for="tech in project.technologies"
              :key="tech"
              class="px-3 py-1.5 rounded-lg text-sm font-medium"
              style="background-color: rgba(56, 189, 248, 0.15); color: #7dd3fc; border: 1px solid rgba(56, 189, 248, 0.3);"
            >
              {{ tech }}
            </span>
          </div>
        </div>

        <!-- Interactive Demo -->
        <div class="rounded-2xl p-6 md:p-8" style="background-color: #1e293b; border: 1px solid #334155;">
          <div class="text-center mb-6">
            <h2 class="text-2xl font-bold mb-2" style="color: #ffffff;">
              <i class="pi pi-play-circle mr-2" style="color: #38bdf8;"></i>
              Live Demo
            </h2>
            <p class="text-sm" style="color: #9ca3af;">
              Interact with the AI agent below - ask anything about 1st Generation Pokémon!
            </p>
          </div>

          <PokedexChat />
        </div>

        <!-- How it works -->
        <div class="mt-12 rounded-2xl p-6 md:p-8" style="background-color: #1e293b; border: 1px solid #334155;">
          <h2 class="text-2xl font-bold mb-6 text-center" style="color: #ffffff;">
            <i class="pi pi-cog mr-2" style="color: #38bdf8;"></i>
            How It Works
          </h2>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="text-center p-4">
              <div class="w-16 h-16 mx-auto mb-4 rounded-full flex items-center justify-center" style="background-color: rgba(56, 189, 248, 0.2);">
                <i class="pi pi-comments text-2xl" style="color: #38bdf8;"></i>
              </div>
              <h3 class="font-bold mb-2" style="color: #ffffff;">1. User Question</h3>
              <p class="text-sm" style="color: #9ca3af;">
                You ask a question about any Pokémon from the first generation
              </p>
            </div>

            <div class="text-center p-4">
              <div class="w-16 h-16 mx-auto mb-4 rounded-full flex items-center justify-center" style="background-color: rgba(56, 189, 248, 0.2);">
                <i class="pi pi-search text-2xl" style="color: #38bdf8;"></i>
              </div>
              <h3 class="font-bold mb-2" style="color: #ffffff;">2. RAG Search</h3>
              <p class="text-sm" style="color: #9ca3af;">
                The system performs semantic search on the PostgreSQL vector database
              </p>
            </div>

            <div class="text-center p-4">
              <div class="w-16 h-16 mx-auto mb-4 rounded-full flex items-center justify-center" style="background-color: rgba(56, 189, 248, 0.2);">
                <i class="pi pi-bolt text-2xl" style="color: #38bdf8;"></i>
              </div>
              <h3 class="font-bold mb-2" style="color: #ffffff;">3. AI Response</h3>
              <p class="text-sm" style="color: #9ca3af;">
                GPT-4o mini generates an accurate, conversational response
              </p>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Footer -->
    <footer class="py-8" style="background-color: #030712; color: #9ca3af; border-top: 1px solid #1f2937;">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <router-link
          to="/"
          class="inline-flex items-center gap-2 px-6 py-3 rounded-lg transition-colors font-medium"
          style="background-color: #0284c7; color: #ffffff;"
        >
          <i class="pi pi-arrow-left"></i>
          Back to Portfolio
        </router-link>
      </div>
    </footer>
  </div>
</template>

<script setup>
import PokedexChat from '../components/PokedexChat.vue'
import { projects } from '../data/portfolio.js'

// Get the Pokedex project
const project = projects.find(p => p.slug === 'pokedex') || projects[0]
</script>
