<template>
  <div class="min-h-screen" style="background-color: var(--bg-page);">
    <Navbar :profile="profile" />

    <div class="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8 pt-8 pb-32">
      <div class="grid grid-cols-1 lg:grid-cols-[300px_1fr] gap-8">

        <!-- Poste: timeline de experiência, ocupa a vertical -->
        <aside id="experience" class="lg:sticky lg:top-24 lg:self-start">
          <h2 class="text-lg font-bold mb-4 uppercase tracking-wide" style="color: var(--text-heading);">
            Professional Experience
          </h2>

          <div class="flex flex-col">
            <div
              v-for="(exp, idx) in experiences"
              :key="exp.id"
              class="relative pl-8"
              :style="idx < experiences.length - 1 ? 'border-left: 1px solid var(--border-color); padding-bottom: 1rem;' : ''"
            >
              <span
                class="absolute -left-[5px] top-1.5 w-[11px] h-[11px] rounded-full"
                :style="exp.current ? 'background-color:#c8703f;' : 'background-color:var(--border-color); border:2px solid var(--text-faint);'"
              ></span>

              <button
                class="exp-item-btn w-full flex items-center justify-between gap-2 text-left rounded-lg px-3 py-2 -ml-3"
                style="background-color: transparent;"
                @click="toggleExp(exp.id)"
              >
                <span class="flex flex-col">
                  <span class="flex items-center gap-2 flex-wrap">
                    <span class="font-semibold text-sm" style="color: var(--text-heading);">{{ exp.position }}</span>
                    <span
                      v-if="exp.current"
                      class="px-2 py-0.5 rounded-full text-[10px] font-bold uppercase"
                      style="background-color: rgba(255,255,255,0.9); color: #874726;"
                    >Current</span>
                  </span>
                  <span class="text-sm" style="color: var(--text-muted);">{{ exp.company }}</span>
                  <span class="text-xs mt-0.5" style="color: var(--text-faint);">
                    {{ formatDate(exp.start_date) }} – {{ exp.current ? 'Present' : formatDate(exp.end_date) }}
                  </span>
                </span>
                <i
                  class="pi text-xs shrink-0"
                  :class="expanded.has(exp.id) ? 'pi-chevron-up' : 'pi-chevron-down'"
                  style="color: var(--text-faint);"
                ></i>
              </button>

              <div v-show="expanded.has(exp.id)" class="mt-2 mb-2 pr-2">
                <p class="text-sm leading-relaxed mb-3" style="color: var(--text-muted);">{{ exp.description }}</p>
                <div class="flex flex-wrap gap-1.5">
                  <span
                    v-for="tech in exp.technologies"
                    :key="tech"
                    class="px-2 py-1 rounded text-xs font-medium"
                    style="background-color: rgba(200,112,63,0.1); color: var(--accent-text); border: 1px solid rgba(200,112,63,0.25);"
                  >
                    {{ tech }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </aside>

        <!-- Main: resumo + catálogo de projetos -->
        <main class="flex flex-col gap-10">

          <!-- Resumo -->
          <section id="about" class="rounded-xl p-6 flex flex-col sm:flex-row items-center sm:items-start gap-6" style="background-color: var(--bg-card); border: 1px solid var(--border-color);">
            <div class="w-28 h-28 rounded-full overflow-hidden shrink-0" style="border: 2px solid var(--border-color);">
              <img :src="profile.avatar_url" :alt="profile.name" class="w-full h-full object-cover" />
            </div>
            <div class="text-center sm:text-left">
              <h1 class="text-2xl font-bold mb-1" style="color: var(--text-heading); font-family: ui-monospace, 'SF Mono', 'Cascadia Code', Consolas, monospace;">
                {{ profile.name }}
              </h1>
              <p class="text-sm font-medium mb-3" style="color: #c8703f;">{{ profile.title }}</p>
              <p class="text-sm leading-relaxed mb-4" style="color: var(--text-muted);">{{ profile.bio }}</p>

              <div class="flex flex-wrap gap-1.5 justify-center sm:justify-start">
                <span
                  v-for="skill in profile.skills"
                  :key="skill"
                  class="px-2.5 py-1 rounded-md text-xs font-medium"
                  style="background-color: rgba(200,112,63,0.12); color: var(--accent-text); border: 1px solid rgba(200,112,63,0.3);"
                >
                  {{ skill }}
                </span>
              </div>
            </div>
          </section>

          <!-- Projects catalog -->
          <section id="projects">
            <h2 class="text-lg font-bold mb-4 uppercase tracking-wide" style="color: var(--text-heading);">
              Featured Projects
            </h2>

            <ProjectCarousel :projects="projects" @open="activeProject = $event" />
          </section>

        </main>
      </div>
    </div>

    <!-- Contato: fixo no rodapé da página -->
    <section id="contact" class="fixed bottom-0 left-0 w-full z-40 py-3" style="background: linear-gradient(135deg, #452414 0%, #2e1810 100%); border-top: 1px solid #66351d;">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-wrap items-center justify-center gap-x-6 gap-y-1.5 text-sm">
        <span class="flex items-center gap-2" style="color: #eab98f;">
          <i class="pi pi-envelope" style="color: #dd9660;"></i>{{ profile.email }}
        </span>
        <span class="hidden sm:inline" style="color: #66351d;">/</span>
        <span class="flex items-center gap-2" style="color: #eab98f;">
          <i class="pi pi-phone" style="color: #dd9660;"></i>{{ profile.phone }}
        </span>
        <span class="hidden sm:inline" style="color: #66351d;">/</span>
        <span class="flex items-center gap-2" style="color: #eab98f;">
          <i class="pi pi-map-marker" style="color: #dd9660;"></i>{{ profile.location }}
        </span>
        <template v-for="(url, platform) in profile.social_links" :key="platform">
          <span class="hidden sm:inline" style="color: #66351d;">/</span>
          <a
            :href="url"
            target="_blank"
            rel="noopener noreferrer"
            class="flex items-center gap-2 font-medium transition-colors hover:opacity-75"
            style="color: #ffffff;"
          >
            <i :class="getSocialIcon(platform)"></i>{{ platform }}
          </a>
        </template>
      </div>
    </section>

    <!-- Project detail modal -->
    <div
      v-if="activeProject"
      class="fixed inset-0 z-[70] flex items-center justify-center p-4"
      style="background-color: rgba(10,9,8,0.72);"
      role="dialog"
      aria-modal="true"
      @click.self="activeProject = null"
      @keydown.esc="activeProject = null"
    >
      <div class="w-full max-w-xl rounded-xl overflow-hidden" style="background-color: var(--bg-card); border: 1px solid var(--border-color);">
        <div class="relative">
          <ProjectCover :project="activeProject" size="md" />
          <button
            class="absolute top-3 right-3 w-8 h-8 rounded-full flex items-center justify-center"
            style="background-color: rgba(0,0,0,0.35); color: #ffffff;"
            @click="activeProject = null"
          >
            <i class="pi pi-times"></i>
          </button>
        </div>
        <div class="p-6">
          <h3 class="text-xl font-bold mb-2" style="color: var(--text-heading);">{{ activeProject.title }}</h3>
          <p class="text-sm leading-relaxed mb-4" style="color: var(--text-muted);">{{ activeProject.description }}</p>
          <div class="flex flex-wrap gap-1.5 mb-5">
            <span
              v-for="tech in activeProject.technologies"
              :key="tech"
              class="px-2 py-1 rounded text-xs font-medium"
              style="background-color: rgba(200,112,63,0.15); color: var(--accent-text); border: 1px solid rgba(200,112,63,0.3);"
            >
              {{ tech }}
            </span>
          </div>
          <div class="flex gap-3 flex-wrap">
            <button
              v-if="activeProject.project_url === 'open-chat'"
              @click="openChat"
              class="flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors hover:opacity-90"
              style="background-color: #c8703f; color: #1c1a17;"
            >
              <i class="pi pi-comments"></i>
              Try it Now
            </button>
            <router-link
              v-else-if="activeProject.project_url && activeProject.project_url.startsWith('/')"
              :to="activeProject.project_url"
              class="flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors hover:opacity-90"
              style="background-color: #c8703f; color: #1c1a17;"
            >
              <i class="pi pi-play"></i>
              Try it Now
            </router-link>
            <a
              v-else-if="activeProject.project_url"
              :href="activeProject.project_url"
              target="_blank"
              rel="noopener noreferrer"
              class="flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors"
              style="background-color: #c8703f; color: #1c1a17;"
            >
              <i class="pi pi-external-link"></i>
              View Project
            </a>
            <a
              v-if="activeProject.github_url"
              :href="activeProject.github_url"
              target="_blank"
              rel="noopener noreferrer"
              class="flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors"
              style="background-color: transparent; color: var(--text-muted); border: 1px solid var(--border-color);"
            >
              <i class="pi pi-github"></i>
              GitHub
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import Navbar from '../components/Navbar.vue'
import ProjectCover from '../components/ProjectCover.vue'
import ProjectCarousel from '../components/ProjectCarousel.vue'
import { profile, projects, experiences } from '../data/portfolio.js'

const expanded = ref(new Set([experiences[0]?.id]))
const activeProject = ref(null)

const toggleExp = (id) => {
  const next = new Set(expanded.value)
  next.has(id) ? next.delete(id) : next.add(id)
  expanded.value = next
}

const getSocialIcon = (platform) => {
  const icons = {
    GitHub: 'pi pi-github',
    LinkedIn: 'pi pi-linkedin',
    Twitter: 'pi pi-twitter',
    Email: 'pi pi-envelope',
    Website: 'pi pi-globe'
  }
  return icons[platform] || 'pi pi-link'
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const [year, month] = dateStr.split('-')
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
  return `${months[parseInt(month) - 1]} ${year}`
}

const openChat = () => {
  const dfMessenger = document.querySelector('df-messenger')
  if (!dfMessenger) return
  if (dfMessenger.shadowRoot) {
    const chatButton = dfMessenger.shadowRoot.querySelector('[opened]')
      ? null
      : dfMessenger.shadowRoot.querySelector('button, .chat-bubble-button, df-messenger-chat-bubble')
    if (chatButton) {
      chatButton.click()
      return
    }
  }
  dfMessenger.setAttribute('opened', 'true')
  setTimeout(() => dfMessenger.click(), 100)
}

const onKeydown = (e) => {
  if (e.key === 'Escape') activeProject.value = null
}
onMounted(() => window.addEventListener('keydown', onKeydown))
onUnmounted(() => window.removeEventListener('keydown', onKeydown))
</script>

<style scoped>
.exp-item-btn {
  transition: width 0.2s ease, background-color 0.2s ease, box-shadow 0.2s ease;
}

.exp-item-btn:hover,
.exp-item-btn:focus-visible {
  width: calc(100% + 16px);
  background-color: var(--bg-card);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
  position: relative;
  z-index: 1;
}
</style>
