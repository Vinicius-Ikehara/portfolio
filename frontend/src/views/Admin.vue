<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex justify-between items-center">
        <h1 class="text-3xl font-bold text-gray-900">Painel Administrativo</h1>
        <router-link to="/" class="text-primary-600 hover:text-primary-700">
          ← Voltar ao Portfólio
        </router-link>
      </div>
    </header>

    <!-- Tabs -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="bg-white rounded-lg shadow">
        <div class="border-b border-gray-200">
          <nav class="flex space-x-8 px-6" aria-label="Tabs">
            <button
              @click="activeTab = 'profile'"
              :class="[activeTab === 'profile' ? 'border-primary-500 text-primary-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300', 'whitespace-nowrap py-4 px-1 border-b-2 font-medium']"
            >
              Perfil
            </button>
            <button
              @click="activeTab = 'projects'"
              :class="[activeTab === 'projects' ? 'border-primary-500 text-primary-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300', 'whitespace-nowrap py-4 px-1 border-b-2 font-medium']"
            >
              Projetos
            </button>
            <button
              @click="activeTab = 'experiences'"
              :class="[activeTab === 'experiences' ? 'border-primary-500 text-primary-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300', 'whitespace-nowrap py-4 px-1 border-b-2 font-medium']"
            >
              Experiências
            </button>
          </nav>
        </div>

        <!-- Profile Tab -->
        <div v-if="activeTab === 'profile'" class="p-6">
          <h2 class="text-2xl font-bold mb-6">Configurar Perfil</h2>
          <form @submit.prevent="saveProfile" class="space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Nome</label>
                <input v-model="profileForm.name" type="text" class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Título</label>
                <input v-model="profileForm.title" type="text" class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500">
              </div>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Bio</label>
              <textarea v-model="profileForm.bio" rows="4" class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500"></textarea>
            </div>
            <div class="grid grid-cols-3 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
                <input v-model="profileForm.email" type="email" class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Telefone</label>
                <input v-model="profileForm.phone" type="text" class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Localização</label>
                <input v-model="profileForm.location" type="text" class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500">
              </div>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">URL do Avatar</label>
              <input v-model="profileForm.avatar_url" type="text" class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Skills (separadas por vírgula)</label>
              <input v-model="skillsInput" type="text" class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500" placeholder="Python, TensorFlow, PyTorch, NLP, Computer Vision">
            </div>
            <button type="submit" class="w-full bg-primary-600 text-white py-3 rounded-lg hover:bg-primary-700 transition font-medium">
              Salvar Perfil
            </button>
          </form>
        </div>

        <!-- Projects Tab -->
        <div v-if="activeTab === 'projects'" class="p-6">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-bold">Gerenciar Projetos</h2>
            <button @click="openProjectForm()" class="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700">
              + Novo Projeto
            </button>
          </div>

          <div v-if="showProjectForm" class="mb-8 bg-gray-50 p-6 rounded-lg">
            <h3 class="text-xl font-bold mb-4">{{ editingProject ? 'Editar' : 'Novo' }} Projeto</h3>
            <form @submit.prevent="saveProject" class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Título</label>
                <input v-model="projectForm.title" type="text" required class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Descrição</label>
                <textarea v-model="projectForm.description" rows="3" required class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500"></textarea>
              </div>
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">URL da Imagem</label>
                  <input v-model="projectForm.image_url" type="text" class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500">
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">URL do Projeto</label>
                  <input v-model="projectForm.project_url" type="text" class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500">
                </div>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">URL do GitHub</label>
                <input v-model="projectForm.github_url" type="text" class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Tecnologias (separadas por vírgula)</label>
                <input v-model="techInput" type="text" class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500">
              </div>
              <div class="flex gap-4">
                <button type="submit" class="flex-1 bg-primary-600 text-white py-2 rounded-lg hover:bg-primary-700">
                  Salvar
                </button>
                <button type="button" @click="cancelProjectForm" class="flex-1 bg-gray-300 text-gray-700 py-2 rounded-lg hover:bg-gray-400">
                  Cancelar
                </button>
              </div>
            </form>
          </div>

          <div class="space-y-4">
            <div v-for="project in projects" :key="project.id" class="bg-white border rounded-lg p-4 flex justify-between items-start">
              <div class="flex-1">
                <h3 class="font-bold text-lg">{{ project.title }}</h3>
                <p class="text-gray-600 text-sm mb-2">{{ project.description }}</p>
                <div class="flex flex-wrap gap-2">
                  <span v-for="tech in project.technologies" :key="tech" class="px-2 py-1 bg-primary-100 text-primary-700 rounded text-xs">
                    {{ tech }}
                  </span>
                </div>
              </div>
              <div class="flex gap-2">
                <button @click="openProjectForm(project)" class="text-blue-600 hover:text-blue-800">Editar</button>
                <button @click="deleteProject(project.id)" class="text-red-600 hover:text-red-800">Excluir</button>
              </div>
            </div>
          </div>
        </div>

        <!-- Experiences Tab -->
        <div v-if="activeTab === 'experiences'" class="p-6">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-bold">Gerenciar Experiências</h2>
            <button @click="openExperienceForm()" class="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700">
              + Nova Experiência
            </button>
          </div>

          <div v-if="showExperienceForm" class="mb-8 bg-gray-50 p-6 rounded-lg">
            <h3 class="text-xl font-bold mb-4">{{ editingExperience ? 'Editar' : 'Nova' }} Experiência</h3>
            <form @submit.prevent="saveExperience" class="space-y-4">
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Empresa</label>
                  <input v-model="experienceForm.company" type="text" required class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500">
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Cargo</label>
                  <input v-model="experienceForm.position" type="text" required class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500">
                </div>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Descrição</label>
                <textarea v-model="experienceForm.description" rows="3" required class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500"></textarea>
              </div>
              <div class="grid grid-cols-3 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Data Início</label>
                  <input v-model="experienceForm.start_date" type="month" required class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500">
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Data Fim</label>
                  <input v-model="experienceForm.end_date" type="month" :disabled="experienceForm.current" class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500">
                </div>
                <div class="flex items-end">
                  <label class="flex items-center">
                    <input v-model="experienceForm.current" type="checkbox" class="mr-2">
                    <span class="text-sm font-medium text-gray-700">Atual</span>
                  </label>
                </div>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Tecnologias (separadas por vírgula)</label>
                <input v-model="expTechInput" type="text" class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500">
              </div>
              <div class="flex gap-4">
                <button type="submit" class="flex-1 bg-primary-600 text-white py-2 rounded-lg hover:bg-primary-700">
                  Salvar
                </button>
                <button type="button" @click="cancelExperienceForm" class="flex-1 bg-gray-300 text-gray-700 py-2 rounded-lg hover:bg-gray-400">
                  Cancelar
                </button>
              </div>
            </form>
          </div>

          <div class="space-y-4">
            <div v-for="exp in experiences" :key="exp.id" class="bg-white border rounded-lg p-4 flex justify-between items-start">
              <div class="flex-1">
                <h3 class="font-bold text-lg">{{ exp.position }}</h3>
                <p class="text-primary-600 font-medium">{{ exp.company }}</p>
                <p class="text-gray-600 text-sm mb-2">{{ exp.description }}</p>
                <p class="text-gray-500 text-sm mb-2">{{ exp.start_date }} - {{ exp.current ? 'Atual' : exp.end_date }}</p>
                <div class="flex flex-wrap gap-2">
                  <span v-for="tech in exp.technologies" :key="tech" class="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs">
                    {{ tech }}
                  </span>
                </div>
              </div>
              <div class="flex gap-2">
                <button @click="openExperienceForm(exp)" class="text-blue-600 hover:text-blue-800">Editar</button>
                <button @click="deleteExperience(exp.id)" class="text-red-600 hover:text-red-800">Excluir</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { profileApi, projectsApi, experiencesApi } from '../services/api'

