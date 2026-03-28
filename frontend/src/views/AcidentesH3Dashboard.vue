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
            <span class="px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider" style="background-color: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3);">
              Powered by H3
            </span>
            <span class="px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider" style="background-color: rgba(251, 191, 36, 0.2); color: #fbbf24; border: 1px solid rgba(251, 191, 36, 0.3);">
              ClickHouse
            </span>
            <span class="px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider" style="background-color: rgba(34, 197, 94, 0.2); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.3);">
              Live Data
            </span>
          </div>
          <h1 class="text-5xl md:text-6xl lg:text-7xl font-bold mb-4" style="color: #ffffff;">
            Highway Accidents H3
          </h1>
          <div class="w-24 h-1 mx-auto mb-6" style="background: linear-gradient(90deg, #ef4444, #f59e0b);"></div>
          <p class="text-lg max-w-2xl mx-auto" style="color: #94a3b8;">
            Geospatial analysis of Brazilian federal highway accidents using
            <span class="font-semibold" style="color: #f87171;">Uber's H3</span>
            hexagonal indexing, powered by
            <span class="font-semibold" style="color: #fbbf24;">ClickHouse</span>.
            Data from PRF (Jan-Feb 2026).
          </p>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="text-center py-12">
          <i class="pi pi-spin pi-spinner text-4xl" style="color: #ef4444;"></i>
          <p class="mt-4 text-lg" style="color: #cbd5e1;">Loading accident data from ClickHouse...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="rounded-xl p-6 text-center" style="background-color: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3);">
          <i class="pi pi-exclamation-triangle text-4xl mb-4" style="color: #ef4444;"></i>
          <p class="text-lg font-semibold mb-2" style="color: #fca5a5;">{{ error }}</p>
          <button @click="fetchAll" class="mt-4 px-4 py-2 rounded-lg text-sm font-medium" style="background-color: #dc2626; color: #ffffff;">
            Retry
          </button>
        </div>

        <!-- Dashboard Content -->
        <div v-else>
          <!-- Data Source Banner -->
          <div class="flex items-center gap-3 rounded-lg px-4 py-3 mb-6" style="background-color: rgba(239, 68, 68, 0.08); border: 1px solid rgba(239, 68, 68, 0.2);">
            <i class="pi pi-database" style="color: #ef4444;"></i>
            <span class="text-sm" style="color: #cbd5e1;">
              Data source: <span class="font-semibold" style="color: #f87171;">ClickHouse</span>
              &mdash; Brazilian Federal Highway Police (PRF) open data, H3 resolution 8
            </span>
          </div>

          <!-- Summary Cards -->
          <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
            <div class="rounded-xl p-5" style="background-color: #1e293b; border: 1px solid #334155;">
              <div class="flex items-center gap-3 mb-3">
                <div class="w-10 h-10 rounded-lg flex items-center justify-center" style="background-color: rgba(239, 68, 68, 0.2);">
                  <i class="pi pi-car text-lg" style="color: #ef4444;"></i>
                </div>
                <span class="text-xs font-medium uppercase tracking-wider" style="color: #94a3b8;">Accidents</span>
              </div>
              <p class="text-3xl font-bold" style="color: #ffffff;">{{ Number(summary.total_acidentes || 0).toLocaleString() }}</p>
            </div>

            <div class="rounded-xl p-5" style="background-color: #1e293b; border: 1px solid #334155;">
              <div class="flex items-center gap-3 mb-3">
                <div class="w-10 h-10 rounded-lg flex items-center justify-center" style="background-color: rgba(251, 191, 36, 0.2);">
                  <i class="pi pi-users text-lg" style="color: #fbbf24;"></i>
                </div>
                <span class="text-xs font-medium uppercase tracking-wider" style="color: #94a3b8;">Involved</span>
              </div>
              <p class="text-3xl font-bold" style="color: #ffffff;">{{ Number(summary.total_envolvidos || 0).toLocaleString() }}</p>
            </div>

            <div class="rounded-xl p-5" style="background-color: #1e293b; border: 1px solid #334155;">
              <div class="flex items-center gap-3 mb-3">
                <div class="w-10 h-10 rounded-lg flex items-center justify-center" style="background-color: rgba(220, 38, 38, 0.2);">
                  <i class="pi pi-heart text-lg" style="color: #dc2626;"></i>
                </div>
                <span class="text-xs font-medium uppercase tracking-wider" style="color: #94a3b8;">Deaths</span>
              </div>
              <p class="text-3xl font-bold" style="color: #ffffff;">{{ Number(summary.total_mortos || 0).toLocaleString() }}</p>
            </div>

            <div class="rounded-xl p-5" style="background-color: #1e293b; border: 1px solid #334155;">
              <div class="flex items-center gap-3 mb-3">
                <div class="w-10 h-10 rounded-lg flex items-center justify-center" style="background-color: rgba(251, 146, 60, 0.2);">
                  <i class="pi pi-exclamation-circle text-lg" style="color: #fb923c;"></i>
                </div>
                <span class="text-xs font-medium uppercase tracking-wider" style="color: #94a3b8;">Severe Injuries</span>
              </div>
              <p class="text-3xl font-bold" style="color: #ffffff;">{{ Number(summary.total_feridos_graves || 0).toLocaleString() }}</p>
            </div>
          </div>

          <!-- H3 Map -->
          <div class="rounded-2xl overflow-hidden mb-8" style="border: 1px solid #334155;">
            <div class="flex items-center justify-between px-6 py-4" style="background-color: #1e293b;">
              <div class="flex items-center gap-3">
                <i class="pi pi-map text-xl" style="color: #ef4444;"></i>
                <h2 class="text-xl font-bold" style="color: #ffffff;">H3 Hexagonal Heatmap</h2>
              </div>
              <div class="flex gap-2">
                <button
                  v-for="m in metrics"
                  :key="m.key"
                  @click="selectedMetric = m.key; fetchHexagons()"
                  class="px-3 py-1.5 rounded-lg text-xs font-medium transition-all"
                  :style="selectedMetric === m.key
                    ? 'background-color: rgba(239, 68, 68, 0.3); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.5);'
                    : 'background-color: #0f172a; color: #94a3b8; border: 1px solid #334155;'"
                >
                  {{ m.label }}
                </button>
              </div>
            </div>
            <div ref="mapContainer" style="height: 500px; width: 100%;"></div>
          </div>

          <!-- Charts Row -->
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
            <!-- Accidents by Hour -->
            <div class="rounded-2xl p-6 md:p-8" style="background-color: #1e293b; border: 1px solid #334155;">
              <div class="flex items-center gap-3 mb-6">
                <i class="pi pi-clock text-xl" style="color: #fbbf24;"></i>
                <h2 class="text-xl font-bold" style="color: #ffffff;">Accidents by Hour</h2>
              </div>
              <div class="flex items-end gap-1 h-40">
                <div
                  v-for="h in hourlyData"
                  :key="h.hora"
                  class="flex-1 flex flex-col items-center gap-1"
                >
                  <span class="text-[9px] font-medium" style="color: #cbd5e1;">{{ h.total_acidentes }}</span>
                  <div
                    class="w-full rounded-t-sm transition-all"
                    :style="{
                      height: barHeight(h.total_acidentes, hourlyData, 'total_acidentes') + '%',
                      background: Number(h.total_mortos) > 50
                        ? 'linear-gradient(to top, #dc2626, #ef4444)'
                        : 'linear-gradient(to top, #f59e0b, #fbbf24)',
                      minHeight: '4px'
                    }"
                  ></div>
                  <span class="text-[9px] mt-1" style="color: #64748b;">{{ h.hora }}h</span>
                </div>
              </div>
            </div>

            <!-- Accidents by Day of Week -->
            <div class="rounded-2xl p-6 md:p-8" style="background-color: #1e293b; border: 1px solid #334155;">
              <div class="flex items-center gap-3 mb-6">
                <i class="pi pi-calendar text-xl" style="color: #38bdf8;"></i>
                <h2 class="text-xl font-bold" style="color: #ffffff;">Accidents by Day of Week</h2>
              </div>
              <div class="space-y-3">
                <div
                  v-for="d in dowData"
                  :key="d.dia_semana"
                  class="flex items-center gap-3"
                >
                  <span class="text-xs w-24 text-right truncate" style="color: #94a3b8;">{{ formatDow(d.dia_semana) }}</span>
                  <div class="flex-1 rounded-full h-6 overflow-hidden" style="background-color: #0f172a;">
                    <div
                      class="h-full rounded-full flex items-center px-2 transition-all"
                      :style="{
                        width: barWidth(d.total_acidentes, dowData, 'total_acidentes') + '%',
                        background: 'linear-gradient(90deg, #3b82f6, #38bdf8)',
                        minWidth: '40px'
                      }"
                    >
                      <span class="text-[10px] font-bold" style="color: #ffffff;">{{ d.total_acidentes }}</span>
                    </div>
                  </div>
                  <span class="text-xs font-mono w-16 text-right" style="color: #f87171;">{{ d.taxa_letalidade }}%</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Top Causes Table -->
          <div class="rounded-2xl p-6 md:p-8 mb-8" style="background-color: #1e293b; border: 1px solid #334155;">
            <div class="flex items-center gap-3 mb-6">
              <i class="pi pi-exclamation-triangle text-xl" style="color: #ef4444;"></i>
              <h2 class="text-xl font-bold" style="color: #ffffff;">Top Accident Causes</h2>
            </div>
            <div class="overflow-x-auto">
              <table class="w-full text-sm">
                <thead>
                  <tr style="border-bottom: 2px solid #334155;">
                    <th class="text-left py-3 px-3 font-semibold" style="color: #94a3b8;">Cause</th>
                    <th class="text-right py-3 px-3 font-semibold" style="color: #94a3b8;">Accidents</th>
                    <th class="text-right py-3 px-3 font-semibold" style="color: #94a3b8;">Deaths</th>
                    <th class="text-right py-3 px-3 font-semibold" style="color: #94a3b8;">Lethality</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="c in causeData"
                    :key="c.causa_acidente"
                    class="transition-colors"
                    style="border-bottom: 1px solid #1e293b;"
                    @mouseenter="$event.currentTarget.style.backgroundColor = '#0f172a'"
                    @mouseleave="$event.currentTarget.style.backgroundColor = 'transparent'"
                  >
                    <td class="py-3 px-3">
                      <span class="font-medium" style="color: #e2e8f0;">{{ c.causa_acidente }}</span>
                    </td>
                    <td class="py-3 px-3 text-right font-mono" style="color: #cbd5e1;">{{ Number(c.total_acidentes).toLocaleString() }}</td>
                    <td class="py-3 px-3 text-right font-mono" style="color: #f87171;">{{ c.total_mortos }}</td>
                    <td class="py-3 px-3 text-right">
                      <span
                        class="px-2 py-1 rounded-full text-xs font-semibold"
                        :style="Number(c.taxa_letalidade) > 20
                          ? 'background-color: rgba(220, 38, 38, 0.2); color: #f87171;'
                          : Number(c.taxa_letalidade) > 8
                            ? 'background-color: rgba(251, 191, 36, 0.2); color: #fbbf24;'
                            : 'background-color: rgba(34, 197, 94, 0.2); color: #4ade80;'"
                      >{{ c.taxa_letalidade }}%</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Top Highways Table -->
          <div class="rounded-2xl p-6 md:p-8 mb-8" style="background-color: #1e293b; border: 1px solid #334155;">
            <div class="flex items-center gap-3 mb-6">
              <i class="pi pi-directions text-xl" style="color: #fbbf24;"></i>
              <h2 class="text-xl font-bold" style="color: #ffffff;">Most Dangerous Highways</h2>
            </div>
            <div class="overflow-x-auto">
              <table class="w-full text-sm">
                <thead>
                  <tr style="border-bottom: 2px solid #334155;">
                    <th class="text-left py-3 px-3 font-semibold" style="color: #94a3b8;">Highway</th>
                    <th class="text-left py-3 px-3 font-semibold" style="color: #94a3b8;">State</th>
                    <th class="text-right py-3 px-3 font-semibold" style="color: #94a3b8;">Accidents</th>
                    <th class="text-right py-3 px-3 font-semibold" style="color: #94a3b8;">Deaths</th>
                    <th class="text-right py-3 px-3 font-semibold" style="color: #94a3b8;">Lethality</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="h in highwayData"
                    :key="h.rodovia + h.uf"
                    class="transition-colors"
                    style="border-bottom: 1px solid #1e293b;"
                    @mouseenter="$event.currentTarget.style.backgroundColor = '#0f172a'"
                    @mouseleave="$event.currentTarget.style.backgroundColor = 'transparent'"
                  >
                    <td class="py-3 px-3">
                      <span class="font-bold" style="color: #fbbf24;">{{ h.rodovia }}</span>
                    </td>
                    <td class="py-3 px-3">
                      <span class="px-2 py-0.5 rounded text-xs font-semibold" style="background-color: rgba(56, 189, 248, 0.15); color: #38bdf8;">{{ h.uf }}</span>
                    </td>
                    <td class="py-3 px-3 text-right font-mono" style="color: #cbd5e1;">{{ Number(h.total_acidentes).toLocaleString() }}</td>
                    <td class="py-3 px-3 text-right font-mono" style="color: #f87171;">{{ h.total_mortos }}</td>
                    <td class="py-3 px-3 text-right">
                      <span
                        class="px-2 py-1 rounded-full text-xs font-semibold"
                        :style="Number(h.taxa_letalidade) > 8
                          ? 'background-color: rgba(220, 38, 38, 0.2); color: #f87171;'
                          : 'background-color: rgba(34, 197, 94, 0.2); color: #4ade80;'"
                      >{{ h.taxa_letalidade }}%</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- How it Works -->
          <div class="rounded-2xl p-6 md:p-8 mb-8" style="background-color: #1e293b; border: 1px solid #334155;">
            <h2 class="text-2xl font-bold mb-6 text-center" style="color: #ffffff;">
              <i class="pi pi-cog mr-2" style="color: #ef4444;"></i>
              How it Works
            </h2>

            <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div class="text-center p-4">
                <div class="w-16 h-16 mx-auto mb-4 rounded-full flex items-center justify-center" style="background-color: rgba(239, 68, 68, 0.2);">
                  <i class="pi pi-database text-2xl" style="color: #ef4444;"></i>
                </div>
                <h3 class="font-bold mb-2" style="color: #ffffff;">1. Open Data</h3>
                <p class="text-sm" style="color: #9ca3af;">
                  31,725 accident records from PRF (Brazilian Federal Highway Police) with lat/lng coordinates
                </p>
              </div>

              <div class="text-center p-4">
                <div class="w-16 h-16 mx-auto mb-4 rounded-full flex items-center justify-center" style="background-color: rgba(251, 191, 36, 0.2);">
                  <i class="pi pi-bolt text-2xl" style="color: #fbbf24;"></i>
                </div>
                <h3 class="font-bold mb-2" style="color: #ffffff;">2. ClickHouse</h3>
                <p class="text-sm" style="color: #9ca3af;">
                  Column-oriented OLAP database with native H3 functions for blazing-fast geospatial aggregations
                </p>
              </div>

              <div class="text-center p-4">
                <div class="w-16 h-16 mx-auto mb-4 rounded-full flex items-center justify-center" style="background-color: rgba(56, 189, 248, 0.2);">
                  <i class="pi pi-th-large text-2xl" style="color: #38bdf8;"></i>
                </div>
                <h3 class="font-bold mb-2" style="color: #ffffff;">3. H3 Indexing</h3>
                <p class="text-sm" style="color: #9ca3af;">
                  Uber's hierarchical hexagonal grid system converts lat/lng into spatial indexes at resolution 8
                </p>
              </div>

              <div class="text-center p-4">
                <div class="w-16 h-16 mx-auto mb-4 rounded-full flex items-center justify-center" style="background-color: rgba(34, 197, 94, 0.2);">
                  <i class="pi pi-map text-2xl" style="color: #22c55e;"></i>
                </div>
                <h3 class="font-bold mb-2" style="color: #ffffff;">4. Visualization</h3>
                <p class="text-sm" style="color: #9ca3af;">
                  Interactive map renders H3 hexagons as colored polygons, revealing accident hotspots across Brazil
                </p>
              </div>
            </div>
          </div>

          <!-- Tech Stack -->
          <div class="rounded-2xl p-6 md:p-8 text-center" style="background-color: #1e293b; border: 1px solid #334155;">
            <p class="text-lg max-w-3xl mx-auto mb-6" style="color: #cbd5e1;">
              {{ project.description }}
            </p>
            <div class="flex flex-wrap gap-2 justify-center">
              <span
                v-for="tech in project.technologies"
                :key="tech"
                class="px-3 py-1.5 rounded-lg text-sm font-medium"
                style="background-color: rgba(239, 68, 68, 0.15); color: #fca5a5; border: 1px solid rgba(239, 68, 68, 0.3);"
              >
                {{ tech }}
              </span>
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
          style="background-color: #dc2626; color: #ffffff;"
        >
          <i class="pi pi-arrow-left"></i>
          Back to Portfolio
        </router-link>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { projects } from '../data/portfolio.js'
