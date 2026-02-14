import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import ProjectDetail from '../views/ProjectDetail.vue'
import LastfmInsightsProject from '../views/LastfmInsightsProject.vue'
import LangfuseDashboard from '../views/LangfuseDashboard.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/projects/pokedex',
    name: 'PokedexProject',
    component: ProjectDetail
  },
  {
    path: '/projects/lastfm-insights',
    name: 'LastfmInsightsProject',
    component: LastfmInsightsProject
  },
  {
    path: '/projects/ai-ops',
    name: 'LangfuseDashboard',
    component: LangfuseDashboard
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to) {
    if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth',
      }
    }
    return { top: 0 }
  }
})

export default router
