<template>
  <div class="flex min-h-screen items-center justify-center bg-gray-100">
    <el-card class="w-full max-w-md">
      <template #header>
        <h1 class="text-2xl font-semibold text-center">Đăng nhập</h1>
      </template>

      <el-form 
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        label-position="top"
        @submit.prevent="handleLogin"
      >
        <el-form-item label="Email" prop="email">
          <el-input
            v-model="loginForm.email"
            type="email"
            placeholder="Nhập email"
            :prefix-icon="User"
          />
        </el-form-item>

        <el-form-item label="Mật khẩu" prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="Nhập mật khẩu"
            :prefix-icon="Lock"
            show-password
          />
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            native-type="submit"
            class="w-full"
            :loading="loading"
          >
            Đăng nhập
          </el-button>
        </el-form-item>
      </el-form>

      <div v-if="error" class="mt-4">
        <el-alert
          :title="error"
          type="error"
          show-icon
          :closable="false"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '~/stores/auth'
import { Lock, User } from '@element-plus/icons-vue'
import type { FormInstance, FormRules } from 'element-plus'

const router = useRouter()
const auth = useAuthStore()

const loginFormRef = ref<FormInstance>()
const loading = ref(false)
const error = ref('')

const loginForm = ref({
  email: '',
  password: ''
})

const loginRules: FormRules = {
  email: [
    { required: true, message: 'Email là bắt buộc', trigger: 'blur' },
    { type: 'email', message: 'Email không hợp lệ', trigger: 'blur' }
  ],
  password: [
    { required: true, message: 'Mật khẩu là bắt buộc', trigger: 'blur' },
    { min: 6, message: 'Mật khẩu phải có ít nhất 6 ký tự', trigger: 'blur' }
  ]
}

async function handleLogin() {
  if (!loginFormRef.value) return

  try {
    await loginFormRef.value.validate()
    
    loading.value = true
    error.value = ''

    const result = await auth.login(
      loginForm.value.email,
      loginForm.value.password
    )

    if (result.success) {
      // Redirect will be handled by middleware
      if (auth.isAdmin) {
        router.push('/websites')
      } else if (auth.isStudent) {
        router.push('/student')
      }
    } else {
      error.value = result.error || 'Đăng nhập thất bại'
    }
  } catch (err) {
    error.value = 'Vui lòng kiểm tra lại thông tin đăng nhập'
  } finally {
    loading.value = false
  }
}

// Redirect if already logged in
if (process.client && auth.isAuthenticated) {
  if (auth.user?.user_type === 'admin') {
    router.push('/admin/dashboard')
  } else if (auth.user?.user_type === 'student') {
    router.push('/student/dashboard')
  }
}
</script>

<style scoped>
.el-card {
  border-radius: 8px;
}

.el-button {
  height: 40px;
  font-size: 16px;
}

.el-input {
  height: 40px;
}
</style>