<template>
  <div class="min-h-screen" style="background-color: #1c1a17;">
    <!-- Header -->
    <header class="sticky top-0 z-50 shadow-lg" style="background-color: #1c1a17; border-bottom: 1px solid #3a352f;">
      <div class="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <router-link to="/" class="flex items-center gap-2 text-xl font-bold transition-colors hover:opacity-80" style="color: #c8703f;">
            <i class="pi pi-arrow-left"></i>
            <span>Back to Portfolio</span>
          </router-link>
        </div>
      </div>
    </header>

    <!-- Project Content -->
    <main class="py-12">
      <div class="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8">
        <!-- Project Header -->
        <div class="text-center mb-12">
          <h1 class="text-4xl md:text-5xl font-bold mb-4" style="color: #ede7df;">
            {{ project.title }}
          </h1>
          <div class="w-24 h-1 mx-auto mb-6" style="background-color: #c8703f;"></div>
          <p class="text-lg max-w-3xl mx-auto mb-8" style="color: #a39b8f;">
            An AI-powered Pokédex chatbot built with Python, FastAPI, and the Agno AI framework.
            Features a complete RAG pipeline with Supabase pgvector for semantic search, guardrails for jailbreak protection,
            and session-based memory. The agent retrieves Pokémon data through embeddings and generates contextualized responses.
          </p>

          <!-- Technologies -->
          <div class="flex flex-wrap gap-2 justify-center mb-8">
            <span
              v-for="tech in project.technologies"
              :key="tech"
              class="px-3 py-1.5 rounded-lg text-sm font-medium"
              style="background-color: rgba(56, 189, 248, 0.15); color: #dd9660; border: 1px solid rgba(56, 189, 248, 0.3);"
            >
              {{ tech }}
            </span>
          </div>
        </div>

        <!-- Interactive Demo -->
        <div class="rounded-2xl p-6 md:p-8" style="background-color: #262320; border: 1px solid #3a352f;">
          <div class="text-center mb-6">
            <h2 class="text-2xl font-bold mb-2" style="color: #ede7df;">
              <i class="pi pi-play-circle mr-2" style="color: #c8703f;"></i>
              Live Demo
            </h2>
            <p class="text-sm" style="color: #a39b8f;">
              Interact with the AI agent below - ask anything about 1st Generation Pokémon!
            </p>
          </div>

          <PokedexChat />
        </div>

        <!-- How it works -->
        <div class="mt-12 rounded-2xl p-6 md:p-8" style="background-color: #262320; border: 1px solid #3a352f;">
          <h2 class="text-2xl font-bold mb-6 text-center" style="color: #ede7df;">
            <i class="pi pi-cog mr-2" style="color: #c8703f;"></i>
            How It Works
          </h2>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="text-center p-4">
              <div class="w-16 h-16 mx-auto mb-4 rounded-full flex items-center justify-center" style="background-color: rgba(56, 189, 248, 0.2);">
                <i class="pi pi-comments text-2xl" style="color: #c8703f;"></i>
              </div>
              <h3 class="font-bold mb-2" style="color: #ede7df;">1. User Question</h3>
              <p class="text-sm" style="color: #a39b8f;">
                You ask a question about any Pokémon from the first generation
              </p>
            </div>

            <div class="text-center p-4">
              <div class="w-16 h-16 mx-auto mb-4 rounded-full flex items-center justify-center" style="background-color: rgba(56, 189, 248, 0.2);">
                <i class="pi pi-search text-2xl" style="color: #c8703f;"></i>
              </div>
              <h3 class="font-bold mb-2" style="color: #ede7df;">2. RAG Search + Guardrail</h3>
              <p class="text-sm" style="color: #a39b8f;">
                The system performs semantic search on the PostgreSQL vector database with a guardrail node to ensure relevant and safe responses
              </p>
            </div>

            <div class="text-center p-4">
              <div class="w-16 h-16 mx-auto mb-4 rounded-full flex items-center justify-center" style="background-color: rgba(56, 189, 248, 0.2);">
                <i class="pi pi-bolt text-2xl" style="color: #c8703f;"></i>
              </div>
              <h3 class="font-bold mb-2" style="color: #ede7df;">3. AI Response</h3>
              <p class="text-sm" style="color: #a39b8f;">
                Agno Agent + GPT-5.2 generates an accurate, conversational response with stats and images
              </p>
            </div>
          </div>
        </div>

        <!-- Workflow Diagram -->
        <div class="mt-12 rounded-2xl p-6 md:p-8" style="background-color: #262320; border: 1px solid #3a352f;">
          <h2 class="text-2xl font-bold mb-6 text-center" style="color: #ede7df;">
            <i class="pi pi-sitemap mr-2" style="color: #c8703f;"></i>
            Workflow Architecture
          </h2>
          <p class="text-center mb-6" style="color: #a39b8f;">
            Built with Python, FastAPI, and Agno AI framework - a complete RAG pipeline with guardrails and session memory.
          </p>

          <!-- Custom Flowchart -->
          <div class="flowchart-container overflow-x-auto py-8">
            <div class="flex flex-col items-center gap-2 min-w-max mx-auto" style="width: fit-content;">

              <!-- Row 1: User Input -->
              <div class="flow-node px-6 py-3 rounded-lg font-semibold" style="background: linear-gradient(135deg, #c8703f, #874726); color: white;">
                <i class="pi pi-user mr-2"></i>
                User Question
              </div>
              <div class="flow-arrow">
                <i class="pi pi-arrow-down text-2xl" style="color: #c8703f;"></i>
              </div>

              <!-- Row 2: API Endpoint -->
              <div class="flow-node px-6 py-3 rounded-lg font-medium" style="background-color: #3a352f; color: #ede7df; border: 2px solid #6b6258;">
                <i class="pi pi-server mr-2" style="color: #c8703f;"></i>
                POST /api/webhook/pokedex
              </div>
              <div class="flow-arrow">
                <i class="pi pi-arrow-down text-2xl" style="color: #c8703f;"></i>
              </div>

              <!-- Row 3: Guardrails -->
              <div class="flow-node px-6 py-3 rounded-lg font-semibold" style="background: linear-gradient(135deg, #f59e0b, #d97706); color: white;">
                <i class="pi pi-shield mr-2"></i>
                Guardrails Check
              </div>

              <!-- Branching -->
              <div class="flex items-start gap-8 mt-2">
                <!-- Left Branch: Blocked -->
                <div class="flex flex-col items-center">
                  <div class="text-xs font-medium px-2 py-1 rounded mb-2" style="background-color: #dc2626; color: white;">
                    Blocked
                  </div>
                  <div class="flow-node px-4 py-2 rounded-lg text-sm" style="background-color: #7f1d1d; color: #fca5a5; border: 1px solid #dc2626;">
                    <i class="pi pi-ban mr-1"></i>
                    Error Response
                  </div>
                </div>

                <!-- Center Arrow Down -->
                <div class="flex flex-col items-center">
                  <div class="text-xs font-medium px-2 py-1 rounded mb-2" style="background-color: #22c55e; color: white;">
                    Passed
                  </div>
                  <i class="pi pi-arrow-down text-2xl" style="color: #c8703f;"></i>
                </div>

                <!-- Right: Empty for balance -->
                <div class="w-24"></div>
              </div>

              <!-- Row 4: Agno Agent Box -->
              <div class="flow-node-large rounded-xl p-4 mt-2" style="background-color: #452414; border: 2px solid #c8703f;">
                <div class="text-center font-bold mb-3" style="color: #c8703f;">
                  <i class="pi pi-android mr-2"></i>
                  Agno Agent
                </div>
                <div class="grid grid-cols-3 gap-3">
                  <!-- Memory -->
                  <div class="flex flex-col items-center p-3 rounded-lg" style="background-color: #131110;">
                    <i class="pi pi-history text-xl mb-2" style="color: #a78bfa;"></i>
                    <span class="text-xs font-medium" style="color: #c4b5fd;">Memory</span>
                    <span class="text-xs mt-1" style="color: #6b6258;">Session History</span>
                  </div>
                  <!-- VectorStore -->
                  <div class="flex flex-col items-center p-3 rounded-lg" style="background-color: #131110;">
                    <i class="pi pi-database text-xl mb-2" style="color: #34d399;"></i>
                    <span class="text-xs font-medium" style="color: #6ee7b7;">VectorStore</span>
                    <span class="text-xs mt-1" style="color: #6b6258;">pgvector RAG</span>
                  </div>
                  <!-- LLM -->
                  <div class="flex flex-col items-center p-3 rounded-lg" style="background-color: #131110;">
                    <i class="pi pi-bolt text-xl mb-2" style="color: #fbbf24;"></i>
                    <span class="text-xs font-medium" style="color: #fde68a;">LLM</span>
                    <span class="text-xs mt-1" style="color: #6b6258;">GPT-5.2</span>
                  </div>
                </div>
              </div>
              <div class="flow-arrow">
                <i class="pi pi-arrow-down text-2xl" style="color: #c8703f;"></i>
              </div>

              <!-- Row 5: Response -->
              <div class="flow-node px-6 py-3 rounded-lg font-semibold" style="background: linear-gradient(135deg, #22c55e, #16a34a); color: white;">
                <i class="pi pi-check-circle mr-2"></i>
                Formatted Response + Image
              </div>

            </div>
          </div>

          <!-- Tech Stack Pills -->
          <div class="flex flex-wrap justify-center gap-2 mt-6 pt-6" style="border-top: 1px solid #3a352f;">
            <span class="px-3 py-1 rounded-full text-xs font-medium" style="background-color: #1e3a8a; color: #93c5fd;">Python</span>
            <span class="px-3 py-1 rounded-full text-xs font-medium" style="background-color: #065f46; color: #6ee7b7;">FastAPI</span>
            <span class="px-3 py-1 rounded-full text-xs font-medium" style="background-color: #7c2d12; color: #fdba74;">Agno</span>
            <span class="px-3 py-1 rounded-full text-xs font-medium" style="background-color: #3f3f46; color: #a1a1aa;">Supabase</span>
            <span class="px-3 py-1 rounded-full text-xs font-medium" style="background-color: #4c1d95; color: #c4b5fd;">pgvector</span>
            <span class="px-3 py-1 rounded-full text-xs font-medium" style="background-color: #155e75; color: #67e8f9;">OpenAI</span>
          </div>
        </div>
      </div>
    </main>

    <!-- Footer -->
    <footer class="py-8" style="background-color: #131110; color: #a39b8f; border-top: 1px solid #3a352f;">
      <div class="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <router-link
          to="/"
          class="inline-flex items-center gap-2 px-6 py-3 rounded-lg transition-colors font-medium"
          style="background-color: #c8703f; color: #1c1a17;"
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