import api from '../services/api'

const project = projects.find(p => p.slug === 'acidentes-h3') || projects[0]

const loading = ref(true)
const error = ref(null)
const mapContainer = ref(null)
let map = null

const summary = ref({})
const hexagons = ref([])
const hourlyData = ref([])
const causeData = ref([])
const highwayData = ref([])
const dowData = ref([])
const selectedMetric = ref('acidentes')

const metrics = [
  { key: 'acidentes', label: 'Accidents' },
  { key: 'mortos', label: 'Deaths' },
  { key: 'letalidade', label: 'Lethality %' },
]

const fetchAll = async () => {
  loading.value = true
  error.value = null
  try {
    const [summaryRes, hexRes, hourRes, causeRes, hwRes, dowRes] = await Promise.all([
      api.get('/acidentes/summary'),
      api.get('/acidentes/h3-hexagons', { params: { metric: selectedMetric.value } }),
      api.get('/acidentes/by-hour'),
      api.get('/acidentes/by-cause'),
      api.get('/acidentes/by-highway'),
      api.get('/acidentes/by-day-of-week'),
    ])
    summary.value = summaryRes.data
    hexagons.value = hexRes.data
    hourlyData.value = hourRes.data
    causeData.value = causeRes.data
    highwayData.value = hwRes.data
    dowData.value = dowRes.data

    await nextTick()
    initMap()
  } catch (err) {
    console.error('Error fetching data:', err)
    error.value = 'Failed to load data from ClickHouse. Please try again.'
  } finally {
    loading.value = false
  }
}

