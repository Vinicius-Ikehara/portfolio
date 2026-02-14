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
          <div class="flex items-center justify-center gap-3 mb-4">
            <span class="px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider" style="background-color: rgba(139, 92, 246, 0.2); color: #a78bfa; border: 1px solid rgba(139, 92, 246, 0.3);">
              Powered by Langfuse
            </span>
            <span class="px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider" style="background-color: rgba(34, 197, 94, 0.2); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.3);">
              Live Data
            </span>
          </div>
          <h1 class="text-5xl md:text-6xl lg:text-7xl font-bold mb-4" style="color: #ffffff;">
            AI Ops Dashboard
          </h1>
          <div class="w-24 h-1 mx-auto mb-6" style="background: linear-gradient(90deg, #8b5cf6, #3b82f6);"></div>
          <p class="text-lg max-w-2xl mx-auto" style="color: #94a3b8;">
            All metrics below are pulled in real-time from a self-hosted
            <span class="font-semibold" style="color: #a78bfa;">Langfuse</span>
            instance, monitoring the
            <router-link to="/projects/pokedex" class="font-semibold underline underline-offset-2" style="color: #38bdf8;">Pok&eacute;dex AI Agent</router-link>
            in production.
          </p>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="text-center py-12">
          <i class="pi pi-spin pi-spinner text-4xl" style="color: #8b5cf6;"></i>
          <p class="mt-4 text-lg" style="color: #cbd5e1;">Loading dashboard data...</p>
        </div>

        <!-- Disabled State -->
        <div v-else-if="!dashboardData.enabled" class="rounded-xl p-8 text-center" style="background-color: #1e293b; border: 1px solid #334155;">
          <i class="pi pi-eye-slash text-5xl mb-4" style="color: #6b7280;"></i>
          <p class="text-xl font-semibold mb-2" style="color: #ffffff;">Langfuse Not Connected</p>
          <p class="text-sm" style="color: #9ca3af;">
            The observability backend is not configured in this environment. Metrics will appear here when Langfuse is enabled.
          </p>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="rounded-xl p-6 text-center" style="background-color: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3);">
          <i class="pi pi-exclamation-triangle text-4xl mb-4" style="color: #ef4444;"></i>
          <p class="text-lg font-semibold mb-2" style="color: #fca5a5;">{{ error }}</p>
          <button @click="fetchDashboard" class="mt-4 px-4 py-2 rounded-lg text-sm font-medium" style="background-color: #0284c7; color: #ffffff;">
            Retry
          </button>
        </div>

        <!-- Dashboard Content -->
        <div v-else>
          <!-- Langfuse Source Banner -->
          <div class="flex items-center gap-3 rounded-lg px-4 py-3 mb-6" style="background-color: rgba(139, 92, 246, 0.08); border: 1px solid rgba(139, 92, 246, 0.2);">
            <i class="pi pi-database" style="color: #8b5cf6;"></i>
            <span class="text-sm" style="color: #cbd5e1;">
              Data source: <span class="font-semibold" style="color: #a78bfa;">Langfuse Public API</span>
              &mdash; fetched from self-hosted instance, cached for 60s
            </span>
          </div>

          <!-- Summary Cards -->
          <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
            <!-- Total Traces -->
            <div class="rounded-xl p-5" style="background-color: #1e293b; border: 1px solid #334155;">
              <div class="flex items-center gap-3 mb-3">
                <div class="w-10 h-10 rounded-lg flex items-center justify-center" style="background-color: rgba(139, 92, 246, 0.2);">
                  <i class="pi pi-list text-lg" style="color: #8b5cf6;"></i>
                </div>
                <span class="text-xs font-medium uppercase tracking-wider" style="color: #94a3b8;">Total Traces</span>
              </div>
              <p class="text-3xl font-bold" style="color: #ffffff;">{{ dashboardData.summary.total_traces }}</p>
            </div>

            <!-- Cost USD -->
            <div class="rounded-xl p-5" style="background-color: #1e293b; border: 1px solid #334155;">
              <div class="flex items-center gap-3 mb-3">
                <div class="w-10 h-10 rounded-lg flex items-center justify-center" style="background-color: rgba(34, 197, 94, 0.2);">
                  <i class="pi pi-dollar text-lg" style="color: #22c55e;"></i>
                </div>
                <span class="text-xs font-medium uppercase tracking-wider" style="color: #94a3b8;">Total Cost</span>
              </div>
              <p class="text-3xl font-bold" style="color: #ffffff;">${{ dashboardData.summary.total_cost_usd.toFixed(2) }}</p>
            </div>

            <!-- Avg Latency -->
            <div class="rounded-xl p-5" style="background-color: #1e293b; border: 1px solid #334155;">
              <div class="flex items-center gap-3 mb-3">
                <div class="w-10 h-10 rounded-lg flex items-center justify-center" style="background-color: rgba(251, 191, 36, 0.2);">
                  <i class="pi pi-clock text-lg" style="color: #fbbf24;"></i>
                </div>
                <span class="text-xs font-medium uppercase tracking-wider" style="color: #94a3b8;">Avg Latency</span>
              </div>
              <p class="text-3xl font-bold" style="color: #ffffff;">{{ formatLatency(dashboardData.summary.avg_latency_ms) }}</p>
            </div>

            <!-- Total Observations -->
            <div class="rounded-xl p-5" style="background-color: #1e293b; border: 1px solid #334155;">
              <div class="flex items-center gap-3 mb-3">
                <div class="w-10 h-10 rounded-lg flex items-center justify-center" style="background-color: rgba(56, 189, 248, 0.2);">
                  <i class="pi pi-eye text-lg" style="color: #38bdf8;"></i>
                </div>
                <span class="text-xs font-medium uppercase tracking-wider" style="color: #94a3b8;">Observations</span>
              </div>
              <p class="text-3xl font-bold" style="color: #ffffff;">{{ dashboardData.summary.total_observations }}</p>
            </div>
          </div>

          <!-- Daily Activity Bar Chart (CSS-only) -->
          <div v-if="dashboardData.daily_stats.length > 0" class="rounded-2xl p-6 md:p-8 mb-8" style="background-color: #1e293b; border: 1px solid #334155;">
            <div class="flex items-center gap-3 mb-6">
              <i class="pi pi-chart-bar text-xl" style="color: #8b5cf6;"></i>
              <h2 class="text-xl font-bold" style="color: #ffffff;">Daily Activity</h2>
            </div>
            <div class="flex items-end gap-2 h-40">
              <div
                v-for="day in dashboardData.daily_stats.slice(0, 14).reverse()"
                :key="day.date"
                class="flex-1 flex flex-col items-center gap-1"
              >
                <span class="text-xs font-medium" style="color: #cbd5e1;">{{ day.traces }}</span>
                <div
                  class="w-full rounded-t-md transition-all"
                  :style="{
                    height: barHeight(day.traces) + '%',
                    background: 'linear-gradient(to top, #8b5cf6, #3b82f6)',
                    minHeight: '4px'
                  }"
                ></div>
                <span class="text-[10px] mt-1" style="color: #64748b;">{{ day.date.slice(5) }}</span>
              </div>
            </div>
          </div>

          <!-- Recent Traces Table -->
          <div class="rounded-2xl p-6 md:p-8 mb-8" style="background-color: #1e293b; border: 1px solid #334155;">
            <div class="flex items-center gap-3 mb-6">
              <i class="pi pi-history text-xl" style="color: #8b5cf6;"></i>
              <h2 class="text-xl font-bold" style="color: #ffffff;">Recent Traces</h2>
            </div>

            <div v-if="dashboardData.recent_traces.length === 0" class="text-center py-8">
              <i class="pi pi-inbox text-4xl mb-3" style="color: #6b7280;"></i>
              <p class="text-sm" style="color: #9ca3af;">No traces recorded yet</p>
            </div>

            <div v-else class="overflow-x-auto">
              <table class="w-full text-sm">
                <thead>
                  <tr style="border-bottom: 2px solid #334155;">
                    <th class="text-left py-3 px-3 font-semibold" style="color: #94a3b8;">Name</th>
                    <th class="text-left py-3 px-3 font-semibold" style="color: #94a3b8;">Time</th>
                    <th class="text-right py-3 px-3 font-semibold" style="color: #94a3b8;">Latency</th>
                    <th class="text-right py-3 px-3 font-semibold" style="color: #94a3b8;">Tokens</th>
                    <th class="text-right py-3 px-3 font-semibold" style="color: #94a3b8;">Cost</th>
                    <th class="text-center py-3 px-3 font-semibold" style="color: #94a3b8;">Status</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="trace in dashboardData.recent_traces"
                    :key="trace.id"
                    class="transition-colors"
                    style="border-bottom: 1px solid #1e293b;"
                    @mouseenter="$event.currentTarget.style.backgroundColor = '#0f172a'"
                    @mouseleave="$event.currentTarget.style.backgroundColor = 'transparent'"
                  >
                    <td class="py-3 px-3">
                      <span class="font-medium" style="color: #e2e8f0;">{{ trace.name }}</span>
                      <div v-if="trace.tags.length > 0" class="flex gap-1 mt-1">
                        <span
                          v-for="tag in trace.tags.slice(0, 2)"
                          :key="tag"
                          class="px-1.5 py-0.5 rounded text-[10px]"
                          style="background-color: rgba(139, 92, 246, 0.15); color: #a78bfa;"
                        >{{ tag }}</span>
                      </div>
                    </td>
                    <td class="py-3 px-3" style="color: #94a3b8;">{{ formatTime(trace.timestamp) }}</td>
                    <td class="py-3 px-3 text-right font-mono" style="color: #cbd5e1;">
                      {{ trace.latency_ms ? formatLatency(trace.latency_ms) : '-' }}
                    </td>
                    <td class="py-3 px-3 text-right font-mono" style="color: #cbd5e1;">
                      {{ trace.total_tokens > 0 ? trace.total_tokens.toLocaleString() : '-' }}
                    </td>
                    <td class="py-3 px-3 text-right font-mono" style="color: #cbd5e1;">
                      {{ trace.cost_usd > 0 ? '$' + trace.cost_usd.toFixed(4) : '-' }}
                    </td>
                    <td class="py-3 px-3 text-center">
                      <span
                        class="px-2 py-1 rounded-full text-xs font-semibold"
                        :style="statusStyle(trace.status)"
                      >{{ trace.status }}</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- How it Works -->
        <div class="mt-12 rounded-2xl p-6 md:p-8" style="background-color: #1e293b; border: 1px solid #334155;">
          <h2 class="text-2xl font-bold mb-6 text-center" style="color: #ffffff;">
            <i class="pi pi-cog mr-2" style="color: #8b5cf6;"></i>
            How it Works
          </h2>

          <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div class="text-center p-4">
              <div class="w-16 h-16 mx-auto mb-4 rounded-full flex items-center justify-center" style="background-color: rgba(139, 92, 246, 0.2);">
                <i class="pi pi-bolt text-2xl" style="color: #8b5cf6;"></i>
              </div>
              <h3 class="font-bold mb-2" style="color: #ffffff;">1. AI App</h3>
              <p class="text-sm" style="color: #9ca3af;">
                The Pokédex chatbot processes user queries using Agno + GPT-5.2 with RAG retrieval
              </p>
            </div>

            <div class="text-center p-4">
              <div class="w-16 h-16 mx-auto mb-4 rounded-full flex items-center justify-center" style="background-color: rgba(56, 189, 248, 0.2);">
                <i class="pi pi-arrows-h text-2xl" style="color: #38bdf8;"></i>
              </div>
              <h3 class="font-bold mb-2" style="color: #ffffff;">2. OpenTelemetry</h3>
              <p class="text-sm" style="color: #9ca3af;">
                OpenLIT auto-instruments every LLM call, embedding, and tool use via OTel SDK
              </p>
            </div>

            <div class="text-center p-4">
              <div class="w-16 h-16 mx-auto mb-4 rounded-full flex items-center justify-center" style="background-color: rgba(34, 197, 94, 0.2);">
                <i class="pi pi-database text-2xl" style="color: #22c55e;"></i>
              </div>
              <h3 class="font-bold mb-2" style="color: #ffffff;">3. Langfuse</h3>
              <p class="text-sm" style="color: #9ca3af;">
                Self-hosted Langfuse ingests traces, computes costs, and stores all observability data
              </p>
            </div>

            <div class="text-center p-4">
              <div class="w-16 h-16 mx-auto mb-4 rounded-full flex items-center justify-center" style="background-color: rgba(251, 191, 36, 0.2);">
                <i class="pi pi-chart-line text-2xl" style="color: #fbbf24;"></i>
              </div>
              <h3 class="font-bold mb-2" style="color: #ffffff;">4. Dashboard</h3>
              <p class="text-sm" style="color: #9ca3af;">
                This page fetches metrics from Langfuse's public API and renders them in real-time
              </p>
            </div>
          </div>
        </div>

        <!-- Tech Stack -->
        <div class="mt-12 rounded-2xl p-6 md:p-8 text-center" style="background-color: #1e293b; border: 1px solid #334155;">
          <p class="text-lg max-w-3xl mx-auto mb-6" style="color: #cbd5e1;">
            {{ project.description }}
          </p>
          <div class="flex flex-wrap gap-2 justify-center">
            <span
              v-for="tech in project.technologies"
              :key="tech"
              class="px-3 py-1.5 rounded-lg text-sm font-medium"
              style="background-color: rgba(139, 92, 246, 0.15); color: #c4b5fd; border: 1px solid rgba(139, 92, 246, 0.3);"
            >
              {{ tech }}
            </span>
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
import { ref, onMounted } from 'vue'
import { projects } from '../data/portfolio.js'
import api from '../services/api'

