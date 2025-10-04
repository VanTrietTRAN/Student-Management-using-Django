<template>
    <div class="min-h-screen bg-gray-50 pt-32 px-4 md:px-6 pb-6">
        <!-- Header Section -->
        <div class="mb-8">
            <h1 class="text-3xl font-bold text-gray-900 mb-2">Dashboard Sinh viên</h1>
            <p class="text-gray-600">Thông tin cá nhân, lịch học và điểm số</p>
        </div>

        <!-- Quick Actions -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <NuxtLink to="/websites/student-profile" class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow block">
                <div class="flex items-center">
                    <span class="p-3 bg-blue-100 rounded-full">
                        <IconUsers class="w-8 h-8 text-blue-600" />
                    </span>
                    <div class="ml-4">
                        <h3 class="text-lg font-semibold text-gray-900">Thông tin cá nhân</h3>
                        <p class="text-sm text-gray-600">Xem và cập nhật thông tin</p>
                    </div>
                </div>
            </NuxtLink>

            <NuxtLink to="/websites/student-grades" class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
                <div class="flex items-center">
                    <div class="p-3 bg-green-100 rounded-full">
                        <IconAppraisal class="w-8 h-8 text-green-600" />
                    </div>
                    <div class="ml-4">
                        <h3 class="text-lg font-semibold text-gray-900">Điểm số</h3>
                        <p class="text-sm text-gray-600">Xem điểm các môn học</p>
                    </div>
                </div>
            </NuxtLink>

            <NuxtLink to="/websites/student-schedule" class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
                <div class="flex items-center">
                    <div class="p-3 bg-purple-100 rounded-full">
                        <IconCalendar class="w-8 h-8 text-purple-600" />
                    </div>
                    <div class="ml-4">
                        <h3 class="text-lg font-semibold text-gray-900">Lịch học</h3>
                        <p class="text-sm text-gray-600">Xem lịch học và thi</p>
                    </div>
                </div>
            </NuxtLink>

            <NuxtLink to="/websites/student-tuition" class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
                <div class="flex items-center">
                    <div class="p-3 bg-orange-100 rounded-full">
                        <IconFile class="w-8 h-8 text-orange-600" />
                    </div>
                    <div class="ml-4">
                        <h3 class="text-lg font-semibold text-gray-900">Học phí</h3>
                        <p class="text-sm text-gray-600">Xem và thanh toán học phí</p>
                    </div>
                </div>
            </NuxtLink>
        </div>

        <!-- Student Info Card -->
        <div class="bg-white rounded-lg shadow-md p-6 mb-8">
            <div class="flex items-center space-x-6">
                <div class="flex-shrink-0">
                    <img 
                        :src="studentInfo.profilePicture || '/default-avatar.png'" 
                        :alt="studentInfo.fullName"
                        class="w-20 h-20 rounded-full object-cover"
                    />
                </div>
                <div class="flex-1">
                    <h2 class="text-2xl font-bold text-gray-900">{{ studentInfo.fullName }}</h2>
                    <p class="text-lg text-gray-600">{{ studentInfo.studentId }} - {{ studentInfo.classroom }}</p>
                    <p class="text-sm text-gray-500">{{ studentInfo.major }} | GPA: {{ studentInfo.gpa }}</p>
                </div>
                <div class="text-right">
                    <el-tag :type="getStatusType(studentInfo.status)" size="large">
                        {{ studentInfo.status }}
                    </el-tag>
                </div>
            </div>
        </div>

        <!-- Statistics Overview -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6 mb-8">
            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-blue-500">
                <div class="flex items-center">
                    <div class="p-3 bg-blue-100 rounded-full">
                        <IconAppraisal class="w-8 h-8 text-blue-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Điểm TB</p>
                        <p class="text-2xl font-bold text-gray-900">{{ studentInfo.gpa }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-green-500">
                <div class="flex items-center">
                    <div class="p-3 bg-green-100 rounded-full">
                        <IconCalendar class="w-8 h-8 text-green-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Môn đang học</p>
                        <p class="text-2xl font-bold text-gray-900">{{ currentSubjects }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-purple-500">
                <div class="flex items-center">
                    <div class="p-3 bg-purple-100 rounded-full">
                        <IconFile class="w-8 h-8 text-purple-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Học phí còn lại</p>
                        <p class="text-2xl font-bold text-gray-900">{{ formatCurrency(remainingTuition) }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-orange-500">
                <div class="flex items-center">
                    <div class="p-3 bg-orange-100 rounded-full">
                        <IconBulb class="w-8 h-8 text-orange-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Thông báo mới</p>
                        <p class="text-2xl font-bold text-gray-900">{{ newNotifications }}</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Today's Schedule & Recent Grades -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- Today's Schedule -->
            <div class="bg-white rounded-lg shadow-md">
                <div class="p-6 border-b border-gray-200">
                    <h3 class="text-lg font-semibold text-gray-900">Lịch học hôm nay</h3>
                </div>
                <div class="p-6">
                    <div class="space-y-4">
                        <div v-for="schedule in todaySchedule" :key="schedule.id" class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                            <div>
                                <p class="font-medium text-gray-900">{{ schedule.subject }}</p>
                                <p class="text-sm text-gray-600">{{ schedule.time }} - {{ schedule.room }}</p>
                                <p class="text-sm text-gray-500">{{ schedule.teacher }}</p>
                            </div>
                            <el-tag :type="getStatusType(schedule.status)">
                                {{ schedule.status }}
                            </el-tag>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Recent Grades -->
            <div class="bg-white rounded-lg shadow-md">
                <div class="p-6 border-b border-gray-200">
                    <h3 class="text-lg font-semibold text-gray-900">Điểm gần đây</h3>
                </div>
                <div class="p-6">
                    <div class="space-y-4">
                        <div v-for="grade in recentGrades" :key="grade.id" class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                            <div>
                                <p class="font-medium text-gray-900">{{ grade.subject }}</p>
                                <p class="text-sm text-gray-600">{{ grade.semester }}</p>
                            </div>
                            <div class="text-right">
                                <p class="text-lg font-bold" :class="getGPAClass(grade.gpa)">
                                    {{ grade.gpa }}
                                </p>
                                <p class="text-xs text-gray-500">{{ grade.status }}</p>
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
import { ElMessage } from 'element-plus'
import IconUsers from '@/assets/icons/users.svg'
import IconAppraisal from '@/assets/icons/appraisal.svg'
import IconCalendar from '@/assets/icons/calendar.svg'
import IconFile from '@/assets/icons/file.svg'
import IconBulb from '@/assets/icons/bulb.svg'
import AcademicService from '@/services/websites/academic'
import { useOauthStore } from '@/stores/oauth'

definePageMeta({ layout: 'websites' })

// Reactive state
const studentInfo = ref<any>({ fullName: '', studentId: '', classroom: '', major: '', gpa: 0, status: '', profilePicture: null })
const currentSubjects = ref(0)
const remainingTuition = ref(0)
const newNotifications = ref(0)
const todaySchedule = ref<any[]>([])
const recentGrades = ref<any[]>([])

const oauth = useOauthStore()

const formatCurrency = (amount: number) => new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(amount)

const getStatusType = (status: string) => {
    switch (status) {
        case 'Đang diễn ra': return 'success'
        case 'Sắp tới': return 'warning'
        case 'Đã kết thúc': return 'info'
        case 'Đang học': return 'success'
        default: return 'danger'
    }
}

const getGPAClass = (gpa: number) => {
    if (gpa >= 8.0) return 'text-green-600'
    if (gpa >= 6.5) return 'text-blue-600'
    if (gpa >= 5.0) return 'text-yellow-600'
    return 'text-red-600'
}

onMounted(async () => {
    const userId = oauth.userId
    if (!userId) return

    try {
        const sRes = await AcademicService.getStudent(userId)
        const sData = sRes && sRes.data ? sRes.data : sRes
        studentInfo.value = sData || studentInfo.value

        // grades
        try {
            const gRes = await AcademicService.getGrades({ student: userId })
            const gData = gRes && gRes.data ? gRes.data : gRes
            recentGrades.value = Array.isArray(gData) ? gData.slice(0,5) : (gData.results || []).slice(0,5)
        } catch (err) {
            console.warn('grades fetch failed', err)
        }

        // tuitions
        try {
            const tRes = await AcademicService.getTuitions({ student: userId })
            const tData = tRes && tRes.data ? tRes.data : tRes
            const tList = Array.isArray(tData) ? tData : (tData.results || [])
            remainingTuition.value = tList.reduce((sum:any, t:any) => sum + ((t.amount || 0) - (t.paid_amount || 0)), 0)
        } catch (err) {
            console.warn('tuitions fetch failed', err)
        }
    } catch (err) {
        ElMessage.error('Không thể tải dashboard sinh viên')
        console.error(err)
    }
})
</script>

<style scoped>
.el-table {
    font-size: 14px;
}
</style>
