import axios from 'axios'

// API URL configurada via VITE_API_URL environment variable
// Force rebuild: 2025-11-23
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Interceptor para adicionar token JWT em todas as requisições
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Interceptor para tratar erros de autenticação
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Token inválido ou expirado - redirecionar para login
      localStorage.removeItem('auth_token')
      localStorage.removeItem('user_info')
      if (window.location.pathname !== '/login') {
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)

// Profile API
export const profileApi = {
  get: () => api.get('/api/profile/'),
  create: (data) => api.post('/api/profile/', data),
  update: (data) => api.put('/api/profile/', data)
}

// Projects API
export const projectsApi = {
  getAll: () => api.get('/api/projects/'),
  getById: (id) => api.get(`/api/projects/${id}`),
  create: (data) => api.post('/api/projects/', data),
  update: (id, data) => api.put(`/api/projects/${id}`, data),
  delete: (id) => api.delete(`/api/projects/${id}`)
}

// Experiences API
export const experiencesApi = {
  getAll: () => api.get('/api/experiences/'),
  getById: (id) => api.get(`/api/experiences/${id}`),
  create: (data) => api.post('/api/experiences/', data),
  update: (id, data) => api.put(`/api/experiences/${id}`, data),
  delete: (id) => api.delete(`/api/experiences/${id}`)
}

// Auth API
export const authApi = {
  getGoogleLoginUrl: () => {
    return `${API_URL}/api/auth/google/login`
  },
  verifyToken: (token) => api.post('/api/auth/verify', { token }),
  logout: () => {
    localStorage.removeItem('auth_token')
    localStorage.removeItem('user_info')
  }
}

export default api