const project = projects.find(p => p.slug === 'ai-ops') || projects[0]

const loading = ref(true)
const error = ref(null)
const dashboardData = ref({
  enabled: false,
  summary: { total_traces: 0, total_cost_usd: 0, avg_latency_ms: 0, total_observations: 0 },
  recent_traces: [],
  daily_stats: [],
})

const fetchDashboard = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await api.get('/langfuse/dashboard')
    dashboardData.value = response.data
  } catch (err) {
    console.error('Error fetching dashboard:', err)
    error.value = 'Failed to load dashboard data. Please try again.'
  } finally {
    loading.value = false
  }
}

const formatLatency = (ms) => {
  if (ms >= 1000) return (ms / 1000).toFixed(1) + 's'
  return ms + 'ms'
}

const formatTime = (timestamp) => {
  if (!timestamp) return '-'
  const date = new Date(timestamp)
  return date.toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

const statusStyle = (status) => {
  if (status === 'OK' || status === 'DEFAULT') {
    return 'background-color: rgba(34, 197, 94, 0.15); color: #22c55e;'
  }
  if (status === 'ERROR') {
    return 'background-color: rgba(239, 68, 68, 0.15); color: #ef4444;'
  }
  if (status === 'WARNING') {
    return 'background-color: rgba(251, 191, 36, 0.15); color: #fbbf24;'
  }
  return 'background-color: rgba(148, 163, 184, 0.15); color: #94a3b8;'
}

const barHeight = (count) => {
  const max = Math.max(...dashboardData.value.daily_stats.map(d => d.traces), 1)
  return Math.max((count / max) * 100, 3)
}

onMounted(fetchDashboard)
</script>
