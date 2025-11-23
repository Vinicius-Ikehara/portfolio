<template>
  <div class="min-h-screen bg-surface-50">
    <Navbar :profile="profile" />

    <!-- Hero Section -->
    <section id="about" class="relative overflow-hidden bg-gradient-to-br from-primary-700 via-primary-800 to-primary-900 text-white py-32">
      <div class="absolute inset-0 opacity-10">
        <div class="absolute inset-0" style="background-image: radial-gradient(circle at 2px 2px, rgba(255,255,255,0.15) 1px, transparent 0); background-size: 40px 40px;"></div>
      </div>

      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div class="flex flex-col md:flex-row items-center gap-16">
          <div class="flex-shrink-0">
            <div class="w-64 h-64 rounded-full bg-gradient-to-br from-primary-400 to-primary-600 p-1 shadow-2xl">
              <img
                :src="profile.avatar_url"
                :alt="profile.name"
                class="w-full h-full rounded-full object-cover border-4 border-white/20"
              />
            </div>
          </div>
          <div class="flex-1 text-center md:text-left">
            <div class="inline-block px-4 py-2 bg-green-500/20 border border-green-400/30 rounded-full mb-6">
              <span class="text-green-300 font-semibold flex items-center gap-2">
                <span class="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
                Available for Projects
              </span>
            </div>
            <h1 class="text-5xl md:text-6xl font-bold mb-6 leading-tight">
              {{ profile.name }}
            </h1>
            <p class="text-2xl md:text-3xl mb-6 text-primary-200 font-light">
              {{ profile.title }}
            </p>
            <p class="text-lg mb-8 text-white/90 leading-relaxed max-w-2xl">
              {{ profile.bio }}
            </p>

            <div class="flex flex-wrap gap-3 justify-center md:justify-start mb-8">
              <span
                v-for="skill in profile.skills"
                :key="skill"
                class="px-4 py-2 bg-white/10 backdrop-blur-sm border border-white/20 rounded-lg text-white font-medium hover:bg-white/20 transition-all"
              >
                {{ skill }}
              </span>
            </div>

            <div class="flex gap-3 justify-center md:justify-start flex-wrap">
              <a
                v-for="(url, platform) in profile.social_links"
                :key="platform"
                :href="url"
                target="_blank"
                rel="noopener noreferrer"
                class="flex items-center gap-2 px-5 py-2.5 bg-white/10 backdrop-blur-sm border-2 border-white/30 rounded-lg text-white hover:bg-white/20 font-semibold transition-all hover:scale-105"
              >
                <i :class="getSocialIcon(platform)" class="text-lg"></i>
                <span>{{ platform }}</span>
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Experience Section -->
    <section id="experience" class="py-24 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-4xl md:text-5xl font-bold mb-4 text-surface-900">
            Professional Experience
          </h2>
          <div class="w-24 h-1 bg-primary-600 mx-auto mb-6"></div>
          <p class="text-xl text-surface-600 max-w-2xl mx-auto">
            My professional journey and contributions across different organizations
          </p>
        </div>

        <div class="space-y-8">
          <ExperienceCard
            v-for="exp in experiences"
            :key="exp.id"
            :experience="exp"
          />
        </div>
      </div>
    </section>

    <!-- Projects Section -->
    <section id="projects" class="py-24 bg-surface-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-4xl md:text-5xl font-bold mb-4 text-surface-900">
            Featured Projects
          </h2>
          <div class="w-24 h-1 bg-primary-600 mx-auto mb-6"></div>
          <p class="text-xl text-surface-600 max-w-2xl mx-auto">
            Showcasing projects that demonstrate my technical expertise and problem-solving abilities
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <ProjectCard
            v-for="project in projects"
            :key="project.id"
            :project="project"
          />
        </div>
      </div>
    </section>

    <!-- Contact Section -->
    <section id="contact" class="py-24 bg-gradient-to-br from-surface-900 via-surface-800 to-primary-950 text-white">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <div class="mb-12">
          <h2 class="text-4xl md:text-5xl font-bold mb-6">Let's Work Together</h2>
          <div class="w-24 h-1 bg-primary-400 mx-auto mb-6"></div>
          <p class="text-xl text-surface-300">
            Always open to new opportunities and collaborations
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
          <div class="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-8 hover:bg-white/10 transition-all hover:scale-105">
            <i class="pi pi-envelope text-4xl text-primary-400 mb-4"></i>
            <div class="text-sm text-surface-400 mb-2 uppercase tracking-wide">Email</div>
            <div class="text-lg font-semibold">{{ profile.email }}</div>
          </div>

          <div class="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-8 hover:bg-white/10 transition-all hover:scale-105">
            <i class="pi pi-phone text-4xl text-primary-400 mb-4"></i>
            <div class="text-sm text-surface-400 mb-2 uppercase tracking-wide">Phone</div>
            <div class="text-lg font-semibold">{{ profile.phone }}</div>
          </div>

          <div class="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-8 hover:bg-white/10 transition-all hover:scale-105">
            <i class="pi pi-map-marker text-4xl text-primary-400 mb-4"></i>
            <div class="text-sm text-surface-400 mb-2 uppercase tracking-wide">Location</div>
            <div class="text-lg font-semibold">{{ profile.location }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-surface-950 text-surface-400 py-8 border-t border-surface-800">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex flex-col md:flex-row justify-between items-center gap-4">
          <p>&copy; 2024 {{ profile.name }}. All rights reserved.</p>
          <button
            @click="scrollToTop"
            class="flex items-center gap-2 px-4 py-2 bg-primary-600 hover:bg-primary-700 rounded-lg transition-colors text-white font-medium"
          >
            <i class="pi pi-arrow-up"></i>
            Back to Top
          </button>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import Navbar from '../components/Navbar.vue'
import ProjectCard from '../components/ProjectCard.vue'
import ExperienceCard from '../components/ExperienceCard.vue'
import { profile, projects, experiences } from '../data/portfolio.js'

const getSocialIcon = (platform) => {
  const icons = {
    'GitHub': 'pi pi-github',
    'LinkedIn': 'pi pi-linkedin',
    'Twitter': 'pi pi-twitter',
    'Email': 'pi pi-envelope',
    'Website': 'pi pi-globe'
  }
  return icons[platform] || 'pi pi-link'
}

const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
</script>

<style scoped>
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>
