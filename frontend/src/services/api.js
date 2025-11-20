import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Profile API
export const profileApi = {
  get: () => api.get('/api/profile'),
  create: (data) => api.post('/api/profile', data),
  update: (data) => api.put('/api/profile', data)
}

// Projects API
export const projectsApi = {
  getAll: () => api.get('/api/projects'),
  getById: (id) => api.get(`/api/projects/${id}`),
  create: (data) => api.post('/api/projects', data),
  update: (id, data) => api.put(`/api/projects/${id}`, data),
  delete: (id) => api.delete(`/api/projects/${id}`)
}

// Experiences API
export const experiencesApi = {
  getAll: () => api.get('/api/experiences'),
  getById: (id) => api.get(`/api/experiences/${id}`),
  create: (data) => api.post('/api/experiences', data),
  update: (id, data) => api.put(`/api/experiences/${id}`, data),
  delete: (id) => api.delete(`/api/experiences/${id}`)
}

export default api