const activeTab = ref('profile')

// Profile
const profileForm = ref({
  name: '',
  title: '',
  bio: '',
  email: '',
  phone: '',
  location: '',
  avatar_url: '',
  social_links: {},
  skills: []
})
const skillsInput = computed({
  get: () => profileForm.value.skills.join(', '),
  set: (val) => {
    profileForm.value.skills = val.split(',').map(s => s.trim()).filter(s => s)
  }
})
const profileExists = ref(false)

// Projects
const projects = ref([])
const showProjectForm = ref(false)
const editingProject = ref(null)
const projectForm = ref({
  title: '',
  description: '',
  technologies: [],
  image_url: '',
  project_url: '',
  github_url: '',
  order: 0
})
const techInput = computed({
  get: () => projectForm.value.technologies.join(', '),
  set: (val) => {
    projectForm.value.technologies = val.split(',').map(s => s.trim()).filter(s => s)
  }
})

// Experiences
const experiences = ref([])
const showExperienceForm = ref(false)
const editingExperience = ref(null)
const experienceForm = ref({
  company: '',
  position: '',
  description: '',
  technologies: [],
  start_date: '',
  end_date: '',
  current: false,
  order: 0
})
const expTechInput = computed({
  get: () => experienceForm.value.technologies.join(', '),
  set: (val) => {
    experienceForm.value.technologies = val.split(',').map(s => s.trim()).filter(s => s)
  }
})

