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
            <h1 class="text-4xl md:text-5xl font-bold" style="color: #ffffff;">
              {{ project.title }}
            </h1>
            <!-- In Progress Badge -->
            <span
              v-if="project.status === 'in-progress'"
              class="px-4 py-2 rounded-full text-sm font-semibold"
              style="background-color: rgba(251, 191, 36, 0.15); color: #fbbf24; border: 1px solid rgba(251, 191, 36, 0.3);"
            >
              <i class="pi pi-clock mr-1"></i>
              In Progress
            </span>
          </div>
          <div class="w-24 h-1 mx-auto mb-6" style="background-color: #38bdf8;"></div>

          <!-- Feature Status Notice -->
          <div class="max-w-2xl mx-auto mb-6 p-4 rounded-lg" style="background-color: rgba(251, 191, 36, 0.1); border: 1px solid rgba(251, 191, 36, 0.2);">
            <p class="text-sm" style="color: #fbbf24;">
              <i class="pi pi-info-circle mr-2"></i>
              Currently showing: <strong>Daily Top 10 Rankings</strong>. More features coming soon!
            </p>
          </div>

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

        <!-- Date Selector -->
        <div class="mb-8 flex justify-center">
          <div class="rounded-xl p-6" style="background-color: #1e293b; border: 1px solid #334155;">
            <label class="block text-sm font-medium mb-2" style="color: #cbd5e1;">Select Date to View Top 10</label>
            <input
              type="date"
              v-model="selectedDate"
              @change="fetchRanking"
              class="px-4 py-2 rounded-lg bg-gray-700 text-white border border-gray-600 focus:border-sky-500 focus:outline-none"
              :max="today"
            />
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="text-center py-12">
          <i class="pi pi-spin pi-spinner text-4xl" style="color: #38bdf8;"></i>
          <p class="mt-4 text-lg" style="color: #cbd5e1;">Loading ranking data...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="rounded-xl p-6 text-center" style="background-color: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3);">
          <i class="pi pi-exclamation-triangle text-4xl mb-4" style="color: #ef4444;"></i>
          <p class="text-lg font-semibold mb-2" style="color: #fca5a5;">{{ error }}</p>
          <p class="text-sm" style="color: #9ca3af;">Try selecting a different date</p>
        </div>

        <!-- Rankings Display -->
        <div v-else-if="rankings.length > 0" class="space-y-6">
          <!-- Summary Cards -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div class="rounded-xl p-6 text-center" style="background-color: #1e293b; border: 1px solid #334155;">
              <i class="pi pi-calendar text-3xl mb-2" style="color: #38bdf8;"></i>
              <p class="text-sm mb-1" style="color: #9ca3af;">Date</p>
              <p class="text-2xl font-bold" style="color: #ffffff;">{{ formatDate(selectedDate) }}</p>
            </div>
            <div class="rounded-xl p-6 text-center" style="background-color: #1e293b; border: 1px solid #334155;">
              <i class="pi pi-chart-line text-3xl mb-2" style="color: #22c55e;"></i>
              <p class="text-sm mb-1" style="color: #9ca3af;">Total Tracks</p>
              <p class="text-2xl font-bold" style="color: #ffffff;">{{ rankings.length }}</p>
            </div>
            <div class="rounded-xl p-6 text-center" style="background-color: #1e293b; border: 1px solid #334155;">
              <i class="pi pi-users text-3xl mb-2" style="color: #a855f7;"></i>
              <p class="text-sm mb-1" style="color: #9ca3af;">Unique Artists</p>
              <p class="text-2xl font-bold" style="color: #ffffff;">{{ uniqueArtists }}</p>
            </div>
          </div>

          <!-- Top 10 Ranking -->
          <div class="rounded-2xl p-6 md:p-8" style="background-color: #1e293b; border: 1px solid #334155;">
            <h2 class="text-2xl font-bold mb-6 text-center" style="color: #ffffff;">
              <i class="pi pi-trophy mr-2" style="color: #fbbf24;"></i>
              Daily Top 10
            </h2>

            <div class="space-y-4">
              <div
                v-for="(item, index) in rankings"
                :key="item.id"
                class="flex items-center gap-4 p-4 rounded-xl transition-all hover:scale-[1.02]"
                style="background-color: #0f172a; border: 1px solid #334155;"
              >
                <!-- Position -->
                <div
                  class="flex-shrink-0 w-12 h-12 rounded-full flex items-center justify-center font-bold text-xl"
                  :style="getPositionStyle(item.posicao)"
                >
                  {{ item.posicao }}
                </div>

                <!-- Album Art -->
                <div class="flex-shrink-0">
                  <img
                    v-if="item.musicas?.imagem_url"
                    :src="item.musicas.imagem_url"
                    :alt="item.musicas?.nome || 'Album cover'"
                    class="w-16 h-16 rounded-lg object-cover"
                    @error="handleImageError"
                  />
                  <div
                    v-else
                    class="w-16 h-16 rounded-lg flex items-center justify-center"
                    style="background-color: #334155;"
                  >
                    <i class="pi pi-image text-2xl" style="color: #64748b;"></i>
                  </div>
                </div>

                <!-- Song Info -->
                <div class="flex-1 min-w-0">
                  <h3 class="font-bold text-lg mb-1 truncate" style="color: #ffffff;">
                    {{ item.musicas?.nome || 'Unknown Track' }}
                  </h3>
                  <p class="text-sm truncate" style="color: #9ca3af;">
                    <i class="pi pi-user mr-1"></i>
                    {{ item.musicas?.artista || 'Unknown Artist' }}
                  </p>
                  <!-- Position Change Indicator -->
                  <div v-if="item.variacao_posicao !== null && item.variacao_posicao !== undefined" class="mt-1 flex items-center gap-1">
                    <span
                      v-if="item.variacao_posicao > 0"
                      class="text-xs font-semibold flex items-center gap-1"
                      style="color: #22c55e;"
                    >
                      <i class="pi pi-arrow-up"></i>
                      {{ Math.abs(item.variacao_posicao) }}
                    </span>
                    <span
                      v-else-if="item.variacao_posicao < 0"
                      class="text-xs font-semibold flex items-center gap-1"
                      style="color: #ef4444;"
                    >
                      <i class="pi pi-arrow-down"></i>
                      {{ Math.abs(item.variacao_posicao) }}
                    </span>
                    <span
                      v-else
                      class="text-xs font-semibold flex items-center gap-1"
                      style="color: #9ca3af;"
                    >
                      <i class="pi pi-minus"></i>
                      No change
                    </span>
                  </div>
                </div>

                <!-- Play Count -->
                <div class="flex-shrink-0 text-right">
                  <p class="text-sm mb-1" style="color: #9ca3af;">Plays (Today)</p>
                  <p class="text-xl font-bold" style="color: #38bdf8;">{{ formatPlaycount(item.playcount_data) }}</p>
                  <p class="text-xs" style="color: #64748b;">{{ item.ouvintes_data?.toLocaleString() || 0 }} listeners</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="text-center py-12">
          <i class="pi pi-inbox text-6xl mb-4" style="color: #6b7280;"></i>
          <p class="text-lg" style="color: #9ca3af;">No data available for this date</p>
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
                <i class="pi pi-database text-2xl" style="color: #38bdf8;"></i>
              </div>
              <h3 class="font-bold mb-2" style="color: #ffffff;">1. Data Collection</h3>
              <p class="text-sm" style="color: #9ca3af;">
                Last.fm listening history is automatically collected and stored in Supabase
              </p>
            </div>

            <div class="text-center p-4">
              <div class="w-16 h-16 mx-auto mb-4 rounded-full flex items-center justify-center" style="background-color: rgba(56, 189, 248, 0.2);">
                <i class="pi pi-chart-bar text-2xl" style="color: #38bdf8;"></i>
              </div>
              <h3 class="font-bold mb-2" style="color: #ffffff;">2. Daily Rankings</h3>
              <p class="text-sm" style="color: #9ca3af;">
                System processes data daily to generate top 10 most played tracks
              </p>
            </div>

            <div class="text-center p-4">
              <div class="w-16 h-16 mx-auto mb-4 rounded-full flex items-center justify-center" style="background-color: rgba(56, 189, 248, 0.2);">
                <i class="pi pi-eye text-2xl" style="color: #38bdf8;"></i>
              </div>
              <h3 class="font-bold mb-2" style="color: #ffffff;">3. Visualization</h3>
              <p class="text-sm" style="color: #9ca3af;">
                FastAPI serves the data through REST endpoints for real-time dashboard display
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
import { ref, computed, onMounted } from 'vue'
import { projects } from '../data/portfolio.js'
import api from '../services/api'

