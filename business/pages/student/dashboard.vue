<template>
  <div>
    <h1 class="text-2xl mb-6">Trang sinh viên</h1>

    <el-row :gutter="20">
      <!-- Thông tin cá nhân -->
      <el-col :span="8">
        <el-card class="info-card">
          <template #header>
            <div class="card-header">
              <h3>Thông tin cá nhân</h3>
              <el-button type="primary" @click="router.push('/websites/student-profile')">
                Chi tiết
              </el-button>
            </div>
          </template>
          <div v-if="auth.user" class="card-content">
            <div class="avatar-container">
              <el-avatar :size="64" :src="auth.user.profile_picture || defaultAvatar" />
            </div>
            <div class="user-info">
              <p class="name">{{ auth.user.first_name }} {{ auth.user.last_name }}</p>
              <p class="email">{{ auth.user.email }}</p>
              <p class="student-id">MSSV: {{ studentInfo.student_id || 'N/A' }}</p>
              <p class="class">Lớp: {{ studentInfo.class_name || 'N/A' }}</p>
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- Điểm số -->
      <el-col :span="8">
        <el-card class="info-card">
          <template #header>
            <div class="card-header">
              <h3>Điểm số gần đây</h3>
              <el-button type="primary" @click="router.push('/websites/student-grades')">
                Xem tất cả
              </el-button>
            </div>
          </template>
          <div v-if="recentGrades && recentGrades.length > 0" class="grades-list">
            <el-table :data="recentGrades" stripe>
              <el-table-column prop="subject" label="Môn học" />
              <el-table-column prop="score" label="Điểm số">
                <template #default="{ row }">
                  <span :class="{ 'text-success': row.score >= 7, 'text-warning': row.score >= 5 && row.score < 7, 'text-danger': row.score < 5 }">
                    {{ row.score }}
                  </span>
                </template>
              </el-table-column>
              <el-table-column prop="date" label="Ngày cập nhật" />
            </el-table>
          </div>
          <div v-else class="empty-state">
            <el-empty description="Chưa có điểm số nào" />
          </div>
        </el-card>
      </el-col>

      <!-- Học phí -->
      <el-col :span="8">
        <el-card class="info-card">
          <template #header>
            <div class="card-header">
              <h3>Học phí</h3>
              <el-button type="primary" @click="router.push('/websites/student-tuition')">
                Chi tiết
              </el-button>
            </div>
          </template>
          <div v-if="tuitionInfo" class="tuition-info">
            <el-progress
              type="dashboard"
              :percentage="tuitionInfo.paidPercentage"
              :color="tuitionProgressColor"
            />
            <div class="tuition-details">
              <div class="detail-item">
                <span class="label">Tổng học phí:</span>
                <span class="value">{{ formatCurrency(tuitionInfo.total) }}</span>
              </div>
              <div class="detail-item">
                <span class="label">Đã đóng:</span>
                <span class="value text-success">{{ formatCurrency(tuitionInfo.paid) }}</span>
              </div>
              <div class="detail-item">
                <span class="label">Còn lại:</span>
                <span class="value text-danger">{{ formatCurrency(tuitionInfo.remaining) }}</span>
              </div>
              <div class="detail-item">
                <span class="label">Hạn nộp:</span>
                <span class="value">{{ tuitionInfo.dueDate }}</span>
              </div>
            </div>
          </div>
          <div v-else class="empty-state">
            <el-empty description="Chưa có thông tin học phí" />
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- Lịch học -->
    <div class="schedule-section mt-6">
      <h2 class="text-xl mb-4">Lịch học hôm nay</h2>
      <el-card v-if="todaySchedule && todaySchedule.length > 0">
        <el-table :data="todaySchedule" stripe>
          <el-table-column prop="time" label="Thời gian" width="150" />
          <el-table-column prop="subject" label="Môn học" />
          <el-table-column prop="room" label="Phòng học" width="120" />
          <el-table-column prop="teacher" label="Giảng viên" />
          <el-table-column prop="status" label="Trạng thái" width="120">
            <template #default="{ row }">
              <el-tag :type="row.status === 'ongoing' ? 'success' : row.status === 'upcoming' ? 'warning' : 'info'">
                {{ formatStatus(row.status) }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
      <el-empty v-else description="Không có lịch học nào hôm nay" />
    </div>

    <!-- Thông báo -->
    <div class="announcements-section mt-6">
      <h2 class="text-xl mb-4">Thông báo mới</h2>
      <el-card v-if="announcements && announcements.length > 0">
        <el-timeline>
          <el-timeline-item
            v-for="announcement in announcements"
            :key="announcement.id"
            :timestamp="announcement.time"
            :type="announcement.type"
          >
            <h4>{{ announcement.title }}</h4>
            <p>{{ announcement.content }}</p>
          </el-timeline-item>
        </el-timeline>
      </el-card>
      <el-empty v-else description="Không có thông báo mới" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import defaultAvatar from '@/assets/images/default-avatar.png'

const router = useRouter()
const auth = useAuthStore()

// State
const studentInfo = ref({
  student_id: '',
  class_name: '',
})

const recentGrades = ref([])
const tuitionInfo = ref(null)
const todaySchedule = ref([])
const announcements = ref([])

// Computed
const tuitionProgressColor = computed(() => {
  if (!tuitionInfo.value) return ''
  const percentage = tuitionInfo.value.paidPercentage
  if (percentage >= 80) return '#67C23A'
  if (percentage >= 50) return '#E6A23C'
  return '#F56C6C'
})

// Functions
function formatCurrency(amount: number) {
  return new Intl.NumberFormat('vi-VN', {
    style: 'currency',
    currency: 'VND'
  }).format(amount)
}

function formatStatus(status: string) {
  const statusMap = {
    'ongoing': 'Đang diễn ra',
    'upcoming': 'Sắp diễn ra',
    'completed': 'Đã kết thúc'
  }
  return statusMap[status] || status
}

onMounted(async () => {
  if (!auth.isAuthenticated || !auth.isStudent) {
    router.push('/login')
    return
  }

  try {
    await fetchDashboardData()
  } catch (error) {
    console.error('Error fetching dashboard data:', error)
  }
})

async function fetchDashboardData() {
  try {
    // Mock data - replace with actual API calls
    studentInfo.value = {
      student_id: '20020001',
      class_name: 'K65-CN1',
    }

    recentGrades.value = [
      { subject: 'Toán cao cấp', score: 8.5, date: '2025-09-30' },
      { subject: 'Lập trình web', score: 7.8, date: '2025-09-29' },
      { subject: 'Cơ sở dữ liệu', score: 8.0, date: '2025-09-28' },
    ]

    tuitionInfo.value = {
      total: 15000000,
      paid: 10000000,
      remaining: 5000000,
      paidPercentage: 66.67,
      dueDate: '2025-10-15'
    }

    todaySchedule.value = [
      { time: '07:00 - 09:00', subject: 'Toán cao cấp', room: 'D3-101', teacher: 'Nguyễn Văn A', status: 'completed' },
      { time: '09:30 - 11:30', subject: 'Lập trình web', room: 'D3-205', teacher: 'Trần Thị B', status: 'ongoing' },
      { time: '13:30 - 15:30', subject: 'Cơ sở dữ liệu', room: 'D3-304', teacher: 'Lê Văn C', status: 'upcoming' },
    ]

    announcements.value = [
      {
        id: 1,
        title: 'Thông báo nghỉ học',
        content: 'Lớp Toán cao cấp ngày mai sẽ nghỉ học',
        time: '2025-10-01 15:00',
        type: 'warning'
      },
      {
        id: 2,
        title: 'Lịch thi giữa kỳ',
        content: 'Lịch thi giữa kỳ đã được cập nhật',
        time: '2025-10-01 14:00',
        type: 'success'
      },
      {
        id: 3,
        title: 'Đăng ký học phần',
        content: 'Hạn đăng ký học phần kết thúc vào ngày 15/10/2025',
        time: '2025-10-01 13:00',
        type: 'info'
      },
    ]
  } catch (error) {
    console.error('Error:', error)
  }
}
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
  font-size: 1.1rem;
}

.info-card {
  height: 100%;
}

.card-content {
  text-align: center;
}

.avatar-container {
  margin-bottom: 1rem;
}

.user-info {
  text-align: left;
}

.user-info .name {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.user-info p {
  margin: 0.5rem 0;
  color: var(--el-text-color-regular);
}

.grades-list {
  max-height: 300px;
  overflow-y: auto;
}

.tuition-info {
  text-align: center;
  padding: 1rem;
}

.tuition-details {
  margin-top: 1rem;
  text-align: left;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  margin: 0.5rem 0;
}

.text-success {
  color: var(--el-color-success);
}

.text-warning {
  color: var(--el-color-warning);
}

.text-danger {
  color: var(--el-color-danger);
}

.schedule-section,
.announcements-section {
  margin-top: 2rem;
}

.empty-state {
  padding: 2rem;
  text-align: center;
}

.el-timeline {
  max-height: 300px;
  overflow-y: auto;
}
</style>