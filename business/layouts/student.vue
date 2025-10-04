<template>
  <div class="min-h-screen bg-gray-100">
    <!-- Header -->
    <el-header class="bg-white shadow-sm">
      <div class="flex items-center justify-between h-16">
        <div class="flex items-center">
          <img src="~/assets/images/logo.png" alt="Logo" class="h-8 w-auto" />
          <h1 class="ml-4 text-xl font-semibold">Hệ thống Quản lý Sinh viên</h1>
        </div>
        
        <div class="flex items-center">
          <!-- Help Button -->
          <el-button type="info" :icon="QuestionFilled" circle class="mr-4" @click="showHelp" />

          <!-- Notifications -->
          <el-popover placement="bottom" :width="300" trigger="click">
            <template #reference>
              <el-badge :value="unreadNotifications.length" :hidden="!unreadNotifications.length">
                <el-button :icon="Bell" circle />
              </el-badge>
            </template>
            <div class="notifications-popup">
              <div class="flex justify-between items-center mb-2">
                <h3 class="text-lg font-semibold">Thông báo</h3>
                <el-button v-if="unreadNotifications.length" type="primary" link @click="markAllAsRead">
                  Đánh dấu đã đọc tất cả
                </el-button>
              </div>
              <el-scrollbar max-height="300px">
                <template v-if="notifications.length">
                  <div
                    v-for="notice in notifications"
                    :key="notice.id"
                    class="notification-item"
                    :class="{ 'bg-gray-50': !notice.read }"
                    @click="viewNotification(notice)"
                  >
                    <div class="flex items-start p-3 hover:bg-gray-50 cursor-pointer">
                      <el-icon :size="20" :class="getNotificationIcon(notice.type).class">
                        <component :is="getNotificationIcon(notice.type).icon" />
                      </el-icon>
                      <div class="ml-3 flex-1">
                        <p class="text-sm font-medium">{{ notice.title }}</p>
                        <p class="text-xs text-gray-500 line-clamp-2">{{ notice.content }}</p>
                        <span class="text-xs text-gray-400">{{ formatDate(notice.time) }}</span>
                      </div>
                    </div>
                  </div>
                </template>
                <el-empty v-else description="Không có thông báo" />
              </el-scrollbar>
              <div class="text-center mt-2">
                <el-button type="primary" link @click="router.push('/student/notifications')">
                  Xem tất cả thông báo
                </el-button>
              </div>
            </div>
          </el-popover>

          <!-- User Menu -->
          <el-dropdown class="ml-4" trigger="click">
            <div class="flex items-center cursor-pointer">
              <el-avatar :size="32" :src="auth.user?.avatar || defaultAvatar" />
              <span class="ml-2 text-sm">{{ auth.user?.first_name }} {{ auth.user?.last_name }}</span>
              <el-icon class="el-icon--right"><arrow-down /></el-icon>
            </div>

            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="router.push('/student/profile')">
                  <el-icon><User /></el-icon>
                  <span>Thông tin cá nhân</span>
                </el-dropdown-item>
                <el-dropdown-item @click="router.push('/student/change-password')">
                  <el-icon><Lock /></el-icon>
                  <span>Đổi mật khẩu</span>
                </el-dropdown-item>
                <el-dropdown-item divided @click="handleLogout">
                  <el-icon><SwitchButton /></el-icon>
                  <span>Đăng xuất</span>
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </el-header>

    <!-- Main Content -->
    <div class="flex">
      <!-- Sidebar -->
      <el-aside width="250px" class="bg-white shadow-sm min-h-[calc(100vh-64px)]">
        <el-menu
          :default-active="activeMenu"
          class="h-full"
          @select="handleSelect"
        >
          <el-menu-item index="/student/dashboard">
            <el-icon><HomeFilled /></el-icon>
            <span>Trang chủ</span>
          </el-menu-item>

          <el-sub-menu index="schedule">
            <template #title>
              <el-icon><Calendar /></el-icon>
              <span>Thời khóa biểu</span>
            </template>
            <el-menu-item index="/student/schedule">Lịch học</el-menu-item>
            <el-menu-item index="/student/exam-schedule">Lịch thi</el-menu-item>
          </el-sub-menu>

          <el-sub-menu index="academic">
            <template #title>
              <el-icon><School /></el-icon>
              <span>Học tập</span>
            </template>
            <el-menu-item index="/student/course-registration">Đăng ký môn học</el-menu-item>
            <el-menu-item index="/student/current-courses">Môn học đang học</el-menu-item>
            <el-menu-item index="/student/grades">Bảng điểm</el-menu-item>
            <el-menu-item index="/student/academic-status">Tình trạng học tập</el-menu-item>
          </el-sub-menu>

          <el-sub-menu index="discipline">
            <template #title>
              <el-icon><Medal /></el-icon>
              <span>Rèn luyện</span>
            </template>
            <el-menu-item index="/student/discipline-points">Điểm rèn luyện</el-menu-item>
            <el-menu-item index="/student/rewards">Khen thưởng</el-menu-item>
            <el-menu-item index="/student/violations">Vi phạm & Kỷ luật</el-menu-item>
          </el-sub-menu>

          <el-sub-menu index="finance">
            <template #title>
              <el-icon><Wallet /></el-icon>
              <span>Tài chính</span>
            </template>
            <el-menu-item index="/student/tuition">Học phí</el-menu-item>
            <el-menu-item index="/student/payment-history">Lịch sử thanh toán</el-menu-item>
            <el-menu-item index="/student/scholarships">Học bổng</el-menu-item>
          </el-sub-menu>

          <el-menu-item index="/student/notifications">
            <el-icon><Bell /></el-icon>
            <span>Thông báo</span>
            <el-badge 
              v-if="unreadNotifications.length" 
              :value="unreadNotifications.length" 
              class="ml-auto mr-4"
            />
          </el-menu-item>
        </el-menu>
      </el-aside>

      <!-- Page Content -->
      <el-main class="flex-1 p-6">
        <!-- Breadcrumb -->
        <el-breadcrumb class="mb-4">
          <el-breadcrumb-item :to="{ path: '/student/dashboard' }">
            Trang chủ
          </el-breadcrumb-item>
          <el-breadcrumb-item 
            v-for="(item, index) in breadcrumbItems" 
            :key="index"
            :to="item.path"
          >
            {{ item.title }}
          </el-breadcrumb-item>
        </el-breadcrumb>

        <!-- Page Title & Actions -->
        <div v-if="pageTitle" class="flex justify-between items-center mb-6">
          <h1 class="text-2xl font-semibold">{{ pageTitle }}</h1>
          <div class="page-actions">
            <slot name="actions" />
          </div>
        </div>

        <!-- Main Content -->
        <slot />
      </el-main>

      <!-- Help Modal -->
      <el-dialog
        v-model="showHelpDialog"
        title="Hướng dẫn sử dụng"
        width="50%"
      >
        <el-scrollbar height="400px">
          <div class="help-content">
            <h3 class="text-lg font-semibold mb-4">Các chức năng chính</h3>
            
            <el-collapse>
              <el-collapse-item title="Thời khóa biểu" name="1">
                <ul class="list-disc ml-4">
                  <li>Xem lịch học theo tuần/tháng</li>
                  <li>Xem chi tiết lịch thi</li>
                  <li>Đăng ký lịch thi lại (nếu có)</li>
                </ul>
              </el-collapse-item>

              <el-collapse-item title="Học tập" name="2">
                <ul class="list-disc ml-4">
                  <li>Đăng ký/hủy môn học trong thời gian quy định</li>
                  <li>Xem điểm các môn học</li>
                  <li>Xem điểm trung bình và xếp loại</li>
                </ul>
              </el-collapse-item>

              <el-collapse-item title="Rèn luyện" name="3">
                <ul class="list-disc ml-4">
                  <li>Theo dõi điểm rèn luyện</li>
                  <li>Xem thông tin khen thưởng</li>
                  <li>Xem thông tin kỷ luật (nếu có)</li>
                </ul>
              </el-collapse-item>

              <el-collapse-item title="Tài chính" name="4">
                <ul class="list-disc ml-4">
                  <li>Xem thông tin học phí</li>
                  <li>Tra cứu lịch sử đóng học phí</li>
                  <li>Xem thông tin học bổng</li>
                </ul>
              </el-collapse-item>
            </el-collapse>

            <div class="mt-4">
              <p class="text-sm text-gray-500">
                Nếu bạn cần hỗ trợ thêm, vui lòng liên hệ:
                <br />
                Email: support@university.edu.vn
                <br />
                Hotline: 1900 xxxx
              </p>
            </div>
          </div>
        </el-scrollbar>
      </el-dialog>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '~/stores/auth'
