<template>
  <div class="min-h-screen">
    <Navbar :profile="profile" />

    <!-- Hero Section -->
    <section id="about" class="bg-gradient-to-br from-primary-600 to-primary-800 text-white py-20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex flex-col md:flex-row items-center gap-12">
          <div v-if="profile?.avatar_url" class="flex-shrink-0">
            <img :src="profile.avatar_url" alt="Avatar" class="w-48 h-48 rounded-full border-4 border-white shadow-xl">
          </div>
          <div class="flex-1 text-center md:text-left">
            <h1 class="text-5xl font-bold mb-4">{{ profile?.name || 'Seu Nome' }}</h1>
            <p class="text-2xl mb-4 text-primary-100">{{ profile?.title || 'Desenvolvedor IA' }}</p>
            <p class="text-lg mb-6 text-white/90">{{ profile?.bio || 'Carregando...' }}</p>

            <div v-if="profile?.skills" class="flex flex-wrap gap-2 justify-center md:justify-start mb-6">
              <span
                v-for="skill in profile.skills"
                :key="skill"
                class="px-4 py-2 bg-white/20 backdrop-blur-sm rounded-full text-sm font-medium"
              >
                {{ skill }}
              </span>
            </div>

            <div v-if="profile?.social_links" class="flex gap-4 justify-center md:justify-start">
              <a
                v-for="(url, platform) in profile.social_links"
                :key="platform"
                :href="url"
                target="_blank"
                class="px-6 py-3 bg-white text-primary-600 rounded-lg font-medium hover:bg-gray-100 transition"
              >
                {{ platform }}
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Experience Section -->
    <section id="experience" class="py-20 bg-gray-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 class="text-4xl font-bold text-center mb-12 text-gray-900">Experiência Profissional</h2>
        <div v-if="loading" class="text-center text-gray-600">Carregando...</div>
        <div v-else-if="experiences.length === 0" class="text-center text-gray-600">
          Nenhuma experiência cadastrada ainda.
        </div>
        <div v-else class="space-y-6">
          <ExperienceCard
            v-for="exp in experiences"
            :key="exp.id"
            :experience="exp"
          />
        </div>
      </div>
    </section>

    <!-- Projects Section -->
    <section id="projects" class="py-20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 class="text-4xl font-bold text-center mb-12 text-gray-900">Projetos</h2>
        <div v-if="loading" class="text-center text-gray-600">Carregando...</div>
        <div v-else-if="projects.length === 0" class="text-center text-gray-600">
          Nenhum projeto cadastrado ainda.
        </div>
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <ProjectCard
            v-for="project in projects"
            :key="project.id"
            :project="project"
          />
        </div>
      </div>
    </section>

    <!-- Contact Section -->
    <section id="contact" class="py-20 bg-gray-900 text-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 class="text-4xl font-bold mb-8">Entre em Contato</h2>
        <div class="space-y-4">
          <p v-if="profile?.email" class="text-xl">
            <span class="text-gray-400">Email:</span> {{ profile.email }}
          </p>
          <p v-if="profile?.phone" class="text-xl">
            <span class="text-gray-400">Telefone:</span> {{ profile.phone }}
          </p>
          <p v-if="profile?.location" class="text-xl">
            <span class="text-gray-400">Localização:</span> {{ profile.location }}
          </p>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-gray-950 text-gray-400 py-8 text-center">
      <p>&copy; 2024 {{ profile?.name }}. Todos os direitos reservados.</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Navbar from '../components/Navbar.vue'
import ProjectCard from '../components/ProjectCard.vue'
import ExperienceCard from '../components/ExperienceCard.vue'
import { profileApi, projectsApi, experiencesApi } from '../services/api'

const profile = ref(null)
const projects = ref([])
const experiences = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    // Carregar dados do perfil
    try {
      const profileRes = await profileApi.get()
      profile.value = profileRes.data
    } catch (error) {
      console.log('Perfil ainda não configurado')
    }

    // Carregar projetos
    const projectsRes = await projectsApi.getAll()
    projects.value = projectsRes.data

    // Carregar experiências
    const experiencesRes = await experiencesApi.getAll()
    experiences.value = experiencesRes.data

    loading.value = false
  } catch (error) {
    console.error('Erro ao carregar dados:', error)
    loading.value = false
  }
})
</script>
