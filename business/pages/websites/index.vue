<template>
    <div class="min-h-screen bg-gray-50 pt-20 px-4 md:px-6 pb-6">
        <!-- Header Section -->
        <div class="mb-8">
            <h1 class="text-3xl font-bold text-gray-900 mb-2">Hệ thống thông tin sinh viên</h1>
            <p class="text-gray-600">Quản lý toàn bộ thông tin sinh viên, lớp học, điểm số và các hoạt động học tập</p>
        </div>

        <!-- Quick Actions -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <NuxtLink to="/websites/students" class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
                <div class="flex items-center">
                    <div class="p-3 bg-blue-100 rounded-full">
                        <IconUsers class="w-8 h-8 text-blue-600" />
                    </div>
                    <div class="ml-4">
                        <h3 class="text-lg font-semibold text-gray-900">Quản lý sinh viên</h3>
                        <p class="text-sm text-gray-600">Quản lý hồ sơ sinh viên</p>
                    </div>
                </div>
            </NuxtLink>

            <NuxtLink to="/websites/classes" class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
                <div class="flex items-center">
                    <div class="p-3 bg-green-100 rounded-full">
                        <IconCalendar class="w-8 h-8 text-green-600" />
                    </div>
                    <div class="ml-4">
                        <h3 class="text-lg font-semibold text-gray-900">Quản lý lớp học</h3>
                        <p class="text-sm text-gray-600">Quản lý lớp và phân công</p>
                    </div>
                </div>
            </NuxtLink>

            <NuxtLink to="/websites/subjects" class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
                <div class="flex items-center">
                    <div class="p-3 bg-purple-100 rounded-full">
                        <Document class="w-8 h-8 text-purple-600" />
                    </div>
                    <div class="ml-4">
                        <h3 class="text-lg font-semibold text-gray-900">Quản lý môn học</h3>
                        <p class="text-sm text-gray-600">Thiết lập môn học</p>
                    </div>
                </div>
            </NuxtLink>

            <NuxtLink to="/websites/grades" class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
                <div class="flex items-center">
                    <div class="p-3 bg-orange-100 rounded-full">
                        <IconAppraisal class="w-8 h-8 text-orange-600" />
                    </div>
                    <div class="ml-4">
                        <h3 class="text-lg font-semibold text-gray-900">Quản lý điểm số</h3>
                        <p class="text-sm text-gray-600">Nhập và quản lý điểm</p>
                    </div>
                </div>
            </NuxtLink>
        </div>

        <!-- Statistics Overview -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6 mb-8">
            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-blue-500">
                <div class="flex items-center">
                    <div class="p-3 bg-blue-100 rounded-full">
                        <IconUsers class="w-8 h-8 text-blue-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Tổng sinh viên</p>
                        <p class="text-2xl font-bold text-gray-900">{{ totalStudents }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-green-500">
                <div class="flex items-center">
                    <div class="p-3 bg-green-100 rounded-full">
                        <IconCalendar class="w-8 h-8 text-green-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Tổng lớp học</p>
                        <p class="text-2xl font-bold text-gray-900">{{ totalClasses }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-purple-500">
                <div class="flex items-center">
                    <div class="p-3 bg-purple-100 rounded-full">
                        <Document class="w-8 h-8 text-purple-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Tổng môn học</p>
                        <p class="text-2xl font-bold text-gray-900">{{ totalSubjects }}</p>
                    </div>
                </div>
          </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-orange-500">
                <div class="flex items-center">
                    <div class="p-3 bg-orange-100 rounded-full">
                        <IconAppraisal class="w-8 h-8 text-orange-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Điểm TB hệ thống</p>
                        <p class="text-2xl font-bold text-gray-900">{{ systemGPA }}</p>
                    </div>
                </div>
            </div>
          </div>

        <!-- Recent Activities -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
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

            <!-- Quick Stats -->
            <div class="bg-white rounded-lg shadow-md">
                <div class="p-6 border-b border-gray-200">
                    <h3 class="text-lg font-semibold text-gray-900">Thống kê nhanh</h3>
                </div>
                <div class="p-6">
                    <div class="space-y-4">
                        <div class="flex justify-between items-center">
                            <span class="text-sm text-gray-600">Sinh viên đang học</span>
                            <span class="text-sm font-semibold text-green-600">{{ activeStudents }}</span>
                        </div>
                        <div class="flex justify-between items-center">
                            <span class="text-sm text-gray-600">Lớp đang hoạt động</span>
                            <span class="text-sm font-semibold text-blue-600">{{ activeClasses }}</span>
                        </div>
                        <div class="flex justify-between items-center">
                            <span class="text-sm text-gray-600">Môn học đang mở</span>
                            <span class="text-sm font-semibold text-purple-600">{{ activeSubjects }}</span>
                        </div>
                        <div class="flex justify-between items-center">
                            <span class="text-sm text-gray-600">Học phí chưa thu</span>
                            <span class="text-sm font-semibold text-red-600">{{ unpaidTuition }}</span>
                        </div>
                    </div>
                </div>
          </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import IconUsers from '@/assets/icons/users.svg'
import IconCalendar from '@/assets/icons/calendar.svg'
import IconAppraisal from '@/assets/icons/appraisal.svg'
import { Document } from '@element-plus/icons-vue'

definePageMeta({
    layout: 'websites'
})

// Mock data for statistics
const totalStudents = ref(1250)
const totalClasses = ref(45)
const totalSubjects = ref(120)
const systemGPA = ref('8.2')
const activeStudents = ref(1180)
const activeClasses = ref(42)
const activeSubjects = ref(95)
const unpaidTuition = ref(85)

const recentNotifications = ref([
    { id: 1, title: 'Thông báo lịch thi cuối kỳ', time: '2 giờ trước' },
    { id: 2, title: 'Cập nhật học phí học kỳ mới', time: '1 ngày trước' },
    { id: 3, title: 'Thông báo nghỉ lễ 30/4', time: '3 ngày trước' },
    { id: 4, title: 'Kết quả xét học bổng', time: '1 tuần trước' }
])
</script>

<style scoped>
.el-table {
    font-size: 14px;
}
</style>