const fetchHexagons = async () => {
  try {
    const res = await api.get('/acidentes/h3-hexagons', { params: { metric: selectedMetric.value } })
    hexagons.value = res.data
    updateMapLayer()
  } catch (err) {
    console.error('Error fetching hexagons:', err)
  }
}

function h3ToPolygon(h3Index) {
  // Convert H3 index to polygon coordinates using the h3-js library loaded via CDN
  if (!window.h3) return null
  const boundary = window.h3.cellToBoundary(h3Index)
  // h3-js returns [lat, lng] pairs, MapLibre needs [lng, lat]
  const coords = boundary.map(([lat, lng]) => [lng, lat])
  coords.push(coords[0]) // close the polygon
  return coords
}

function getColor(value, maxValue) {
  const ratio = Math.min(value / (maxValue || 1), 1)
  if (ratio < 0.25) return 'rgba(254, 240, 138, 0.6)'  // yellow light
  if (ratio < 0.5) return 'rgba(251, 191, 36, 0.7)'    // amber
  if (ratio < 0.75) return 'rgba(249, 115, 22, 0.8)'   // orange
  return 'rgba(220, 38, 38, 0.9)'                       // red
}

function buildGeoJSON() {
  const maxValue = Math.max(...hexagons.value.map(h => Number(h.value)), 1)
  const features = []

  for (const hex of hexagons.value) {
    const coords = h3ToPolygon(hex.h3_index)
    if (!coords) continue

    features.push({
      type: 'Feature',
      properties: {
        h3: hex.h3_index,
        value: Number(hex.value),
        acidentes: Number(hex.acidentes),
        mortos: Number(hex.mortos),
        municipio: hex.municipio,
        uf: hex.uf,
        rodovia: hex.rodovia,
        color: getColor(Number(hex.value), maxValue),
      },
      geometry: {
        type: 'Polygon',
        coordinates: [coords],
      },
    })
  }

  return { type: 'FeatureCollection', features }
}

