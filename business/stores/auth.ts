import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRuntimeConfig, useFetch } from '#imports'

interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  user_type: 'admin' | 'teacher' | 'student';
}

interface AuthResponse {
  user: User;
  access: string;
  refresh: string;
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)
  const refreshToken = ref<string | null>(null)
  const intervalId = ref<number | null>(null)

  const isAuthenticated = computed(() => !!token.value)
  const isStudent = computed(() => user.value?.user_type === 'student')
  const isAdmin = computed(() => user.value?.user_type === 'admin')
  const isTeacher = computed(() => user.value?.user_type === 'teacher')
  const userRole = computed(() => user.value?.user_type)

  const canManageStudents = computed(() => isAdmin.value || isTeacher.value)
  const canManageGrades = computed(() => isAdmin.value || isTeacher.value)
  const canManageTuition = computed(() => isAdmin.value)
  const canViewGrades = computed(() => true)
  const canViewSchedule = computed(() => true)

  async function login(email: string, password: string) {
    const config = useRuntimeConfig()
    const baseUrl = config.public.apiBase as string

    try {
      // Try student login first
      try {
        const { data, error } = await useFetch<AuthResponse>(`${config.public.defaultHost}/o/token/`, {
          method: 'POST',
          body: new URLSearchParams({
            'grant_type': 'password',
            'username': email,
            'password': password,
                        'client_id': 'ejnIx2wsSw73lvJrGAO3CXO111SikplyDPJ9BdEn',
            'client_secret': 'kUVb7jaAkWcDt9nOjes89SpLmNPRG99VNnRuonudxmxPLGRQEd1fuFzaeBHAQXKvDt6DAE3jheNYZVUFPDOM9lyon399WTdz5thETiHxsZXKAHe59Q1vKAo9E0KGl61f'
          }).toString(),
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        })

        if (error.value) {
          throw new Error(error.value.message)
        }

        if (!data.value) {
          throw new Error('Invalid response from server')
        }

        token.value = data.value.access
        refreshToken.value = data.value.refresh
        user.value = data.value.user
        startTokenRefresh()
        
        return { 
          success: true,
          redirectTo: '/student'
        }
      } catch {
        // If student login fails, try admin login
        const { data, error } = await useFetch<AuthResponse>(`${baseUrl}/api/admin/auth/login/`, {
          method: 'POST',
          body: {
            email,
            password
          }
        })

        if (error.value) {
          throw new Error(error.value.message)
        }

        if (!data.value) {
          throw new Error('Invalid response from server')
        }

        token.value = data.value.access
        refreshToken.value = data.value.refresh
        user.value = data.value.user
        startTokenRefresh()

        return {
          success: true,
          redirectTo: '/websites'
        }
      }
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Login failed',
        redirectTo: '/login'
      }
    }
  }

  async function refreshAccessToken() {
    const config = useRuntimeConfig()
    const baseUrl = config.public.apiBase as string

    try {
      const { data, error } = await useFetch<{ access: string }>(`${baseUrl}/api/students/auth/refresh/`, {
        method: 'POST',
        body: {
          refresh: refreshToken.value
        }
      })

      if (error.value) {
        throw new Error(error.value.message)
      }

      if (!data.value) {
        throw new Error('Invalid response from server')
      }

      token.value = data.value.access
      return { success: true }
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Token refresh failed'
      }
    }
  }

  function logout() {
    user.value = null
    token.value = null
    refreshToken.value = null
    stopTokenRefresh()
  }

  function startTokenRefresh() {
    stopTokenRefresh()
    intervalId.value = window.setInterval(async () => {
      const result = await refreshAccessToken()
      if (!result.success) {
        logout()
      }
    }, 4 * 60 * 1000) // Refresh every 4 minutes
  }

  function stopTokenRefresh() {
    if (intervalId.value !== null) {
      window.clearInterval(intervalId.value)
      intervalId.value = null
    }
  }

  return {
    user,
    token,
    isAuthenticated,
    isStudent,
    isAdmin,
    isTeacher,
    userRole,
    canManageStudents,
    canManageGrades,
    canManageTuition,
    canViewGrades,
    canViewSchedule,
    login,
    logout,
    refreshAccessToken
  }
})