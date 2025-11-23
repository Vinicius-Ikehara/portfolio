<template>
  <div class="min-h-screen">
    <Navbar :profile="profile" />

    <!-- Hero Section -->
    <section id="about" class="bg-gradient-to-br from-primary-600 to-primary-800 text-white py-20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex flex-col md:flex-row items-center gap-12">
          <div v-if="profile.avatar_url" class="flex-shrink-0">
            <img :src="profile.avatar_url" alt="Avatar" class="w-48 h-48 rounded-full border-4 border-white shadow-xl">
          </div>
          <div class="flex-1 text-center md:text-left">
            <h1 class="text-5xl font-bold mb-4">{{ profile.name }}</h1>
            <p class="text-2xl mb-4 text-primary-100">{{ profile.title }}</p>
            <p class="text-lg mb-6 text-white/90">{{ profile.bio }}</p>

            <div class="flex flex-wrap gap-2 justify-center md:justify-start mb-6">
              <span
                v-for="skill in profile.skills"
                :key="skill"
                class="px-4 py-2 bg-white/20 backdrop-blur-sm rounded-full text-sm font-medium"
              >
                {{ skill }}
              </span>
            </div>

            <div class="flex gap-4 justify-center md:justify-start">
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
        <div class="space-y-6">
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
    <section id="contact" class="py-20 bg-gray-900 text-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 class="text-4xl font-bold mb-8">Entre em Contato</h2>
        <div class="space-y-4">
          <p class="text-xl">
            <span class="text-gray-400">Email:</span> {{ profile.email }}
          </p>
          <p v-if="profile.phone" class="text-xl">
            <span class="text-gray-400">Telefone:</span> {{ profile.phone }}
          </p>
          <p class="text-xl">
            <span class="text-gray-400">Localização:</span> {{ profile.location }}
          </p>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-gray-950 text-gray-400 py-8 text-center">
      <p>&copy; 2024 {{ profile.name }}. Todos os direitos reservados.</p>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Navbar from '../components/Navbar.vue'
import ProjectCard from '../components/ProjectCard.vue'
import ExperienceCard from '../components/ExperienceCard.vue'

// Dados do perfil hardcoded
const profile = ref({
  name: 'Vinícius Ikehara',
  title: 'Desenvolvedor IA & Full Stack',
  bio: 'Desenvolvedor apaixonado por inteligência artificial e tecnologias web modernas. Especializado em criar soluções inovadoras que combinam IA com desenvolvimento web.',
  email: 'vhikehara@gmail.com',
  phone: '',
  location: 'Brasil',
  avatar_url: 'https://avatars.githubusercontent.com/u/seu-usuario',
  skills: [
    'Python',
    'JavaScript',
    'Vue.js',
    'FastAPI',
    'Machine Learning',
    'TensorFlow',
    'PyTorch',
    'Docker',
    'PostgreSQL'
  ],
  social_links: {
    GitHub: 'https://github.com/Vinicius-Ikehara',
    LinkedIn: 'https://linkedin.com/in/seu-perfil',
    Twitter: 'https://twitter.com/seu-usuario'
  }
})

// Experiências hardcoded
const experiences = ref([
  {
    id: 1,
    company: 'Empresa de Tecnologia',
    position: 'Desenvolvedor Full Stack',
    start_date: '2022-01',
    end_date: null,
    description: 'Desenvolvimento de aplicações web usando Vue.js, FastAPI e PostgreSQL. Implementação de soluções de IA para automação de processos.',
    technologies: ['Vue.js', 'FastAPI', 'PostgreSQL', 'Docker'],
    order: 1
  },
  {
    id: 2,
    company: 'Startup de IA',
    position: 'Desenvolvedor IA',
    start_date: '2020-06',
    end_date: '2021-12',
    description: 'Desenvolvimento de modelos de machine learning e deep learning para processamento de linguagem natural e visão computacional.',
    technologies: ['Python', 'TensorFlow', 'PyTorch', 'Scikit-learn'],
    order: 2
  }
])

// Projetos hardcoded
const projects = ref([
  {
    id: 1,
    title: 'Portfolio Interativo',
    description: 'Portfolio profissional desenvolvido com Vue.js e FastAPI, apresentando projetos e experiências de forma moderna e responsiva.',
    image_url: 'https://via.placeholder.com/400x300',
    github_url: 'https://github.com/Vinicius-Ikehara/portfolio',
    live_url: 'https://seu-portfolio.com',
    technologies: ['Vue.js', 'FastAPI', 'TailwindCSS', 'PostgreSQL'],
    order: 1
  },
  {
    id: 2,
    title: 'Assistente IA com LangChain',
    description: 'Sistema de assistente virtual utilizando LangChain e OpenAI para processamento de linguagem natural e automação de tarefas.',
    image_url: 'https://via.placeholder.com/400x300',
    github_url: 'https://github.com/seu-usuario/projeto',
    live_url: '',
    technologies: ['Python', 'LangChain', 'OpenAI', 'FastAPI'],
    order: 2
  },
  {
    id: 3,
    title: 'Dashboard Analytics',
    description: 'Dashboard interativo para análise de dados com visualizações dinâmicas e relatórios personalizados.',
    image_url: 'https://via.placeholder.com/400x300',
    github_url: 'https://github.com/seu-usuario/dashboard',
    live_url: 'https://seu-dashboard.com',
    technologies: ['Vue.js', 'Chart.js', 'Python', 'Pandas'],
    order: 3
  }
])
</script>
