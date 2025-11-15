import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Token expired, try to refresh
      const refreshToken = localStorage.getItem('refresh_token')
      if (refreshToken) {
        try {
          const response = await axios.post(
            `${api.defaults.baseURL}/auth/refresh`,
            { refresh_token: refreshToken }
          )
          localStorage.setItem('access_token', response.data.access_token)
          localStorage.setItem('refresh_token', response.data.refresh_token)

          // Retry original request
          error.config.headers.Authorization = `Bearer ${response.data.access_token}`
          return api.request(error.config)
        } catch (refreshError) {
          // Refresh failed, logout
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          window.location.href = '/login'
        }
      } else {
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)

export default api

// API Services
export const authService = {
  register: (userData) => api.post('/auth/register', userData),
  login: (credentials) => api.post('/auth/login', new URLSearchParams(credentials), {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  }),
  getMe: () => api.get('/auth/me'),
}

export const datasetService = {
  upload: (file, data) => {
    const formData = new FormData()
    formData.append('file', file)
    if (data.name) formData.append('name', data.name)
    if (data.description) formData.append('description', data.description)
    return api.post('/datasets/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  list: () => api.get('/datasets/'),
  get: (id) => api.get(`/datasets/${id}`),
  profile: (id) => api.get(`/datasets/${id}/profile`),
  preview: (id, nRows = 100) => api.get(`/datasets/${id}/preview?n_rows=${nRows}`),
  delete: (id) => api.delete(`/datasets/${id}`),
}

export const statisticsService = {
  descriptives: (data) => api.post('/statistics/descriptives', data),
  frequencies: (datasetId, variable, bins) =>
    api.post(`/statistics/frequencies?dataset_id=${datasetId}&variable=${variable}${bins ? `&bins=${bins}` : ''}`),
  ttest: (data) => api.post('/statistics/ttest', data),
  anova: (data) => api.post('/statistics/anova', data),
  correlation: (data) => api.post('/statistics/correlation', data),
  crosstabs: (data) => api.post('/statistics/crosstabs', data),
  regression: (data, type = 'linear') => api.post(`/statistics/regression/${type}`, data),
  factorAnalysis: (data) => api.post('/statistics/factor-analysis', data),
  clusterAnalysis: (data) => api.post('/statistics/cluster-analysis', data),
}

export const mlService = {
  train: (data) => api.post('/ml/train', data),
  automl: (data) => api.post('/ml/automl', data),
  predict: (modelId, datasetId) => api.post('/ml/predict', { model_id: modelId, dataset_id: datasetId }),
  list: () => api.get('/ml/models'),
}
