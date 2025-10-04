<template>
  <div>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-6">
      <!-- Thông tin học tập -->
      <el-card>
        <template #header>
          <div class="flex items-center">
            <el-icon class="mr-2"><School /></el-icon>
            <span>Thông tin học tập</span>
          </div>
        </template>
        <div class="space-y-4">
          <div>
            <p class="text-sm text-gray-500">Điểm trung bình tích lũy</p>
            <p class="text-xl font-semibold">3.65/4.0</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">Số tín chỉ đã đạt</p>
            <p class="text-xl font-semibold">85/150</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">Xếp loại</p>
            <el-tag type="success">Giỏi</el-tag>
          </div>
        </div>
      </el-card>

      <!-- Thông tin học phí -->
      <el-card>
        <template #header>
          <div class="flex items-center">
            <el-icon class="mr-2"><Wallet /></el-icon>
            <span>Thông tin học phí</span>
          </div>
        </template>
        <div class="space-y-4">
          <div>
            <p class="text-sm text-gray-500">Học phí học kỳ hiện tại</p>
            <p class="text-xl font-semibold">12,500,000 VNĐ</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">Đã đóng</p>
            <p class="text-xl font-semibold text-green-600">6,250,000 VNĐ</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">Còn nợ</p>
            <p class="text-xl font-semibold text-red-600">6,250,000 VNĐ</p>
          </div>
        </div>
      </el-card>

      <!-- Thông tin điểm rèn luyện -->
      <el-card>
        <template #header>
          <div class="flex items-center">
            <el-icon class="mr-2"><Medal /></el-icon>
            <span>Điểm rèn luyện</span>
          </div>
        </template>
        <div class="space-y-4">
          <div>
            <p class="text-sm text-gray-500">Điểm rèn luyện học kỳ</p>
            <p class="text-xl font-semibold">85/100</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">Xếp loại rèn luyện</p>
            <el-tag type="success">Tốt</el-tag>
          </div>
        </div>
      </el-card>
    </div>

    <!-- Lịch học trong tuần -->
    <el-card class="mb-6">
      <template #header>
        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <el-icon class="mr-2"><Calendar /></el-icon>
            <span>Lịch học trong tuần</span>
          </div>
          <el-button type="primary" link @click="router.push('/student/schedule')">
            Xem tất cả
          </el-button>
        </div>
      </template>
      <el-table :data="weeklySchedule" stripe>
        <el-table-column prop="time" label="Thời gian" width="180" />
        <el-table-column prop="subject" label="Môn học" />
        <el-table-column prop="location" label="Phòng học" width="150" />
        <el-table-column prop="teacher" label="Giảng viên" width="200" />
      </el-table>
    </el-card>

    <!-- Thông báo mới -->
    <el-card>
      <template #header>
        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <el-icon class="mr-2"><Bell /></el-icon>
            <span>Thông báo mới</span>
          </div>
          <el-button type="primary" link @click="router.push('/student/notifications')">
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
          <h4 class="font-medium">{{ notice.title }}</h4>
          <p class="text-sm text-gray-600">{{ notice.content }}</p>
        </el-timeline-item>
      </el-timeline>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import {
  School,
  Wallet,
  Medal,
  Calendar,
  Bell
} from '@element-plus/icons-vue'

definePageMeta({
  layout: 'student',
  middleware: ['student-auth']
})

const router = useRouter()

// Dữ liệu mẫu cho lịch học trong tuần
const weeklySchedule = ref([
  {
    time: 'Thứ 2 (7:00 - 9:30)',
    subject: 'Lập trình Web',
    location: 'H1-301',
    teacher: 'Nguyễn Văn A'
  },
  {
    time: 'Thứ 3 (13:00 - 15:30)',
    subject: 'Cơ sở dữ liệu',
    location: 'H2-402',
    teacher: 'Trần Thị B'
  },
  {
    time: 'Thứ 4 (7:00 - 9:30)',
    subject: 'Công nghệ phần mềm',
    location: 'H1-401',
    teacher: 'Lê Văn C'
  }
])

// Dữ liệu mẫu cho thông báo mới
const recentNotifications = ref([
  {
    id: 1,
    title: 'Thông báo về việc đóng học phí học kỳ 1 năm học 2025-2026',
    content: 'Sinh viên vui lòng đóng học phí đúng hạn trước ngày 15/10/2025',
    time: '2025-10-01 10:00',
    type: 'warning'
  },
  {
    id: 2,
    title: 'Lịch thi giữa kỳ học kỳ 1 năm học 2025-2026',
    content: 'Lịch thi giữa kỳ đã được cập nhật trên hệ thống',
    time: '2025-09-30 15:30',
    type: 'info'
  },
  {
    id: 3,
    title: 'Thông báo nghỉ học ngày 20/10/2025',
    content: 'Toàn trường nghỉ học nhân ngày Phụ nữ Việt Nam 20/10',
    time: '2025-09-29 14:00',
    type: 'info'
  }
])
</script>