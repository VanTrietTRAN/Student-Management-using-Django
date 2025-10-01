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
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import IconUsers from '@/assets/icons/users.svg'
import IconCalendar from '@/assets/icons/calendar.svg'
import IconAppraisal from '@/assets/icons/appraisal.svg'
import { Document } from '@element-plus/icons-vue'
import AcademicService from '@/services/websites/academic'

definePageMeta({ layout: 'websites' })

const totalStudents = ref<number | string>('—')
const totalClasses = ref<number | string>('—')
const totalSubjects = ref<number | string>('—')
const systemGPA = ref<number | string>('—')
const activeStudents = ref<number | string>('—')
const activeClasses = ref<number | string>('—')
const activeSubjects = ref<number | string>('—')
const unpaidTuition = ref<number | string>('—')

const recentNotifications = ref([
    { id: 1, title: 'Thông báo lịch thi cuối kỳ', time: '2 giờ trước' },
    { id: 2, title: 'Cập nhật học phí học kỳ mới', time: '1 ngày trước' },
    { id: 3, title: 'Thông báo nghỉ lễ 30/4', time: '3 ngày trước' },
    { id: 4, title: 'Kết quả xét học bổng', time: '1 tuần trước' }
])

onMounted(async () => {
    try {
        // students
        const sRes = await AcademicService.getStudents({ page_size: 1 })
        const sData = sRes && sRes.data ? sRes.data : sRes
        // If paginated
        totalStudents.value = Array.isArray(sData) ? sData.length : (sData.count ?? '—')

        // classrooms
        try {
            const cRes = await AcademicService.getClassrooms({ page_size: 1 })
            const cData = cRes && cRes.data ? cRes.data : cRes
            totalClasses.value = Array.isArray(cData) ? cData.length : (cData.count ?? '—')
        } catch (err) {
            console.warn('classrooms fetch failed', err)
            totalClasses.value = '—'
        }

        // subjects
        try {
            const subRes = await AcademicService.getSubjects({ page_size: 1 })
            const subData = subRes && subRes.data ? subRes.data : subRes
            totalSubjects.value = Array.isArray(subData) ? subData.length : (subData.count ?? '—')
        } catch (err) {
            console.warn('subjects fetch failed', err)
            totalSubjects.value = '—'
        }

        // system GPA - compute average from grades endpoint if available
        try {
            const gRes = await AcademicService.getGrades({ page_size: 1000 })
            const gData = gRes && gRes.data ? gRes.data : gRes
            const gradesList = Array.isArray(gData) ? gData : (gData.results || [])
            if (gradesList.length > 0) {
                const avg = gradesList.reduce((acc:any, g:any) => acc + (g.gpa || 0), 0) / gradesList.length
                systemGPA.value = avg.toFixed(2)
            } else {
                systemGPA.value = '—'
            }
        } catch (err) {
            console.warn('grades fetch failed', err)
            systemGPA.value = '—'
        }
    } catch (err) {
        ElMessage.error('Không thể tải số liệu hệ thống')
        console.error(err)
    }
})
</script>

<style scoped>
.el-table {
    font-size: 14px;
}
</style>