<template>
  <div>
    <el-menu
      :default-active="activeIndex"
      mode="horizontal"
      @select="handleSelect"
      class="student-nav"
    >
      <!-- Student menu -->
      <el-menu-item v-if="isStudent" index="dashboard">
        <el-icon><HomeFilled /></el-icon>
        {{ $t('Trang chủ') }}
      </el-menu-item>
      <el-menu-item v-if="isStudent" index="profile">
        <el-icon><User /></el-icon>
        {{ $t('Thông tin cá nhân') }}
      </el-menu-item>
      <el-menu-item v-if="isStudent" index="grades">
        <el-icon><Document /></el-icon>
        {{ $t('Điểm số') }}
      </el-menu-item>
      <el-menu-item v-if="isStudent" index="classes">
        <el-icon><Collection /></el-icon>
        {{ $t('Lớp học') }}
      </el-menu-item>
      <el-menu-item v-if="isStudent" index="schedule">
        <el-icon><Calendar /></el-icon>
        {{ $t('Lịch học') }}
      </el-menu-item>
      <el-menu-item v-if="isStudent" index="registration">
        <el-icon><Edit /></el-icon>
        {{ $t('Đăng ký học phần') }}
      </el-menu-item>
      <el-menu-item v-if="isStudent" index="tuition">
        <el-icon><Wallet /></el-icon>
        {{ $t('Học phí') }}
      </el-menu-item>

      <!-- Admin/teacher menu -->
      <el-menu-item v-if="isAdminOrTeacher" index="student-management">
        <el-icon><User /></el-icon>
        Quản lý sinh viên
      </el-menu-item>
      <el-menu-item v-if="isAdminOrTeacher" index="class-management">
        <el-icon><Collection /></el-icon>
        Quản lý lớp học
      </el-menu-item>
      <el-menu-item v-if="isAdminOrTeacher" index="subject-management">
        <el-icon><Document /></el-icon>
        Quản lý môn học
      </el-menu-item>
      <el-menu-item v-if="isAdminOrTeacher" index="grade-management">
        <el-icon><Document /></el-icon>
        Quản lý điểm số
      </el-menu-item>
      <el-menu-item v-if="isAdminOrTeacher" index="tuition-management">
        <el-icon><Wallet /></el-icon>
        Quản lý học phí
      </el-menu-item>
    </el-menu>

    <router-view />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { HomeFilled, User, Document, Collection, Calendar, Wallet, Edit } from '@element-plus/icons-vue'

const router = useRouter()
const activeIndex = ref('dashboard')
const auth = useAuthStore()

const isStudent = computed(() => auth.user?.user_type === 'student')
const isAdminOrTeacher = computed(() => {
  return auth.user?.user_type === 'admin' || auth.user?.user_type === 'teacher'
})

const handleSelect = (key: string) => {
  if (isStudent.value) {
    router.push(`/student/${key}`)
  } else if (isAdminOrTeacher.value) {
    router.push(`/admin/${key}`)
  }
}
</script>

<style scoped>
.student-nav {
  margin-bottom: 20px;
}
</style>