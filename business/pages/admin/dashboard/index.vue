<template>
  <div>
    <!-- Statistics Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
      <el-card>
        <template #header>
          <div class="flex items-center">
            <el-icon class="mr-2"><User /></el-icon>
            <span>Tổng số sinh viên</span>
          </div>
        </template>
        <div class="text-2xl font-bold">2,500</div>
        <div class="text-sm text-gray-500">Đang theo học</div>
      </el-card>

      <el-card>
        <template #header>
          <div class="flex items-center">
            <el-icon class="mr-2"><School /></el-icon>
            <span>Tổng số lớp học</span>
          </div>
        </template>
        <div class="text-2xl font-bold">85</div>
        <div class="text-sm text-gray-500">Học kỳ hiện tại</div>
      </el-card>

      <el-card>
        <template #header>
          <div class="flex items-center">
            <el-icon class="mr-2"><Wallet /></el-icon>
            <span>Học phí đã thu</span>
          </div>
        </template>
        <div class="text-2xl font-bold">2.5 tỷ</div>
        <div class="text-sm text-gray-500">Học kỳ hiện tại</div>
      </el-card>

      <el-card>
        <template #header>
          <div class="flex items-center">
            <el-icon class="mr-2"><Calendar /></el-icon>
            <span>Lớp học hôm nay</span>
          </div>
        </template>
        <div class="text-2xl font-bold">24</div>
        <div class="text-sm text-gray-500">Đang diễn ra</div>
      </el-card>
    </div>

    <!-- Quick Actions -->
    <el-card class="mb-6">
      <template #header>
        <div class="flex items-center">
          <el-icon class="mr-2"><List /></el-icon>
          <span>Thao tác nhanh</span>
        </div>
      </template>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <el-button @click="router.push('/admin/students/new')">
          <el-icon><CirclePlus /></el-icon>
          Thêm sinh viên
        </el-button>
        <el-button @click="router.push('/admin/teachers/new')">
          <el-icon><CirclePlus /></el-icon>
          Thêm giảng viên
        </el-button>
        <el-button @click="router.push('/admin/courses/new')">
          <el-icon><CirclePlus /></el-icon>
          Thêm môn học
        </el-button>
        <el-button @click="router.push('/admin/notifications/new')">
          <el-icon><Bell /></el-icon>
          Tạo thông báo
        </el-button>
      </div>
    </el-card>

    <!-- Recent Activities -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Latest Students -->
      <el-card>
        <template #header>
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <el-icon class="mr-2"><User /></el-icon>
              <span>Sinh viên mới</span>
            </div>
            <el-button type="primary" link @click="router.push('/admin/students')">
              Xem tất cả
            </el-button>
          </div>
        </template>
        <el-table :data="recentStudents" stripe>
          <el-table-column prop="id" label="MSSV" width="100" />
          <el-table-column prop="name" label="Họ và tên" />
          <el-table-column prop="class" label="Lớp" width="100" />
          <el-table-column prop="created_at" label="Ngày thêm" width="150" />
        </el-table>
      </el-card>

      <!-- Latest Notifications -->
      <el-card>
        <template #header>
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <el-icon class="mr-2"><Bell /></el-icon>
              <span>Thông báo gần đây</span>
            </div>
            <el-button type="primary" link @click="router.push('/admin/notifications')">
              Xem tất cả
            </el-button>
          </div>
        </template>
        <el-timeline>
          <el-timeline-item
            v-for="notice in recentNotifications"
            :key="notice.id"
            :type="notice.type"
            :timestamp="notice.time"
          >
            <h4>{{ notice.title }}</h4>
            <p class="text-sm text-gray-600">{{ notice.content }}</p>
          </el-timeline-item>
        </el-timeline>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import {
  User,
  School,
  Wallet,
  Calendar,
  List,
  Bell,
  CirclePlus
} from '@element-plus/icons-vue'

definePageMeta({
  layout: 'admin',
  middleware: ['auth']
})

const router = useRouter()

// Sample data for recent students
const recentStudents = ref([
  {
    id: '20020001',
    name: 'Nguyễn Văn A',
    class: 'K65-CNTT',
    created_at: '2025-10-01'
  },
  {
    id: '20020002',
    name: 'Trần Thị B',
    class: 'K65-CNTT',
    created_at: '2025-10-01'
  },
  {
    id: '20020003',
    name: 'Lê Văn C',
    class: 'K65-CNTT',
    created_at: '2025-10-01'
  }
])

// Sample data for recent notifications
const recentNotifications = ref([
  {
    id: 1,
    title: 'Thông báo lịch thi giữa kỳ',
    content: 'Lịch thi giữa kỳ học kỳ 1 năm học 2025-2026 đã được cập nhật',
    time: '2025-10-02 10:00',
    type: 'primary'
  },
  {
    id: 2,
    title: 'Nhắc nhở đóng học phí',
    content: 'Nhắc nhở sinh viên đóng học phí đúng hạn trước ngày 15/10/2025',
    time: '2025-10-01 15:30',
    type: 'warning'
  },
  {
    id: 3,
    title: 'Cập nhật phần mềm',
    content: 'Hệ thống sẽ bảo trì từ 22:00 ngày 05/10/2025',
    time: '2025-10-01 09:00',
    type: 'info'
  }
])
</script>