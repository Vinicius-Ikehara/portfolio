import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Admin from '../views/Admin.vue'
import Login from '../views/Login.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/admin',
    name: 'Admin',
    component: Admin,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard para proteger rotas que requerem autenticação
router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // Verifica se existe token no localStorage
    const token = localStorage.getItem('auth_token')

    if (!token) {
      // Não tem token, redireciona para login
      next({ name: 'Login' })
    } else {
      // Tem token, permite acesso
      next()
    }
  } else {
    // Rota não requer autenticação
    next()
  }
})

export default router
