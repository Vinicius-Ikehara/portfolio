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
          <h1 class="text-5xl md:text-6xl lg:text-7xl font-bold mb-4" style="color: #ffffff;">
            {{ project.title }}
          </h1>
          <div class="w-24 h-1 mx-auto mb-6" style="background-color: #38bdf8;"></div>
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

        <!-- Rankings Display - Single Container -->
        <div v-else-if="rankings.length > 0" class="rounded-2xl p-6 md:p-8" style="background-color: #1e293b; border: 1px solid #334155;">
          <!-- Header with Date Selector -->
          <div class="flex flex-col md:flex-row items-center justify-between gap-4 pb-6 mb-6" style="border-bottom: 2px solid #334155;">
            <div class="flex items-center gap-3">
              <i class="pi pi-chart-line text-2xl" style="color: #38bdf8;"></i>
              <h2 class="text-2xl font-bold" style="color: #ffffff;">Music Analytics Dashboard</h2>
            </div>
            <div class="flex items-center gap-3">
              <label class="text-sm font-medium" style="color: #cbd5e1;">
                <i class="pi pi-calendar mr-2" style="color: #38bdf8;"></i>
                Date:
              </label>
              <input
                type="date"
                v-model="selectedDate"
                @change="fetchRanking"
                @click="(e) => e.target.showPicker()"
                class="px-6 py-3 rounded-lg font-medium border-2 focus:outline-none transition-all hover:scale-105 cursor-pointer min-w-[200px]"
                style="background-color: #ffffff; color: #1e293b; border-color: #38bdf8; font-weight: 600; font-size: 1rem;"
                :max="today"
              />
            </div>
          </div>

          <!-- Dual Layout: Newsletter (66%) + Top 10 (33%) -->
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 lg:items-stretch">
            <!-- Newsletter Section (66% - 2 columns) -->
            <div class="lg:col-span-2 rounded-2xl p-6 md:p-8 flex flex-col" style="background-color: #0f172a; border: 1px solid #334155;">
              <div v-if="newsletter.length > 0" class="grid grid-cols-2 gap-4 flex-1">
                <!-- Headline Title (spans 2 columns) -->
                <div class="col-span-2 rounded-xl p-6 text-center" style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); border: 2px solid #38bdf8;">
                  <div class="flex items-center justify-center gap-3 mb-2">
                    <div class="w-8 h-0.5" style="background: linear-gradient(90deg, #0284c7 0%, #38bdf8 100%);"></div>
                    <i class="pi pi-sparkles text-2xl" style="background: linear-gradient(135deg, #0284c7 0%, #38bdf8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;"></i>
                    <div class="w-8 h-0.5" style="background: linear-gradient(90deg, #38bdf8 0%, #0284c7 100%);"></div>
                  </div>
                  <h2 class="text-3xl font-black uppercase tracking-wide" style="background: linear-gradient(135deg, #0284c7 0%, #38bdf8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-family: 'Arial Black', sans-serif; text-shadow: 2px 2px 8px rgba(56, 189, 248, 0.3);">
                    AI-Curated Newsletter
                  </h2>
                  <p class="text-xs mt-2 uppercase tracking-widest" style="color: #94a3b8;">✨ Personalized Artist Insights by AI ✨</p>
                </div>

                <!-- Card Wrapper -->
                <div
                  v-for="(item, index) in newsletter.slice(0, 4)"
                  :key="item.id"
                >
                  <!-- Flip Card Container -->
                  <div class="flip-card-container">
                    <div class="flip-card-inner">
                      <!-- Front Face -->
                      <div class="flip-card-front rounded-xl overflow-hidden relative" style="border: 2px solid #334155;">
                        <!-- Artist Image 100% -->
                        <img
                          v-if="item.imagem_url"
                          :src="item.imagem_url"
                          :alt="item.artista"
                          class="w-full h-full object-cover"
                        />
                        <div
                          v-else
                          class="w-full h-full flex items-center justify-center"
                          style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);"
                        >
                          <i class="pi pi-user text-4xl" style="color: #64748b;"></i>
                        </div>

                        <!-- Title Overlay (Bottom) -->
                        <div class="absolute bottom-0 left-0 right-0 p-4" style="background: linear-gradient(to top, rgba(0,0,0,0.95) 0%, rgba(0,0,0,0.7) 70%, transparent 100%);">
                          <p class="text-xs font-bold uppercase mb-1" style="color: #a855f7; letter-spacing: 0.05em;">
                            {{ item.artista }}
                          </p>
                          <h3 class="font-bold text-sm leading-tight line-clamp-2" style="color: #ffffff; font-family: 'Arial', sans-serif;">
                            {{ item.titulo || 'Trending Artist' }}
                          </h3>
                        </div>

                        <!-- Hover Hint -->
                        <div class="absolute inset-0 bg-black/40 flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity">
                          <p class="text-white text-xs font-semibold uppercase tracking-wider">
                            ↻ Hover to see details
                          </p>
                        </div>
                      </div>

                      <!-- Back Face -->
                      <div class="flip-card-back rounded-xl p-4 flex flex-col justify-center" style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border: 2px solid #38bdf8;">
                        <div class="text-center">
                          <h3 class="font-bold text-xl mb-3" style="color: #38bdf8;">
                            {{ item.artista }}
                          </h3>
                          <div class="w-12 h-1 mx-auto mb-3" style="background-color: #38bdf8;"></div>
                          <p class="text-sm leading-relaxed" style="color: #cbd5e1;">
                            {{ item.descricao || 'No description available for this artist.' }}
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Newsletter Empty State -->
              <div v-else class="flex-1 flex flex-col">
                <!-- Headline Title -->
                <div class="rounded-xl p-6 text-center mb-4" style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); border: 2px solid #38bdf8;">
                  <div class="flex items-center justify-center gap-3 mb-2">
                    <div class="w-8 h-0.5" style="background: linear-gradient(90deg, #0284c7 0%, #38bdf8 100%);"></div>
                    <i class="pi pi-sparkles text-2xl" style="background: linear-gradient(135deg, #0284c7 0%, #38bdf8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;"></i>
                    <div class="w-8 h-0.5" style="background: linear-gradient(90deg, #38bdf8 0%, #0284c7 100%);"></div>
                  </div>
                  <h2 class="text-3xl font-black uppercase tracking-wide" style="background: linear-gradient(135deg, #0284c7 0%, #38bdf8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-family: 'Arial Black', sans-serif; text-shadow: 2px 2px 8px rgba(56, 189, 248, 0.3);">
                    AI-Curated Newsletter
                  </h2>
                  <p class="text-xs mt-2 uppercase tracking-widest" style="color: #94a3b8;">✨ Personalized Artist Insights by AI ✨</p>
                </div>
                <!-- Empty message -->
                <div class="flex-1 flex items-center justify-center">
                  <div class="text-center">
                    <i class="pi pi-inbox text-4xl mb-3" style="color: #6b7280;"></i>
                    <p class="text-sm" style="color: #9ca3af;">No artists available</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Top 10 Ranking (33% - 1 column) -->
            <div class="lg:col-span-1 rounded-2xl p-6 md:p-8" style="background-color: #0f172a; border: 1px solid #334155;">
              <h2 class="text-2xl font-bold mb-6 text-center" style="color: #ffffff;">
                <i class="pi pi-trophy mr-2" style="color: #fbbf24;"></i>
                Daily Top 10
              </h2>

              <div class="space-y-1.5">
                <div
                  v-for="(item, index) in rankings"
                  :key="item.id"
                  class="flex items-center gap-3 p-2 rounded-xl transition-all hover:scale-[1.02]"
                  style="background-color: #0f172a; border: 1px solid #334155;"
                >
                  <!-- Position -->
                  <div
                    class="flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center font-bold text-lg"
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
                      class="w-12 h-12 rounded-lg object-cover"
                      @error="handleImageError"
                    />
                    <div
                      v-else
                      class="w-12 h-12 rounded-lg flex items-center justify-center"
                      style="background-color: #334155;"
                    >
                      <i class="pi pi-image text-xl" style="color: #64748b;"></i>
                    </div>
                  </div>

                  <!-- Song Info -->
                  <div class="flex-1 min-w-0">
                    <h3 class="font-bold text-sm mb-0.5 truncate" style="color: #ffffff;">
                      {{ item.musicas?.nome || 'Unknown Track' }}
                    </h3>
                    <p class="text-xs truncate" style="color: #9ca3af;">
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
            How the ETL Pipeline Works
          </h2>

          <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div class="text-center p-4">
              <div class="w-16 h-16 mx-auto mb-4 rounded-full flex items-center justify-center" style="background-color: rgba(56, 189, 248, 0.2);">
                <i class="pi pi-download text-2xl" style="color: #38bdf8;"></i>
              </div>
              <h3 class="font-bold mb-2" style="color: #ffffff;">1. Daily Extract</h3>
              <p class="text-sm" style="color: #9ca3af;">
                Automated ETL runs daily to extract Last.fm data (only available for current day)
              </p>
            </div>

            <div class="text-center p-4">
              <div class="w-16 h-16 mx-auto mb-4 rounded-full flex items-center justify-center" style="background-color: rgba(168, 85, 247, 0.2);">
                <i class="pi pi-database text-2xl" style="color: #a855f7;"></i>
              </div>
              <h3 class="font-bold mb-2" style="color: #ffffff;">2. Store & Transform</h3>
              <p class="text-sm" style="color: #9ca3af;">
                Data is stored in Supabase and transformed to calculate rankings and position changes
              </p>
            </div>

            <div class="text-center p-4">
              <div class="w-16 h-16 mx-auto mb-4 rounded-full flex items-center justify-center" style="background-color: rgba(34, 197, 94, 0.2);">
                <i class="pi pi-sparkles text-2xl" style="color: #22c55e;"></i>
              </div>
              <h3 class="font-bold mb-2" style="color: #ffffff;">3. AI Analysis</h3>
              <p class="text-sm" style="color: #9ca3af;">
                AI analyzes top 50 tracks to identify trends, ranking shifts, and generates personalized insights
              </p>
            </div>

            <div class="text-center p-4">
              <div class="w-16 h-16 mx-auto mb-4 rounded-full flex items-center justify-center" style="background-color: rgba(251, 191, 36, 0.2);">
                <i class="pi pi-send text-2xl" style="color: #fbbf24;"></i>
              </div>
              <h3 class="font-bold mb-2" style="color: #ffffff;">4. Newsletter</h3>
              <p class="text-sm" style="color: #9ca3af;">
                Curated newsletter is generated with artist highlights and served via FastAPI dashboard
              </p>
            </div>
          </div>
        </div>

        <!-- Project Description -->
        <div class="mt-12 rounded-2xl p-6 md:p-8 text-center" style="background-color: #1e293b; border: 1px solid #334155;">
          <p class="text-lg max-w-3xl mx-auto mb-6" style="color: #cbd5e1;">
            {{ project.description }}
          </p>

          <!-- Technologies -->
          <div class="flex flex-wrap gap-2 justify-center">
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
const newsletter = ref([])
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
  newsletter.value = []

  try {
    const response = await api.get('/lastfm/ranking/latest')
    rankings.value = response.data
    // Update selectedDate with the actual date from the data
    if (response.data.length > 0) {
      selectedDate.value = response.data[0].data
      // Fetch newsletter for the same date
      await fetchNewsletter()
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

// Fetch newsletter data for specific date
const fetchNewsletter = async () => {
  if (!selectedDate.value) return

  try {
    const response = await api.get(`/lastfm/newsletter/${selectedDate.value}`)
    newsletter.value = response.data
  } catch (err) {
    console.error('Error fetching newsletter:', err)
    // Don't show error for newsletter, it's optional
  }
}

// Fetch ranking data for specific date
const fetchRanking = async () => {
  if (!selectedDate.value) return

  loading.value = true
  error.value = null
  rankings.value = []
  newsletter.value = []

  try {
    // Fetch both ranking and newsletter in parallel
    const [rankingResponse] = await Promise.all([
      api.get(`/lastfm/ranking/${selectedDate.value}`),
      fetchNewsletter()
    ])
    rankings.value = rankingResponse.data
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

// Initialize with yesterday's data
onMounted(() => {
  // Calculate yesterday's date
  const yesterday = new Date()
  yesterday.setDate(yesterday.getDate() - 1)
  selectedDate.value = yesterday.toISOString().split('T')[0]

  // Fetch data for yesterday
  fetchRanking()
})
</script>

<style scoped>
/* Flip Card 3D Effect */
.flip-card-container {
  position: relative;
  perspective: 1000px;
  cursor: pointer;
  width: 100%;
  aspect-ratio: 1;
}

.flip-card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  transition: transform 0.6s;
  transform-style: preserve-3d;
}

.flip-card-container:hover .flip-card-inner {
  transform: rotateY(180deg);
}

.flip-card-front,
.flip-card-back {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
}

.flip-card-front {
  z-index: 2;
}

.flip-card-back {
  transform: rotateY(180deg);
}
</style>