// Get the Last.fm project
const project = projects.find(p => p.slug === 'lastfm-insights') || projects[0]

// Reactive state
const selectedDate = ref('')
const rankings = ref([])
const loading = ref(false)
const error = ref(null)

// Get today's date in YYYY-MM-DD format
const today = computed(() => {
  const date = new Date()
  return date.toISOString().split('T')[0]
})

// Compute unique artists count
const uniqueArtists = computed(() => {
  if (!rankings.value || !Array.isArray(rankings.value)) return 0
  const artists = new Set(rankings.value.map(r => r.musicas?.artista).filter(Boolean))
  return artists.size
})

// Format date for display
const formatDate = (dateStr) => {
  const date = new Date(dateStr + 'T00:00:00')
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// Get position badge style
const getPositionStyle = (position) => {
  if (position === 1) {
    return 'background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%); color: #ffffff;'
  } else if (position === 2) {
    return 'background: linear-gradient(135deg, #d4d4d8 0%, #a1a1aa 100%); color: #18181b;'
  } else if (position === 3) {
    return 'background: linear-gradient(135deg, #fb923c 0%, #ea580c 100%); color: #ffffff;'
  } else {
    return 'background-color: #334155; color: #cbd5e1;'
  }
}

// Format playcount with commas
const formatPlaycount = (count) => {
  if (!count) return '0'
  return count.toLocaleString()
}

// Handle image loading errors
const handleImageError = (event) => {
  event.target.style.display = 'none'
  const fallback = event.target.nextElementSibling
  if (fallback) fallback.style.display = 'flex'
}

// Fetch latest ranking data from API
const fetchLatestRanking = async () => {
  loading.value = true
  error.value = null
  rankings.value = []

  try {
    const response = await api.get('/lastfm/ranking/latest')
    rankings.value = response.data
    // Update selectedDate with the actual date from the data
    if (response.data.length > 0) {
      selectedDate.value = response.data[0].data
    }
  } catch (err) {
    console.error('Error fetching latest ranking:', err)
    if (err.response?.status === 404) {
      error.value = 'No ranking data available in the database'
    } else {
      error.value = 'Failed to load ranking data. Please try again.'
    }
  } finally {
    loading.value = false
  }
}

// Fetch ranking data for specific date
const fetchRanking = async () => {
  if (!selectedDate.value) return

  loading.value = true
  error.value = null
  rankings.value = []

  try {
    const response = await api.get(`/lastfm/ranking/${selectedDate.value}`)
    rankings.value = response.data
  } catch (err) {
    console.error('Error fetching ranking:', err)
    if (err.response?.status === 404) {
      error.value = `No ranking data found for ${formatDate(selectedDate.value)}`
    } else {
      error.value = 'Failed to load ranking data. Please try again.'
    }
  } finally {
    loading.value = false
  }
}

// Initialize with latest data from database
onMounted(() => {
  fetchLatestRanking()
})
</script>