function initMap() {
  if (!mapContainer.value || !window.maplibregl) return

  map = new window.maplibregl.Map({
    container: mapContainer.value,
    style: {
      version: 8,
      sources: {
        osm: {
          type: 'raster',
          tiles: ['https://tile.openstreetmap.org/{z}/{x}/{y}.png'],
          tileSize: 256,
          attribution: '&copy; OpenStreetMap contributors',
        },
      },
      layers: [
        {
          id: 'osm',
          type: 'raster',
          source: 'osm',
          paint: { 'raster-saturation': -0.8, 'raster-brightness-max': 0.4 },
        },
      ],
    },
    center: [-49.5, -15.5],
    zoom: 4,
  })

  map.addControl(new window.maplibregl.NavigationControl(), 'top-right')

  map.on('load', () => {
    updateMapLayer()

    // Popup on click
    map.on('click', 'h3-fill', (e) => {
      const props = e.features[0].properties
      new window.maplibregl.Popup({ className: 'h3-popup' })
        .setLngLat(e.lngLat)
        .setHTML(`
          <div style="color:#111827;font-size:13px;line-height:1.5;">
            <strong>${props.municipio} - ${props.uf}</strong><br/>
            <span style="color:#6b7280;">${props.rodovia}</span><br/>
            <hr style="margin:4px 0;border-color:#e5e7eb;"/>
            Accidents: <strong>${props.acidentes}</strong><br/>
            Deaths: <strong style="color:#dc2626;">${props.mortos}</strong>
          </div>
        `)
        .addTo(map)
    })

    map.on('mouseenter', 'h3-fill', () => { map.getCanvas().style.cursor = 'pointer' })
    map.on('mouseleave', 'h3-fill', () => { map.getCanvas().style.cursor = '' })
  })
}

