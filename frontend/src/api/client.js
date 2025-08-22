import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

// Vytvoření Axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor - přidá token k požadavkům
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor - zpracuje odpovědi a chyby
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response?.status === 401) {
      // Token vypršel nebo není platný
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// API endpoints
export const authAPI = {
  login: (credentials) => {
    const formData = new FormData()
    formData.append('username', credentials.email)
    formData.append('password', credentials.password)
    return apiClient.post('/api/auth/login', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  register: (userData) => apiClient.post('/api/auth/register', userData),
  getCurrentUser: () => apiClient.get('/api/users/me'),
  refreshToken: () => apiClient.post('/api/auth/refresh'),
}

export const transactionsAPI = {
  getAll: (params) => apiClient.get('/api/transactions', { params }),
  create: (transaction) => apiClient.post('/api/transactions', transaction),
  update: (id, transaction) => apiClient.put(`/api/transactions/${id}`, transaction),
  delete: (id) => apiClient.delete(`/api/transactions/${id}`),
  getStats: () => apiClient.get('/api/dashboard/stats'),
}

export const budgetsAPI = {
  getAll: () => apiClient.get('/api/budgets'),
  create: (budget) => apiClient.post('/api/budgets', budget),
  update: (id, budget) => apiClient.put(`/api/budgets/${id}`, budget),
  delete: (id) => apiClient.delete(`/api/budgets/${id}`),
}

export const goalsAPI = {
  getAll: () => apiClient.get('/api/goals'),
  create: (goal) => apiClient.post('/api/goals', goal),
  update: (id, goal) => apiClient.put(`/api/goals/${id}`, goal),
  delete: (id) => apiClient.delete(`/api/goals/${id}`),
  contribute: (id, amount) => apiClient.post(`/api/goals/${id}/contribute`, { amount }),
}

export const categoriesAPI = {
  getAll: () => apiClient.get('/api/categories'),
  create: (category) => apiClient.post('/api/categories', category),
  update: (id, category) => apiClient.put(`/api/categories/${id}`, category),
  delete: (id) => apiClient.delete(`/api/categories/${id}`),
}

export default apiClient