import defaultAvatar from '~/assets/images/default-avatar.png'
import {
  HomeFilled,
  Calendar,
  School,
  Medal,
  Wallet,
  Bell,
  User,
  Lock,
  SwitchButton,
  ArrowDown,
  QuestionFilled
} from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

// Menu handling
const activeMenu = computed(() => route.path)

function handleSelect(key: string) {
  router.push(key)
}

// Breadcrumb
const breadcrumbItems = computed(() => {
  const paths = route.path.split('/').filter(Boolean)
  return paths.slice(1).map((path, index) => {
    const fullPath = '/' + paths.slice(0, index + 2).join('/')
    return {
      path: fullPath,
      title: getBreadcrumbTitle(path)
    }
  })
})

function getBreadcrumbTitle(path: string) {
  const titles = {
    dashboard: 'Trang chủ',
    schedule: 'Lịch học',
    'exam-schedule': 'Lịch thi',
    'course-registration': 'Đăng ký môn học',
    'current-courses': 'Môn học hiện tại',
    grades: 'Bảng điểm',
    'academic-status': 'Tình trạng học tập',
    'discipline-points': 'Điểm rèn luyện',
    rewards: 'Khen thưởng',
    violations: 'Vi phạm & Kỷ luật',
    tuition: 'Học phí',
    'payment-history': 'Lịch sử thanh toán',
    scholarships: 'Học bổng',
    notifications: 'Thông báo',
    profile: 'Thông tin cá nhân',
    'change-password': 'Đổi mật khẩu'
  }
  return titles[path] || path
}

