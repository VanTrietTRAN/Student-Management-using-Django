import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const useStudentStore = defineStore('student', () => {
  // State
  const profile = ref(null)
  const grades = ref([])
  const classes = ref([])
  const schedule = ref([])
  const registrations = ref([])
  const tuitionFees = ref([])
  const loading = ref(false)
  const error = ref(null)

  // API calls
  async function fetchProfile() {
    try {
      loading.value = true
      const response = await axios.get('/api/students/profile/my_profile/')
      profile.value = response.data
      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.error || 'Failed to fetch profile'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  async function updateProfile(data) {
    try {
      loading.value = true
      const response = await axios.patch('/api/students/profile/my_profile/', data)
      profile.value = response.data
      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.error || 'Failed to update profile'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  async function fetchGrades() {
    try {
      loading.value = true
      const response = await axios.get('/api/students/profile/my_grades/')
      grades.value = response.data
      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.error || 'Failed to fetch grades'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  async function fetchClasses() {
    try {
      loading.value = true
      const response = await axios.get('/api/students/profile/current_classes/')
      classes.value = response.data
      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.error || 'Failed to fetch classes'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  async function fetchSchedule() {
    try {
      loading.value = true
      const response = await axios.get('/api/students/profile/schedule/')
      schedule.value = response.data
      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.error || 'Failed to fetch schedule'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  async function registerCourse(classId) {
    try {
      loading.value = true
      const response = await axios.post('/api/students/registration/', {
        class_instance: classId
      })
      await fetchRegistrations()
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.error || 'Failed to register course'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  async function fetchRegistrations() {
    try {
      loading.value = true
      const response = await axios.get('/api/students/registration/')
      registrations.value = response.data
      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.error || 'Failed to fetch registrations'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  async function fetchTuitionFees() {
    try {
      loading.value = true
      const response = await axios.get('/api/students/tuition/')
      tuitionFees.value = response.data
      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.error || 'Failed to fetch tuition fees'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  // Reset store
  function reset() {
    profile.value = null
    grades.value = []
    classes.value = []
    schedule.value = []
    registrations.value = []
    tuitionFees.value = []
    loading.value = false
    error.value = null
  }

  return {
    // State
    profile,
    grades,
    classes,
    schedule,
    registrations,
    tuitionFees,
    loading,
    error,

    // Actions
    fetchProfile,
    updateProfile,
    fetchGrades,
    fetchClasses,
    fetchSchedule,
    registerCourse,
    fetchRegistrations,
    fetchTuitionFees,
    reset
  }
})