


// boot/axios.js
import { boot } from 'quasar/wrappers'
import axios from 'axios'

// Configuración base
const api = axios.create({
  baseURL: process.env.DEV 
    ? 'http://localhost:8000' 
    : 'https://loteriabackend.onrender.com',
  timeout: 10000, // 10 segundos
})

// Interceptor de request para agregar token automáticamente
api.interceptors.request.use((config) => {
  const CLIENT_TOKEN = "La_mata1985" // Token hardcodeado
  
  // Agregar token como header para TODAS las requests
  config.headers['X-Cliente-Token'] = CLIENT_TOKEN
  
  // Para GET, también agregar como parámetro (backward compatibility)
  if (config.method === 'get' && config.params) {
    config.params.token = CLIENT_TOKEN
  }
  
  console.log(`🚀 ${config.method?.toUpperCase()} ${config.url}`, config.params || config.data)
  return config
})

// Interceptor de response para manejo centralizado de errores
api.interceptors.response.use(
  (response) => {
    console.log(`✅ ${response.status} ${response.config.url}`)
    return response
  },
  (error) => {
    console.error(`❌ ${error.response?.status} ${error.config?.url}`, error)
    
    // Manejo centralizado de errores HTTP
    if (error.response?.status === 401) {
      // Redirigir a login si el token expira
      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')
      window.location.href = '/login'
    }
    
    return Promise.reject(error)
  }
)

export default boot(({ app }) => {
  // Hacer disponible globalmente en Vue
  app.config.globalProperties.$axios = axios
  app.config.globalProperties.$api = api
})

export { axios, api }