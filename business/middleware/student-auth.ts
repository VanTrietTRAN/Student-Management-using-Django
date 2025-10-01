import { useAuthStore } from '~/stores/auth'

export default defineNuxtRouteMiddleware((to) => {
  if (process.client) {
    const auth = useAuthStore()

    if (!auth.isAuthenticated && to.path !== '/login') {
      return navigateTo('/login')
    }

    // Student routes
    if (to.path.startsWith('/student/')) {
      if (!auth.isStudent) {
        return navigateTo('/unauthorized')
      }
    }

    // Admin routes
    if (to.path.startsWith('/admin/')) {
      if (auth.user?.user_type !== 'admin') {
        return navigateTo('/unauthorized')
      }
    }

    // Teacher routes
    if (to.path.startsWith('/teacher/')) {
      if (auth.user?.user_type !== 'teacher') {
        return navigateTo('/unauthorized')
      }
    }

    // After login, redirect to appropriate dashboard
    if (to.path === '/login' && auth.isAuthenticated) {
      switch (auth.user?.user_type) {
        case 'student':
          return navigateTo('/student/dashboard')
        case 'admin':
          return navigateTo('/admin/dashboard')
        case 'teacher':
          return navigateTo('/teacher/dashboard')
        default:
          return navigateTo('/unauthorized')
      }
    }
  }
})