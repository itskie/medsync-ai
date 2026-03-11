import axios from 'axios'

// Base API instance pointing to FastAPI backend
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8080',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Auto-attach JWT token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Auth APIs
export const registerUser = (data) => api.post('/auth/register', data)
export const loginUser = (data) => api.post('/auth/login', data)

// HCP APIs
export const getAllHCPs = () => api.get('/hcps/')
export const createHCP = (data) => api.post('/hcps/', data)
export const getHCP = (id) => api.get(`/hcps/${id}`)
export const updateHCP = (id, data) => api.put(`/hcps/${id}`, data)
export const deleteHCP = (id) => api.delete(`/hcps/${id}`)

// Interaction APIs
export const getAllInteractions = () => api.get('/interactions/')
export const createInteraction = (data) => api.post('/interactions/', data)
export const getHCPInteractions = (hcpId) => api.get(`/interactions/hcp/${hcpId}`)

// Agent API
export const chatWithAgent = (message) => api.post('/agent/chat', { message })

export default api