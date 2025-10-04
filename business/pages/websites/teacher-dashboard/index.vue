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
import { ref, onMounted } from 'vue'
import IconCalendar from '@/assets/icons/calendar.svg'
import IconUsers from '@/assets/icons/users.svg'
import IconAppraisal from '@/assets/icons/appraisal.svg'
import IconBulb from '@/assets/icons/bulb.svg'
import AcademicService from '@/services/websites/academic'

definePageMeta({ layout: 'websites' })

// State
const teachingClasses = ref<number | string>('—')
const totalStudents = ref<number | string>('—')
const teachingSubjects = ref<number | string>('—')
const unreadNotifications = ref<number | string>('—')

const todaySchedule = ref<any[]>([
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

const recentNotifications = ref<any[]>([])

onMounted(async () => {
    try {
        // classrooms (teachingClasses)
        try {
            const cRes = await AcademicService.getClassrooms({ page_size: 100 })
            const cData = cRes && cRes.data ? cRes.data : cRes
            teachingClasses.value = Array.isArray(cData) ? cData.length : (cData.count ?? '—')
        } catch (err) {
            console.warn('classrooms fetch failed', err)
            teachingClasses.value = 4
        }

        // students
        try {
            const sRes = await AcademicService.getStudents({ page_size: 1 })
            const sData = sRes && sRes.data ? sRes.data : sRes
            totalStudents.value = Array.isArray(sData) ? sData.length : (sData.count ?? 120)
        } catch (err) {
            console.warn('students fetch failed', err)
            totalStudents.value = 120
        }

        // subjects
        try {
            const subRes = await AcademicService.getSubjects({ page_size: 1 })
            const subData = subRes && subRes.data ? subRes.data : subRes
            teachingSubjects.value = Array.isArray(subData) ? subData.length : (subData.count ?? 3)
        } catch (err) {
            console.warn('subjects fetch failed', err)
            teachingSubjects.value = 3
        }

        // notifications
        try {
            const nRes = await AcademicService.getNotifications({ page_size: 5 })
            const nData = nRes && nRes.data ? nRes.data : nRes
            recentNotifications.value = Array.isArray(nData) ? nData : (nData.results || [])
            unreadNotifications.value = recentNotifications.value.filter((n:any) => !n.isRead).length
        } catch (err) {
            console.warn('notifications fetch failed', err)
            recentNotifications.value = [
                { id: 1, title: 'Thay đổi lịch học CNTT21A', time: '2 giờ trước' },
                { id: 2, title: 'Nhắc nhở nộp điểm giữa kỳ', time: '1 ngày trước' }
            ]
            unreadNotifications.value = 2
        }
    } catch (err) {
        console.error(err)
    }
})

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