// Page title
const pageTitle = computed(() => {
  return getBreadcrumbTitle(route.path.split('/').pop() || '')
})

// Notifications
const notifications = ref([
  {
    id: 1,
    title: 'Thông báo học phí',
    content: 'Hạn nộp học phí học kỳ 1 năm học 2025-2026 là ngày 15/10/2025. Sinh viên vui lòng đóng học phí đúng hạn.',
    type: 'warning',
    time: '2025-10-01T10:00:00',
    read: false
  },
  {
    id: 2,
    title: 'Lịch thi giữa kỳ',
    content: 'Lịch thi giữa kỳ các môn học đã được cập nhật. Vui lòng kiểm tra lịch thi trong mục Lịch thi.',
    type: 'info',
    time: '2025-10-01T09:30:00',
    read: false
  },
  {
    id: 3,
    title: 'Đăng ký môn học',
    content: 'Thời gian đăng ký môn học học kỳ 2 bắt đầu từ ngày 15/10/2025.',
    type: 'info',
    time: '2025-10-01T09:00:00',
    read: true
  }
])

const unreadNotifications = computed(() => 
  notifications.value.filter(n => !n.read)
)

function markAllAsRead() {
  notifications.value = notifications.value.map(n => ({ ...n, read: true }))
}

function viewNotification(notice) {
  // Mark as read
  notice.read = true
  
  // Navigate based on notification type
  switch (notice.type) {
    case 'tuition':
      router.push('/student/tuition')
      break
    case 'exam':
      router.push('/student/exam-schedule')
      break
    case 'course':
      router.push('/student/course-registration')
      break
    default:
      router.push('/student/notifications')
  }
}

function getNotificationIcon(type: string) {
  const icons = {
    info: { icon: 'information', class: 'text-blue-500' },
    warning: { icon: 'warning', class: 'text-yellow-500' },
    success: { icon: 'success', class: 'text-green-500' },
    error: { icon: 'error', class: 'text-red-500' }
  }
  return icons[type] || icons.info
}

function formatDate(date: string) {
  return new Date(date).toLocaleDateString('vi-VN', {
    hour: '2-digit',
    minute: '2-digit',
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
}

// Help Dialog
const showHelpDialog = ref(false)

function showHelp() {
  showHelpDialog.value = true
}

// Logout handling
async function handleLogout() {
  try {
    await auth.logout()
    router.push('/login')
  } catch (error) {
    console.error('Logout failed:', error)
    ElMessage.error('Đăng xuất thất bại. Vui lòng thử lại.')
  }
}
</script>

<style scoped>
.notification-item {
  border-bottom: 1px solid #f0f0f0;
}

.notification-item:last-child {
  border-bottom: none;
}

.notification-item:hover {
  background-color: var(--el-fill-color-light);
}

.el-menu {
  border-right: none;
}

.help-content {
  font-size: 14px;
  line-height: 1.6;
}

.help-content ul {
  margin-bottom: 1rem;
}

.help-content li {
  margin-bottom: 0.5rem;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .el-aside {
    width: 200px !important;
  }
}

@media (max-width: 640px) {
  .el-header {
    padding: 0 1rem;
  }
  
  .el-main {
    padding: 1rem;
  }
}
</style>
