<template>
    <div class="min-h-screen bg-gray-50 pt-20 px-4 md:px-6 pb-6">
        <!-- Header Section -->
        <div class="mb-8">
            <h1 class="text-3xl font-bold text-gray-900 mb-2">Dashboard Giảng viên</h1>
            <p class="text-gray-600">Quản lý lịch dạy, lớp học và điểm số</p>
        </div>

        <!-- Quick Actions -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <NuxtLink to="/websites/teacher-schedule" class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
                <div class="flex items-center">
                    <div class="p-3 bg-blue-100 rounded-full">
                        <IconCalendar class="w-8 h-8 text-blue-600" />
                    </div>
                    <div class="ml-4">
                        <h3 class="text-lg font-semibold text-gray-900">Lịch dạy</h3>
                        <p class="text-sm text-gray-600">Xem lịch dạy cá nhân</p>
                    </div>
                </div>
            </NuxtLink>

            <NuxtLink to="/websites/teacher-classes" class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
                <div class="flex items-center">
                    <div class="p-3 bg-green-100 rounded-full">
                        <IconUsers class="w-8 h-8 text-green-600" />
                    </div>
                    <div class="ml-4">
                        <h3 class="text-lg font-semibold text-gray-900">Lớp học</h3>
                        <p class="text-sm text-gray-600">Quản lý lớp phụ trách</p>
                    </div>
                </div>
            </NuxtLink>

            <NuxtLink to="/websites/teacher-grades" class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
                <div class="flex items-center">
                    <div class="p-3 bg-purple-100 rounded-full">
                        <IconAppraisal class="w-8 h-8 text-purple-600" />
                    </div>
                    <div class="ml-4">
                        <h3 class="text-lg font-semibold text-gray-900">Nhập điểm</h3>
                        <p class="text-sm text-gray-600">Nhập và quản lý điểm</p>
                    </div>
                </div>
            </NuxtLink>

            <NuxtLink to="/websites/teacher-notifications" class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
                <div class="flex items-center">
                    <div class="p-3 bg-orange-100 rounded-full">
                        <IconBulb class="w-8 h-8 text-orange-600" />
                    </div>
                    <div class="ml-4">
                        <h3 class="text-lg font-semibold text-gray-900">Thông báo</h3>
                        <p class="text-sm text-gray-600">Gửi thông báo cho sinh viên</p>
                    </div>
                </div>
            </NuxtLink>
        </div>

        <!-- Statistics Overview -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6 mb-8">
            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-blue-500">
                <div class="flex items-center">
                    <div class="p-3 bg-blue-100 rounded-full">
                        <IconCalendar class="w-8 h-8 text-blue-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Lớp đang dạy</p>
                        <p class="text-2xl font-bold text-gray-900">{{ teachingClasses }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-green-500">
                <div class="flex items-center">
                    <div class="p-3 bg-green-100 rounded-full">
                        <IconUsers class="w-8 h-8 text-green-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Tổng sinh viên</p>
                        <p class="text-2xl font-bold text-gray-900">{{ totalStudents }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-purple-500">
                <div class="flex items-center">
                    <div class="p-3 bg-purple-100 rounded-full">
                        <IconAppraisal class="w-8 h-8 text-purple-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Môn đang dạy</p>
                        <p class="text-2xl font-bold text-gray-900">{{ teachingSubjects }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-orange-500">
                <div class="flex items-center">
                    <div class="p-3 bg-orange-100 rounded-full">
                        <IconBulb class="w-8 h-8 text-orange-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Thông báo chưa đọc</p>
                        <p class="text-2xl font-bold text-gray-900">{{ unreadNotifications }}</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Today's Schedule -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- Today's Classes -->
            <div class="bg-white rounded-lg shadow-md">
                <div class="p-6 border-b border-gray-200">
                    <h3 class="text-lg font-semibold text-gray-900">Lịch dạy hôm nay</h3>
                </div>
                <div class="p-6">
                    <div class="space-y-4">
                        <div v-for="schedule in todaySchedule" :key="schedule.id" class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                            <div>
                                <p class="font-medium text-gray-900">{{ schedule.subject }}</p>
                                <p class="text-sm text-gray-600">{{ schedule.className }} - {{ schedule.time }}</p>
                                <p class="text-sm text-gray-500">{{ schedule.room }}</p>
                            </div>
                            <el-tag :type="getStatusType(schedule.status)">
                                {{ schedule.status }}
                            </el-tag>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Recent Notifications -->
            <div class="bg-white rounded-lg shadow-md">
                <div class="p-6 border-b border-gray-200">
                    <h3 class="text-lg font-semibold text-gray-900">Thông báo gần đây</h3>
                </div>
                <div class="p-6">
                    <div class="space-y-4">
                        <div v-for="notification in recentNotifications" :key="notification.id" class="flex items-start space-x-3">
                            <div class="flex-shrink-0">
                                <div class="w-2 h-2 bg-blue-500 rounded-full mt-2"></div>
                            </div>
                            <div class="flex-1">
                                <p class="text-sm font-medium text-gray-900">{{ notification.title }}</p>
                                <p class="text-xs text-gray-500">{{ notification.time }}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import IconCalendar from '@/assets/icons/calendar.svg'
import IconUsers from '@/assets/icons/users.svg'
import IconAppraisal from '@/assets/icons/appraisal.svg'
import IconBulb from '@/assets/icons/bulb.svg'

definePageMeta({
    layout: 'websites'
})

// Mock data for teacher dashboard
const teachingClasses = ref(4)
const totalStudents = ref(120)
const teachingSubjects = ref(3)
const unreadNotifications = ref(2)

const todaySchedule = ref([
    {
        id: 1,
        subject: 'Lập trình cơ bản',
        className: 'CNTT21A',
        time: '08:00-10:00',
        room: 'A101',
        status: 'Đang diễn ra'
    },
    {
        id: 2,
        subject: 'Cấu trúc dữ liệu',
        className: 'CNTT21B',
        time: '10:00-12:00',
        room: 'A102',
        status: 'Sắp tới'
    },
    {
        id: 3,
        subject: 'Phát triển phần mềm',
        className: 'CNTT22A',
        time: '14:00-16:00',
        room: 'B201',
        status: 'Sắp tới'
    }
])

const recentNotifications = ref([
    { id: 1, title: 'Thay đổi lịch học CNTT21A', time: '2 giờ trước' },
    { id: 2, title: 'Nhắc nhở nộp điểm giữa kỳ', time: '1 ngày trước' },
    { id: 3, title: 'Thông báo nghỉ bù ngày 15/01', time: '2 ngày trước' }
])

const getStatusType = (status: string) => {
    switch (status) {
        case 'Đang diễn ra': return 'success'
        case 'Sắp tới': return 'warning'
        case 'Đã kết thúc': return 'info'
        default: return 'danger'
    }
}
</script>

<style scoped>
.el-table {
    font-size: 14px;
}
</style>
