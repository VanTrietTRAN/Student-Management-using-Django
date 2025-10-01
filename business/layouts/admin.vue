&lt;template>
  &lt;div class="admin-layout">
    &lt;el-menu mode="vertical" :router="true" class="admin-menu">
      &lt;el-menu-item index="/admin/dashboard">
        &lt;el-icon>&lt;HomeFilled />&lt;/el-icon>
        Trang chủ
      &lt;/el-menu-item>
      &lt;el-menu-item index="/admin/students">
        &lt;el-icon>&lt;User />&lt;/el-icon>
        Quản lý sinh viên
      &lt;/el-menu-item>
      &lt;el-menu-item index="/admin/teachers">
        &lt;el-icon>&lt;User />&lt;/el-icon>
        Quản lý giảng viên
      &lt;/el-menu-item>
      &lt;el-menu-item index="/admin/classes">
        &lt;el-icon>&lt;Document />&lt;/el-icon>
        Quản lý lớp học
      &lt;/el-menu-item>
      &lt;el-menu-item index="/admin/grades">
        &lt;el-icon>&lt;Document />&lt;/el-icon>
        Quản lý điểm số
      &lt;/el-menu-item>
      &lt;el-menu-item index="/admin/schedule">
        &lt;el-icon>&lt;Calendar />&lt;/el-icon>
        Quản lý lịch học
      &lt;/el-menu-item>
      &lt;el-menu-item index="/admin/tuition">
        &lt;el-icon>&lt;Wallet />&lt;/el-icon>
        Quản lý học phí
      &lt;/el-menu-item>
    &lt;/el-menu>
    &lt;div class="admin-content">
      &lt;slot />
    &lt;/div>
  &lt;/div>
&lt;/template>

&lt;script setup lang="ts">
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

onMounted(() => {
  if (!auth.isAuthenticated || auth.user?.user_type !== 'admin') {
    router.push('/login')
  }
})
&lt;/script>

&lt;style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
}

.admin-menu {
  width: 250px;
  min-height: 100vh;
  border-right: 1px solid #dcdfe6;
}

.admin-content {
  flex-grow: 1;
  padding: 20px;
}
&lt;/style>