function updateMapLayer() {
  if (!map || !map.isStyleLoaded()) return

  const geojson = buildGeoJSON()

  if (map.getSource('h3-source')) {
    map.getSource('h3-source').setData(geojson)
  } else {
    map.addSource('h3-source', { type: 'geojson', data: geojson })

    map.addLayer({
      id: 'h3-fill',
      type: 'fill',
      source: 'h3-source',
      paint: {
        'fill-color': ['get', 'color'],
        'fill-opacity': 0.8,
      },
    })

    map.addLayer({
      id: 'h3-outline',
      type: 'line',
      source: 'h3-source',
      paint: {
        'line-color': 'rgba(255, 255, 255, 0.3)',
        'line-width': 0.5,
      },
    })
  }
}

const barHeight = (value, data, field) => {
  const max = Math.max(...data.map(d => Number(d[field])), 1)
  return Math.max((Number(value) / max) * 100, 3)
}

const barWidth = (value, data, field) => {
  const max = Math.max(...data.map(d => Number(d[field])), 1)
  return Math.max((Number(value) / max) * 100, 10)
}

const formatDow = (day) => {
  const map = {
    'segunda-feira': 'Mon',
    'terça-feira': 'Tue',
    'quarta-feira': 'Wed',
    'quinta-feira': 'Thu',
    'sexta-feira': 'Fri',
    'sábado': 'Sat',
    'domingo': 'Sun',
  }
  return map[day] || day
}

onMounted(fetchAll)

onBeforeUnmount(() => {
  if (map) {
    map.remove()
    map = null
  }
})
</script>
