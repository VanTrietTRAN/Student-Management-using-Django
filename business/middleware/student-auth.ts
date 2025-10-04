import { useAuthStore } from '~/stores/auth'

export default defineNuxtRouteMiddleware((to) => {
  if (process.client) {
    const auth = useAuthStore()

    if (!auth.isAuthenticated && to.path !== '/login') {
      return navigateTo('/login')
    }

    // Student routes
    if (to.path.startsWith('/student')) {
      if (!auth.isStudent) {
        return navigateTo('/unauthorized')
      }
    }

    // Admin routes
    if (to.path.startsWith('/websites') || to.path.startsWith('/admin')) {
      if (!auth.isAdmin) {
        return navigateTo('/unauthorized')
      }
    }

    // After login, redirect to appropriate dashboard
    if (to.path === '/login' && auth.isAuthenticated) {
      if (auth.isAdmin) {
        return navigateTo('/websites')
      } else if (auth.isStudent) {
        return navigateTo('/student')
      } else {
        return navigateTo('/unauthorized')
      }
    }
  }
})