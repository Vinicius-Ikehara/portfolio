<template>
  <div class="min-h-screen" style="background-color: #111827;">
    <Navbar :profile="profile" />

    <!-- Hero Section -->
    <section id="about" class="relative overflow-hidden text-white py-16" style="background: linear-gradient(135deg, #1f2937 0%, #111827 50%, #0c4a6e 100%);">
      <div class="absolute inset-0 opacity-10">
        <div class="absolute inset-0" style="background-image: radial-gradient(circle at 2px 2px, rgba(255,255,255,0.15) 1px, transparent 0); background-size: 40px 40px;"></div>
      </div>

      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div class="flex flex-col md:flex-row items-center gap-10">
          <div class="flex-shrink-0">
            <div class="w-72 h-72 md:w-80 md:h-80 rounded-full shadow-2xl overflow-hidden">
              <img
                :src="profile.avatar_url"
                :alt="profile.name"
                class="w-full h-full rounded-full object-cover"
              />
            </div>
          </div>
          <div class="flex-1 text-center md:text-left">
            <h1 class="text-4xl md:text-5xl font-bold mb-3 leading-tight" style="color: #ffffff;">
              {{ profile.name }}
            </h1>
            <p class="text-xl md:text-2xl mb-4 font-light" style="color: #7dd3fc;">
              {{ profile.title }}
            </p>
            <p class="text-base mb-5 leading-relaxed max-w-2xl" style="color: rgba(255,255,255,0.9);">
              {{ profile.bio }}
            </p>

            <div class="flex flex-wrap gap-2 justify-center md:justify-start mb-5">
              <span
                v-for="skill in profile.skills"
                :key="skill"
                class="px-3 py-1.5 rounded-lg text-sm font-medium hover:bg-white/20 transition-all"
                style="background-color: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); color: #ffffff;"
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
                class="flex items-center gap-2 px-4 py-2 rounded-lg font-semibold transition-all hover:scale-105 text-sm"
                style="background-color: rgba(255,255,255,0.1); border: 2px solid rgba(255,255,255,0.3); color: #ffffff;"
              >
                <i :class="getSocialIcon(platform)" class="text-base"></i>
                <span>{{ platform }}</span>
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Experience Section -->
    <section id="experience" class="py-24" style="background-color: #0f172a;">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-4xl md:text-5xl font-bold mb-4" style="color: #ffffff;">
            Professional Experience
          </h2>
          <div class="w-24 h-1 mx-auto" style="background-color: #38bdf8;"></div>
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
    <section id="projects" class="py-24" style="background-color: #111827;">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-4xl md:text-5xl font-bold mb-4" style="color: #ffffff;">
            Featured Projects
          </h2>
          <div class="w-24 h-1 mx-auto mb-6" style="background-color: #38bdf8;"></div>
          <p class="text-xl max-w-2xl mx-auto" style="color: #9ca3af;">
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
    <section id="contact" class="py-24 text-white" style="background: linear-gradient(135deg, #1f2937 0%, #111827 50%, #0c4a6e 100%);">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <div class="mb-12">
          <h2 class="text-4xl md:text-5xl font-bold mb-6" style="color: #ffffff;">Let's Work Together</h2>
          <div class="w-24 h-1 mx-auto mb-6" style="background-color: #38bdf8;"></div>
          <p class="text-xl" style="color: #d1d5db;">
            Always open to new opportunities and collaborations
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
          <div class="rounded-xl p-8 transition-all hover:scale-105" style="background-color: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2);">
            <i class="pi pi-envelope text-4xl mb-4 block" style="color: #38bdf8;"></i>
            <div class="text-sm mb-2 uppercase tracking-wide" style="color: #9ca3af;">Email</div>
            <div class="text-lg font-semibold" style="color: #ffffff;">{{ profile.email }}</div>
          </div>

          <div class="rounded-xl p-8 transition-all hover:scale-105" style="background-color: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2);">
            <i class="pi pi-phone text-4xl mb-4 block" style="color: #38bdf8;"></i>
            <div class="text-sm mb-2 uppercase tracking-wide" style="color: #9ca3af;">Phone</div>
            <div class="text-lg font-semibold" style="color: #ffffff;">{{ profile.phone }}</div>
          </div>

          <div class="rounded-xl p-8 transition-all hover:scale-105" style="background-color: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2);">
            <i class="pi pi-map-marker text-4xl mb-4 block" style="color: #38bdf8;"></i>
            <div class="text-sm mb-2 uppercase tracking-wide" style="color: #9ca3af;">Location</div>
            <div class="text-lg font-semibold" style="color: #ffffff;">{{ profile.location }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="py-8" style="background-color: #030712; color: #9ca3af; border-top: 1px solid #1f2937;">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex flex-col md:flex-row justify-between items-center gap-4">
          <p>&copy; 2024 {{ profile.name }}. All rights reserved.</p>
          <button
            @click="scrollToTop"
            class="flex items-center gap-2 px-4 py-2 rounded-lg transition-colors font-medium"
            style="background-color: #0284c7; color: #ffffff;"
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