onMounted(async () => {
  await loadProfile()
  await loadProjects()
  await loadExperiences()
})

async function loadProfile() {
  try {
    const res = await profileApi.get()
    profileForm.value = res.data
    profileExists.value = true
  } catch (error) {
    console.log('Perfil não existe ainda')
  }
}

async function saveProfile() {
  try {
    if (profileExists.value) {
      await profileApi.update(profileForm.value)
      alert('Perfil atualizado com sucesso!')
    } else {
      await profileApi.create(profileForm.value)
      profileExists.value = true
      alert('Perfil criado com sucesso!')
    }
  } catch (error) {
    alert('Erro ao salvar perfil: ' + error.message)
  }
}

async function loadProjects() {
  const res = await projectsApi.getAll()
  projects.value = res.data
}

function openProjectForm(project = null) {
  if (project) {
    editingProject.value = project
    projectForm.value = { ...project }
  } else {
    editingProject.value = null
    projectForm.value = { title: '', description: '', technologies: [], image_url: '', project_url: '', github_url: '', order: 0 }
  }
  showProjectForm.value = true
}

function cancelProjectForm() {
  showProjectForm.value = false
  editingProject.value = null
}

async function saveProject() {
  try {
    if (editingProject.value) {
      await projectsApi.update(editingProject.value.id, projectForm.value)
      alert('Projeto atualizado!')
    } else {
      await projectsApi.create(projectForm.value)
      alert('Projeto criado!')
    }
    showProjectForm.value = false
    await loadProjects()
  } catch (error) {
    alert('Erro ao salvar projeto: ' + error.message)
  }
}

async function deleteProject(id) {
  if (confirm('Tem certeza que deseja excluir este projeto?')) {
    await projectsApi.delete(id)
    await loadProjects()
  }
}

async function loadExperiences() {
  const res = await experiencesApi.getAll()
  experiences.value = res.data
}

function openExperienceForm(exp = null) {
  if (exp) {
    editingExperience.value = exp
    experienceForm.value = { ...exp }
  } else {
    editingExperience.value = null
    experienceForm.value = { company: '', position: '', description: '', technologies: [], start_date: '', end_date: '', current: false, order: 0 }
  }
  showExperienceForm.value = true
}

function cancelExperienceForm() {
  showExperienceForm.value = false
  editingExperience.value = null
}

async function saveExperience() {
  try {
    if (editingExperience.value) {
      await experiencesApi.update(editingExperience.value.id, experienceForm.value)
      alert('Experiência atualizada!')
    } else {
      await experiencesApi.create(experienceForm.value)
      alert('Experiência criada!')
    }
    showExperienceForm.value = false
    await loadExperiences()
  } catch (error) {
    alert('Erro ao salvar experiência: ' + error.message)
  }
}

async function deleteExperience(id) {
  if (confirm('Tem certeza que deseja excluir esta experiência?')) {
    await experiencesApi.delete(id)
    await loadExperiences()
  }
}
</script>
