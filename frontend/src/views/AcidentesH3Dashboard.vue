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
                      <span class="font-medium" style="color: #e2e8f0;">{{ tr('causa_acidente', c.causa_acidente) }}</span>
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

    <!-- Drawer: origins of a clicked hex -->
    <transition name="drawer">
      <div
        v-if="drawerOpen"
        class="fixed inset-0 z-50 flex"
        role="dialog"
        aria-modal="true"
        aria-labelledby="drawer-title"
      >
        <!-- Backdrop -->
        <div class="flex-1" style="background-color: rgba(0,0,0,0.55);" @click="closeDrawer"></div>
        <!-- Panel -->
        <aside
          class="w-full max-w-xl h-full overflow-hidden flex flex-col shadow-2xl"
          style="background-color: #0f172a; border-left: 1px solid #1e293b;"
        >
          <header class="px-6 py-4 flex items-start justify-between gap-3" style="border-bottom: 1px solid #1e293b;">
            <div class="min-w-0">
              <div class="flex items-center gap-2 mb-1">
                <span class="px-2 py-0.5 rounded text-xs font-semibold" style="background-color: rgba(239,68,68,0.15); color: #f87171;">
                  H3 Hex
                </span>
                <span class="text-xs font-mono truncate" style="color: #64748b;">{{ drawerHex?.h3_hex }}</span>
              </div>
              <h3 id="drawer-title" class="text-lg font-bold truncate" style="color: #ffffff;">
                {{ drawerHex?.municipio }} <span style="color: #94a3b8; font-weight: 500;">— {{ drawerHex?.uf }}</span>
              </h3>
              <p class="text-sm mt-0.5" style="color: #94a3b8;">
                {{ drawerHex?.acidentes }} accidents · {{ drawerHex?.mortos }} deaths
              </p>
            </div>
            <button
              @click="closeDrawer"
              aria-label="Close origins panel"
              class="flex-shrink-0 w-9 h-9 rounded-lg flex items-center justify-center transition-colors"
              style="background-color: #1e293b; color: #cbd5e1;"
            >
              <i class="pi pi-times"></i>
            </button>
          </header>

          <!-- Filters -->
          <div class="px-6 py-3 flex items-center gap-2" style="border-bottom: 1px solid #1e293b;">
            <button
              v-for="f in [
                { key: 'all', label: 'All', count: drawerOrigins.length },
                { key: 'fatal', label: 'Fatal', count: drawerOrigins.filter(r => Number(r.mortos) > 0).length },
                { key: 'serious', label: 'Serious', count: drawerOrigins.filter(r => Number(r.feridos_graves) > 0 && Number(r.mortos) === 0).length },
              ]"
              :key="f.key"
              @click="drawerFilter = f.key"
              class="px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors"
              :style="drawerFilter === f.key
                ? 'background-color: #dc2626; color: #ffffff;'
                : 'background-color: #1e293b; color: #94a3b8;'"
            >
              {{ f.label }} <span style="opacity: 0.75;">({{ f.count }})</span>
            </button>
          </div>

          <!-- Body -->
          <div class="flex-1 overflow-y-auto px-2 py-3" aria-live="polite">
            <div v-if="drawerLoading" class="flex items-center justify-center py-12" style="color: #94a3b8;">
              <i class="pi pi-spin pi-spinner text-2xl mr-3"></i>
              Loading origin accidents...
            </div>

            <div v-else-if="drawerError" class="mx-4 p-4 rounded-lg" style="background-color: rgba(239, 68, 68, 0.08); border: 1px solid rgba(239, 68, 68, 0.3);">
              <p class="text-sm" style="color: #f87171;">{{ drawerError }}</p>
            </div>

            <div v-else-if="filteredOrigins.length === 0" class="text-center py-12" style="color: #64748b;">
              <i class="pi pi-inbox text-3xl mb-3 block"></i>
              <p class="text-sm">No accidents match this filter.</p>
            </div>

            <ul v-else class="space-y-2 px-2">
              <li
                v-for="row in filteredOrigins"
                :key="row.id"
                class="rounded-lg p-3 cursor-pointer transition-colors"
                style="background-color: #1e293b; border: 1px solid transparent;"
                @click="focusOrigin(row)"
                @mouseenter="ev => ev.currentTarget.style.borderColor = '#38bdf8'"
                @mouseleave="ev => ev.currentTarget.style.borderColor = 'transparent'"
              >
                <div class="flex items-start justify-between gap-3 mb-1.5">
                  <div class="flex items-center gap-2 min-w-0">
                    <span class="text-xs font-mono px-1.5 py-0.5 rounded" style="background-color: #0f172a; color: #7dd3fc;">
                      {{ formatDate(row.data) }} {{ String(row.horario || '').slice(0, 5) }}
                    </span>
                    <span class="text-xs" style="color: #94a3b8;">{{ trDow(row.dia_semana) }}</span>
                  </div>
                  <div class="flex items-center gap-1 text-xs font-semibold flex-shrink-0">
                    <span v-if="Number(row.mortos) > 0" class="px-1.5 py-0.5 rounded" style="background-color: rgba(220,38,38,0.2); color: #fca5a5;">
                      ✝ {{ row.mortos }}
                    </span>
                    <span v-if="Number(row.feridos_graves) > 0" class="px-1.5 py-0.5 rounded" style="background-color: rgba(245,158,11,0.2); color: #fcd34d;">
                      ▲ {{ row.feridos_graves }}
                    </span>
                    <span v-if="Number(row.feridos_leves) > 0" class="px-1.5 py-0.5 rounded" style="background-color: rgba(59,130,246,0.2); color: #93c5fd;">
                      ~ {{ row.feridos_leves }}
                    </span>
                  </div>
                </div>
                <div class="text-sm font-semibold mb-1" style="color: #e2e8f0;">
                  {{ tr('tipo_acidente', row.tipo_acidente) }}
                </div>
                <div class="text-xs mb-2" style="color: #94a3b8;">
                  {{ row.rodovia }} · km {{ Number(row.km).toFixed(1) }} · {{ tr('classificacao_acidente', row.classificacao_acidente) }}
                </div>
                <div class="text-xs italic" style="color: #cbd5e1;">
                  {{ tr('causa_acidente', row.causa_acidente) }}
                </div>
                <div class="flex flex-wrap gap-1.5 mt-2">
                  <span v-if="row.condicao_metereologica && row.condicao_metereologica !== 'Céu Claro'"
                        class="text-xs px-1.5 py-0.5 rounded" style="background-color: #0f172a; color: #94a3b8;">
                    ☁ {{ tr('condicao_metereologica', row.condicao_metereologica) }}
                  </span>
                  <span v-if="row.fase_dia" class="text-xs px-1.5 py-0.5 rounded" style="background-color: #0f172a; color: #94a3b8;">
                    {{ tr('fase_dia', row.fase_dia) }}
                  </span>
                  <span v-if="row.tracado_via" class="text-xs px-1.5 py-0.5 rounded" style="background-color: #0f172a; color: #94a3b8;">
                    {{ tr('tracado_via', row.tracado_via) }}
                  </span>
                </div>
              </li>
            </ul>
          </div>

          <footer class="px-6 py-3 text-xs" style="background-color: #0f172a; color: #64748b; border-top: 1px solid #1e293b;">
            Click a row to pinpoint on the map. Showing up to 100 accidents ordered by severity.
          </footer>
        </aside>
      </div>
    </transition>

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
import { ref, computed, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { cellToBoundary } from 'h3-js'
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

// Drawer state (origins viewer)
const drawerOpen = ref(false)
const drawerLoading = ref(false)
const drawerError = ref(null)
const drawerHex = ref(null)      // { h3_hex, municipio, uf, acidentes, mortos }
const drawerOrigins = ref([])    // raw rows from /origins
const drawerFilter = ref('all')  // 'all' | 'fatal' | 'serious'
const originsCache = new Map()   // client-side cache keyed by h3_hex
let highlightMarker = null       // maplibre marker for the selected row

const metrics = [
  { key: 'acidentes', label: 'Accidents' },
  { key: 'mortos', label: 'Deaths' },
  { key: 'letalidade', label: 'Lethality %' },
]

const fetchAll = async () => {
  loading.value = true
  error.value = null
  try {
    const [summaryRes, hexRes] = await Promise.all([
      api.get('/acidentes/summary'),
      api.get('/acidentes/h3-hexagons', { params: { metric: selectedMetric.value } }),
    ])
    summary.value = summaryRes.data
    hexagons.value = hexRes.data
  } catch {
    error.value = 'Failed to load data from ClickHouse. Please try again.'
  } finally {
    loading.value = false
    await nextTick()
    initMap()
  }
  // Load charts in background (non-blocking)
  try {
    const [hourRes, causeRes, hwRes, dowRes] = await Promise.all([
      api.get('/acidentes/by-hour'),
      api.get('/acidentes/by-cause'),
      api.get('/acidentes/by-highway'),
      api.get('/acidentes/by-day-of-week'),
    ])
    hourlyData.value = hourRes.data
    causeData.value = causeRes.data
    highwayData.value = hwRes.data
    dowData.value = dowRes.data
  } catch {
    // charts are optional, don't block
  }
}

const fetchHexagons = async () => {
  try {
    const res = await api.get('/acidentes/h3-hexagons', { params: { metric: selectedMetric.value } })
    hexagons.value = res.data
    updateMapLayer()
  } catch {
    // silently handle metric switch errors
  }
}

function getColor(value, maxValue) {
  const ratio = Math.min(value / (maxValue || 1), 1)
  if (ratio < 0.2) return '#fca5a5'   // light red
  if (ratio < 0.4) return '#f87171'   // medium light
  if (ratio < 0.6) return '#ef4444'   // medium
  if (ratio < 0.8) return '#dc2626'   // dark
  return '#991b1b'                     // darkest
}

function buildHexGeoJSON() {
  const maxValue = Math.max(...hexagons.value.map(h => Number(h.value)), 1)
  const features = []

  for (const hex of hexagons.value) {
    if (!hex.h3_hex) continue
    // cellToBoundary already returns [lng, lat] in h3-js v4
    const boundary = cellToBoundary(hex.h3_hex)
    const coords = [...boundary]
    coords.push(coords[0]) // close polygon

    features.push({
      type: 'Feature',
      properties: {
        h3_hex: hex.h3_hex,
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

async function openOriginsDrawer(props) {
  // Reset highlight marker from any previous selection
  if (highlightMarker) {
    highlightMarker.remove()
    highlightMarker = null
  }
  drawerHex.value = {
    h3_hex: props.h3_hex,
    municipio: props.municipio,
    uf: props.uf,
    rodovia: props.rodovia,
    acidentes: props.acidentes,
    mortos: props.mortos,
  }
  drawerFilter.value = 'all'
  drawerOpen.value = true
  drawerError.value = null

  // Cache hit — reuse without round-trip
  const cached = originsCache.get(props.h3_hex)
  if (cached) {
    drawerOrigins.value = cached
    return
  }

  drawerLoading.value = true
  drawerOrigins.value = []
  try {
    const res = await api.get(`/acidentes/h3-hexagons/${encodeURIComponent(props.h3_hex)}/origins`, {
      params: { limit: 100 },
    })
    drawerOrigins.value = res.data
    originsCache.set(props.h3_hex, res.data)
  } catch {
    drawerError.value = 'Failed to load origin accidents. Please try again.'
  } finally {
    drawerLoading.value = false
  }
}

function closeDrawer() {
  drawerOpen.value = false
  if (highlightMarker) {
    highlightMarker.remove()
    highlightMarker = null
  }
}

function focusOrigin(row) {
  if (!map || !row.latitude || !row.longitude) return
  const lng = Number(row.longitude)
  const lat = Number(row.latitude)
  if (!Number.isFinite(lng) || !Number.isFinite(lat)) return
  if (highlightMarker) highlightMarker.remove()
  const el = document.createElement('div')
  el.style.cssText =
    'width:18px;height:18px;border-radius:50%;background:#fbbf24;box-shadow:0 0 0 4px rgba(251,191,36,0.35),0 0 12px rgba(251,191,36,0.6);border:2px solid #fff;'
  highlightMarker = new window.maplibregl.Marker({ element: el }).setLngLat([lng, lat]).addTo(map)
  map.flyTo({ center: [lng, lat], zoom: 15, speed: 1.6 })
}

const filteredOrigins = computed(() => {
  const rows = drawerOrigins.value
  if (drawerFilter.value === 'fatal') return rows.filter(r => Number(r.mortos) > 0)
  if (drawerFilter.value === 'serious') return rows.filter(r => Number(r.feridos_graves) > 0 && Number(r.mortos) === 0)
  return rows
})

function formatDate(iso) {
  if (!iso) return ''
  const parts = iso.split('-')
  if (parts.length !== 3) return iso
  return `${parts[2]}/${parts[1]}/${parts[0]}`
}

function initMap() {
  if (!mapContainer.value || !window.maplibregl) return

  map = new window.maplibregl.Map({
    container: mapContainer.value,
    style: {
      version: 8,
      sources: {
        'carto-dark': {
          type: 'raster',
          tiles: ['https://basemaps.cartocdn.com/dark_all/{z}/{x}/{y}@2x.png'],
          tileSize: 256,
          attribution: '&copy; CARTO &copy; OpenStreetMap contributors',
        },
      },
      layers: [
        {
          id: 'carto-dark',
          type: 'raster',
          source: 'carto-dark',
        },
      ],
    },
    center: [-43.2, -22.9],
    zoom: 13,
  })

  map.addControl(new window.maplibregl.NavigationControl(), 'top-right')

  map.on('load', () => {
    updateMapLayer()

    map.on('click', 'h3-fill', (e) => {
      openOriginsDrawer(e.features[0].properties)
    })

    map.on('mouseenter', 'h3-fill', () => { map.getCanvas().style.cursor = 'pointer' })
    map.on('mouseleave', 'h3-fill', () => { map.getCanvas().style.cursor = '' })
  })
}

function updateMapLayer() {
  if (!map) return

  const geojson = buildHexGeoJSON()

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
        'fill-opacity': 0.75,
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
  const days = {
    'segunda-feira': 'Mon',
    'terça-feira': 'Tue',
    'quarta-feira': 'Wed',
    'quinta-feira': 'Thu',
    'sexta-feira': 'Fri',
    'sábado': 'Sat',
    'domingo': 'Sun',
  }
  return days[day] || day
}

// PT→EN translation for categorical columns coming from the PRF dataset.
// Kept on the client so the raw data in ClickHouse stays canonical in Portuguese.
const i18n = {
  dia_semana: {
    'domingo': 'Sunday', 'segunda-feira': 'Monday', 'terça-feira': 'Tuesday',
    'quarta-feira': 'Wednesday', 'quinta-feira': 'Thursday', 'sexta-feira': 'Friday', 'sábado': 'Saturday',
  },
  fase_dia: {
    'Amanhecer': 'Dawn', 'Anoitecer': 'Dusk', 'Plena Noite': 'Night', 'Pleno dia': 'Daytime',
  },
  classificacao_acidente: {
    'Com Vítimas Fatais': 'With Fatal Victims',
    'Com Vítimas Feridas': 'With Injuries',
    'Sem Vítimas': 'No Victims',
    'NA': 'N/A',
  },
  tipo_acidente: {
    'Atropelamento de Animal': 'Animal Strike',
    'Atropelamento de Pedestre': 'Pedestrian Strike',
    'Capotamento': 'Rollover',
    'Colisão com objeto': 'Object Collision',
    'Colisão frontal': 'Head-on Collision',
    'Colisão lateral mesmo sentido': 'Same-direction Side Collision',
    'Colisão lateral sentido oposto': 'Opposite-direction Side Collision',
    'Colisão transversal': 'T-bone Collision',
    'Colisão traseira': 'Rear-end Collision',
    'Derramamento de carga': 'Cargo Spill',
    'Engavetamento': 'Pile-up',
    'Eventos atípicos': 'Atypical Events',
    'Incêndio': 'Fire',
    'Queda de ocupante de veículo': 'Occupant Fall',
    'Saída de leito carroçável': 'Roadway Departure',
    'Sinistro pessoal de trânsito': 'Personal Traffic Incident',
    'Tombamento': 'Vehicle Tipping',
  },
  condicao_metereologica: {
    'Chuva': 'Rain', 'Céu Claro': 'Clear Sky', 'Garoa/Chuvisco': 'Drizzle',
    'Ignorado': 'Unknown', 'Nevoeiro/Neblina': 'Fog', 'Nublado': 'Cloudy',
    'Sol': 'Sunny', 'Vento': 'Windy',
  },
  tipo_pista: { 'Dupla': 'Double', 'Múltipla': 'Multiple', 'Simples': 'Single' },
  tracado_via_token: {
    'Aclive': 'Uphill', 'Curva': 'Curve', 'Declive': 'Downhill',
    'Em Obras': 'Under Construction', 'Desvio Temporário': 'Temporary Detour',
    'Interseção de Vias': 'Intersection', 'Ponte': 'Bridge', 'Reta': 'Straight',
    'Retorno Regulamentado': 'Regulated Return', 'Rotatória': 'Roundabout',
    'Túnel': 'Tunnel', 'Viaduto': 'Overpass',
  },
  causa_acidente: {
    'Ausência de reação do condutor': 'Driver failed to react',
    'Reação tardia ou ineficiente do condutor': 'Late or ineffective driver reaction',
    'Acessar a via sem observar a presença dos outros veículos': 'Entering road without checking for other vehicles',
    'Velocidade Incompatível': 'Incompatible speed',
    'Condutor deixou de manter distância do veículo da frente': 'Failed to keep safe distance',
    'Manobra de mudança de faixa': 'Lane change maneuver',
    'Ingestão de álcool pelo condutor': 'Driver alcohol consumption',
    'Demais falhas mecânicas ou elétricas': 'Other mechanical or electrical failures',
    'Transitar na contramão': 'Driving against traffic',
    'Condutor Dormindo': 'Driver asleep',
    'Ultrapassagem Indevida': 'Improper overtaking',
    'Chuva': 'Rain',
    'Avarias e/ou desgaste excessivo no pneu': 'Tire damage or excessive wear',
    'Animais na Pista': 'Animals on road',
    'Trafegar com motocicleta (ou similar) entre as faixas': 'Motorcycle lane splitting',
    'Desrespeitar a preferência no cruzamento': 'Failure to yield at intersection',
    'Acumulo de água sobre o pavimento': 'Water on pavement',
    'Conversão proibida': 'Prohibited turn',
    'Acesso irregular': 'Irregular road access',
    'Pista Escorregadia': 'Slippery road',
    'Entrada inopinada do pedestre': 'Unexpected pedestrian entry',
    'Pedestre andava na pista': 'Pedestrian walking on road',
    'Mal súbito do condutor': 'Driver sudden illness',
    'Transitar no Acostamento': 'Driving on shoulder',
    'Objeto estático sobre o leito carroçável': 'Static object on road',
    'Pista esburacada': 'Potholed road',
    'Pedestre cruzava a pista fora da faixa': 'Pedestrian crossing outside crosswalk',
    'Retorno proibido': 'Prohibited U-turn',
    'Frear bruscamente': 'Sudden braking',
    'Condutor desrespeitou a iluminação vermelha do semáforo': 'Driver ran red light',
    'Demais falhas na via': 'Other road failures',
    'Acumulo de areia ou detritos sobre o pavimento': 'Sand or debris on pavement',
    'Problema com o freio': 'Brake problem',
    'Acostamento em desnível': 'Uneven shoulder',
    'Condutor usando celular': 'Driver using mobile phone',
    'Carga excessiva e/ou mal acondicionada': 'Excessive or poorly loaded cargo',
    'Afundamento ou ondulação no pavimento': 'Pavement deformation',
    'Acumulo de óleo sobre o pavimento': 'Oil on pavement',
    'Ausência de sinalização': 'Lack of signage',
    'Curva acentuada': 'Sharp curve',
    'Suicídio (presumido)': 'Suicide (presumed)',
    'Estacionar ou parar em local proibido': 'Parking/stopping in prohibited area',
    'Deficiência do Sistema de Iluminação/Sinalização': 'Lighting/signage deficiency',
    'Iluminação deficiente': 'Poor lighting',
    'Transtornos Mentais (exceto suicidio)': 'Mental disorder (non-suicide)',
    'Pedestre - Ingestão de álcool/ substâncias psicoativas': 'Pedestrian under influence',
    'Demais Fenômenos da natureza': 'Other natural phenomena',
    'Ingestão de substâncias psicoativas pelo condutor': 'Driver under psychoactive substances',
    'Problema na suspensão': 'Suspension problem',
    'Área urbana sem a presença de local apropriado para a travessia de pedestres': 'No proper pedestrian crossing',
    'Falta de acostamento': 'No road shoulder',
    'Falta de elemento de contenção que evite a saída do leito carroçável': 'No containment barrier',
    'Sinalização mal posicionada': 'Poorly positioned signage',
    'Desvio temporário': 'Temporary detour',
    'Declive acentuado': 'Steep downhill',
    'Faixas de trânsito com largura insuficiente': 'Insufficient lane width',
    'Restrição de visibilidade em curvas verticais': 'Vertical curve visibility issue',
    'Redutor de velocidade em desacordo': 'Non-compliant speed bump',
    'Participar de racha': 'Street racing',
    'Transitar na calçada': 'Driving on sidewalk',
    'Fumaça': 'Smoke',
    'Deixar de acionar o farol da motocicleta (ou similar)': 'Motorcycle headlight off',
    'Restrição de visibilidade em curvas horizontais': 'Horizontal curve visibility issue',
    'Modificação proibida': 'Prohibited vehicle modification',
    'Sinalização encoberta': 'Obscured signage',
    'Neblina': 'Fog',
  },
}

function tr(field, value) {
  if (!value) return value
  if (field === 'tracado_via') {
    return String(value).split(';')
      .map(t => i18n.tracado_via_token[t.trim()] || t.trim())
      .join(' + ')
  }
  return (i18n[field] && i18n[field][value]) || value
}

function trDow(value) {
  return i18n.dia_semana[value] || value
}

onMounted(fetchAll)

onBeforeUnmount(() => {
  if (map) {
    map.remove()
    map = null
  }
  if (highlightMarker) {
    highlightMarker.remove()
    highlightMarker = null
  }
})
</script>

<style scoped>
.drawer-enter-active,
.drawer-leave-active {
  transition: opacity 0.2s ease;
}
.drawer-enter-active aside,
.drawer-leave-active aside {
  transition: transform 0.25s cubic-bezier(0.2, 0.9, 0.3, 1);
}
.drawer-enter-from,
.drawer-leave-to {
  opacity: 0;
}
.drawer-enter-from aside,
.drawer-leave-to aside {
  transform: translateX(100%);
}
</style>
