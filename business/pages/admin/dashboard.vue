<template>
  <div>
    <h1 class="text-2xl mb-6">Bảng điều khiển quản trị viên</h1>

    <el-row :gutter="20">
      <el-col :span="6" v-for="(stat, index) in statistics" :key="index">
        <el-card class="mb-4">
          <div class="stat-card">
            <div class="stat-icon">
              <el-icon :size="24">
                <component :is="stat.icon" />
              </el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ stat.value }}</div>
              <div class="stat-label">{{ stat.label }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- Hoạt động gần đây -->
    <div class="recent-activity mt-6">
      <h2 class="text-xl mb-4">Hoạt động gần đây</h2>
      <el-card>
        <el-table :data="recentActivities" stripe>
          <el-table-column prop="time" label="Thời gian" width="180" />
          <el-table-column prop="user" label="Người dùng" width="180" />
          <el-table-column prop="action" label="Hành động" />
          <el-table-column prop="status" label="Trạng thái">
            <template #default="{ row }">
              <el-tag :type="row.status === 'success' ? 'success' : 'danger'">
                {{ row.status === 'success' ? 'Thành công' : 'Thất bại' }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>

    <el-row :gutter="20" class="mt-6">
      <!-- Danh sách sinh viên mới -->
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>Sinh viên mới đăng ký</span>
              <el-button type="primary" @click="router.push('/admin/students')">
                Xem tất cả
              </el-button>
            </div>
          </template>
          <el-table :data="newStudents" stripe>
            <el-table-column prop="name" label="Họ và tên" />
            <el-table-column prop="email" label="Email" />
            <el-table-column prop="registrationDate" label="Ngày đăng ký" />
          </el-table>
        </el-card>
      </el-col>

      <!-- Thông báo hệ thống -->
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>Thông báo hệ thống</span>
              <el-button type="primary" @click="router.push('/admin/notifications')">
                Quản lý
              </el-button>
            </div>
          </template>
          <el-timeline>
            <el-timeline-item
              v-for="(notification, index) in systemNotifications"
              :key="index"
              :timestamp="notification.time"
              :type="notification.type"
            >
              {{ notification.content }}
            </el-timeline-item>
          </el-timeline>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import {
  User,
  Calendar,
  Document,
  School
} from '@element-plus/icons-vue'

const router = useRouter()
const auth = useAuthStore()

// Thống kê chung
const statistics = ref([
  { label: 'Tổng số sinh viên', value: 0, icon: 'User' },
  { label: 'Lớp học đang hoạt động', value: 0, icon: 'School' },
  { label: 'Bài kiểm tra trong tuần', value: 0, icon: 'Document' },
  { label: 'Sự kiện sắp diễn ra', value: 0, icon: 'Calendar' }
])

// Hoạt động gần đây
const recentActivities = ref([])
const newStudents = ref([])
const systemNotifications = ref([])

onMounted(async () => {
  if (!auth.isAuthenticated || auth.user?.user_type !== 'admin') {
    router.push('/login')
    return
  }

  try {
    // Call API to fetch dashboard data
    await fetchDashboardData()
  } catch (error) {
    console.error('Error fetching dashboard data:', error)
  }
})

async function fetchDashboardData() {
  try {
    // Mock data - replace with actual API calls
    statistics.value = [
      { label: 'Tổng số sinh viên', value: 1250, icon: 'User' },
      { label: 'Lớp học đang hoạt động', value: 45, icon: 'School' },
      { label: 'Bài kiểm tra trong tuần', value: 12, icon: 'Document' },
      { label: 'Sự kiện sắp diễn ra', value: 5, icon: 'Calendar' }
    ]

    recentActivities.value = [
      { time: '2025-10-01 15:30', user: 'Nguyễn Văn A', action: 'Đăng ký môn học', status: 'success' },
      { time: '2025-10-01 14:45', user: 'Trần Thị B', action: 'Nộp học phí', status: 'success' },
      { time: '2025-10-01 14:00', user: 'Lê Văn C', action: 'Cập nhật thông tin', status: 'success' },
    ]

    newStudents.value = [
      { name: 'Nguyễn Văn A', email: 'nguyenvana@example.com', registrationDate: '2025-10-01' },
      { name: 'Trần Thị B', email: 'tranthib@example.com', registrationDate: '2025-10-01' },
      { name: 'Lê Văn C', email: 'levanc@example.com', registrationDate: '2025-09-30' },
    ]

    systemNotifications.value = [
      { time: '2025-10-01 15:00', type: 'success', content: 'Hệ thống đã được cập nhật thành công' },
      { time: '2025-10-01 14:00', type: 'warning', content: 'Bảo trì hệ thống vào ngày 05/10/2025' },
      { time: '2025-10-01 13:00', type: 'info', content: 'Thông báo mới về lịch thi học kỳ' },
    ]
  } catch (error) {
    console.error('Error:', error)
  }
}
</script>

<style scoped>
.stat-card {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.stat-icon {
  background-color: var(--el-color-primary-light-9);
  padding: 1rem;
  border-radius: 8px;
  color: var(--el-color-primary);
}

.stat-content {
  flex-grow: 1;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--el-color-primary);
}

.stat-label {
  color: var(--el-text-color-secondary);
  font-size: 0.875rem;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.recent-activity {
  margin-top: 2rem;
}

.el-timeline {
  max-height: 300px;
  overflow-y: auto;
}
</style>