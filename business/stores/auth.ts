import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  user_type: 'admin' | 'teacher' | 'student';
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)
  const refreshToken = ref<string | null>(null)

  const isAuthenticated = computed(() => !!token.value)
  const isStudent = computed(() => user.value?.user_type === 'student')
  const isAdmin = computed(() => user.value?.user_type === 'admin')
  const isTeacher = computed(() => user.value?.user_type === 'teacher')
  const userRole = computed(() => user.value?.user_type)

  const canManageStudents = computed(() => isAdmin.value || isTeacher.value)
  const canManageGrades = computed(() => isAdmin.value || isTeacher.value)
  const canManageTuition = computed(() => isAdmin.value)
  const canViewGrades = computed(() => true) // Everyone can view grades
  const canViewSchedule = computed(() => true) // Everyone can view schedule

  async function login(email: string, password: string) {
    try {
      const response = await axios.post('/api/students/auth/login/', {
        email,
        password
      })

      token.value = response.data.access
      refreshToken.value = response.data.refresh
      user.value = response.data.user

      // Set auth header for future requests
      axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`

      return { success: true }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'Login failed'
      }
    }
  }

  async function refreshAccessToken() {
    try {
      const response = await axios.post('/api/students/auth/refresh/', {
        refresh: refreshToken.value
      })

      token.value = response.data.access
      axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`

      return { success: true }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'Token refresh failed'
      }
    }
  }

  function logout() {
    user.value = null
    token.value = null
    refreshToken.value = null
    delete axios.defaults.headers.common['Authorization']
  }

  // Auto refresh token before expiry
  let refreshInterval
  function startTokenRefresh() {
    refreshInterval = setInterval(async () => {
      const result = await refreshAccessToken()
      if (!result.success) {
        logout()
      }
    }, 4 * 60 * 1000) // Refresh every 4 minutes
  }

  function stopTokenRefresh() {
    if (refreshInterval) {
      clearInterval(refreshInterval)
    }
  }

  return {
    user,
    isAuthenticated,
    isStudent,
    login,
    logout,
    refreshAccessToken,
    startTokenRefresh,
    stopTokenRefresh
  }
})