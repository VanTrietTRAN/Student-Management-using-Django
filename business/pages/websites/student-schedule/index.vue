<template>
    <div class="min-h-screen bg-gray-50 pt-20 px-4 md:px-6 pb-6">
        <!-- Header Section -->
        <div class="mb-8">
            <h1 class="text-3xl font-bold text-gray-900 mb-2">Lịch học của tôi</h1>
            <p class="text-gray-600">Xem lịch học và lịch thi theo tuần/tháng</p>
        </div>

        <!-- Filter Section -->
        <div class="bg-white rounded-lg shadow-md p-6 mb-6">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <el-select v-model="selectedWeek" placeholder="Chọn tuần" clearable>
                    <el-option label="Tuần này" value="current" />
                    <el-option label="Tuần tới" value="next" />
                    <el-option label="Tuần trước" value="previous" />
                </el-select>
                <el-select v-model="selectedType" placeholder="Chọn loại" clearable>
                    <el-option label="Tất cả" value="" />
                    <el-option label="Lịch học" value="study" />
                    <el-option label="Lịch thi" value="exam" />
                </el-select>
                <el-date-picker
                    v-model="selectedDate"
                    type="date"
                    placeholder="Chọn ngày"
                    clearable
                />
                <el-button type="primary" :icon="Search" @click="handleFilter">
                    Lọc kết quả
                </el-button>
            </div>
        </div>

        <!-- Schedule Overview -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6 mb-8">
            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-blue-500">
                <div class="flex items-center">
                    <div class="p-3 bg-blue-100 rounded-full">
                        <IconCalendar class="w-8 h-8 text-blue-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Lớp học hôm nay</p>
                        <p class="text-2xl font-bold text-gray-900">{{ todayClasses }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-green-500">
                <div class="flex items-center">
                    <div class="p-3 bg-green-100 rounded-full">
                        <IconCalendar class="w-8 h-8 text-green-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Lớp học tuần này</p>
                        <p class="text-2xl font-bold text-gray-900">{{ weekClasses }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-orange-500">
                <div class="flex items-center">
                    <div class="p-3 bg-orange-100 rounded-full">
                        <IconCalendar class="w-8 h-8 text-orange-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Lịch thi sắp tới</p>
                        <p class="text-2xl font-bold text-gray-900">{{ upcomingExams }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-purple-500">
                <div class="flex items-center">
                    <div class="p-3 bg-purple-100 rounded-full">
                        <IconUsers class="w-8 h-8 text-purple-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Tổng môn học</p>
                        <p class="text-2xl font-bold text-gray-900">{{ totalSubjects }}</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Weekly Schedule -->
        <div class="bg-white rounded-lg shadow-md mb-6">
            <div class="p-6 border-b border-gray-200">
                <h3 class="text-lg font-semibold text-gray-900">Lịch học tuần</h3>
            </div>
            <div class="p-6">
                <div class="grid grid-cols-7 gap-4">
                    <div v-for="day in weekDays" :key="day.name" class="text-center">
                        <div class="font-semibold text-gray-900 mb-2">{{ day.name }}</div>
                        <div class="space-y-2">
                            <div v-for="schedule in day.schedules" :key="schedule.id" 
                                 class="p-2 bg-gray-50 rounded text-xs"
                                 :class="getScheduleClass(schedule.type)">
                                <div class="font-medium">{{ schedule.subject }}</div>
                                <div class="text-gray-600">{{ schedule.time }}</div>
                                <div class="text-xs text-gray-500">{{ schedule.room }}</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Detailed Schedule Table -->
        <div class="bg-white rounded-lg shadow-md">
            <div class="p-6 border-b border-gray-200">
                <h3 class="text-lg font-semibold text-gray-900">Chi tiết lịch học</h3>
            </div>
            <div class="overflow-x-auto">
                <el-table :data="filteredSchedules" stripe style="width: 100%">
                    <el-table-column prop="date" label="Ngày" width="120" />
                    <el-table-column prop="time" label="Thời gian" width="120" />
                    <el-table-column prop="subject" label="Môn học" width="200" />
                    <el-table-column prop="type" label="Loại" width="100">
                        <template #default="scope">
                            <el-tag :type="getTypeColor(scope.row.type)">
                                {{ scope.row.type }}
                            </el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column prop="room" label="Phòng" width="100" />
                    <el-table-column prop="teacher" label="Giảng viên" width="180" />
                    <el-table-column prop="status" label="Trạng thái" width="120">
                        <template #default="scope">
                            <el-tag :type="getStatusType(scope.row.status)">
                                {{ scope.row.status }}
                            </el-tag>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import IconCalendar from '@/assets/icons/calendar.svg'
import IconUsers from '@/assets/icons/users.svg'
import AcademicService from '@/services/websites/academic'

definePageMeta({ layout: 'student' })

// Reactive data
const selectedWeek = ref('')
const selectedType = ref('')
const selectedDate = ref('')

// Stats
const todayClasses = ref(0)
const weekClasses = ref(0)
const upcomingExams = ref(0)
const totalSubjects = ref(0)

const schedules = ref<any[]>([])

const fallbackSchedules = [
    {
        id: 1,
        date: '2024-01-15',
        time: '08:00-10:00',
        subject: 'Lập trình cơ bản',
        type: 'Lịch học',
        room: 'A101',
        teacher: 'ThS. Nguyễn Văn A',
        status: 'Đang diễn ra'
    },
    {
        id: 2,
        date: '2024-01-15',
        time: '10:00-12:00',
        subject: 'Cấu trúc dữ liệu',
        type: 'Lịch học',
        room: 'A102',
        teacher: 'TS. Trần Thị B',
        status: 'Sắp tới'
    },
    {
        id: 3,
        date: '2024-01-20',
        time: '14:00-16:00',
        subject: 'Lập trình cơ bản',
        type: 'Lịch thi',
        room: 'A101',
        teacher: 'ThS. Nguyễn Văn A',
        status: 'Sắp tới'
    }
]

const weekDays = ref([
    { name: 'Thứ 2', schedules: [] },
    { name: 'Thứ 3', schedules: [] },
    { name: 'Thứ 4', schedules: [] },
    { name: 'Thứ 5', schedules: [] },
    { name: 'Thứ 6', schedules: [] },
    { name: 'Thứ 7', schedules: [] },
    { name: 'CN', schedules: [] }
])

// Computed properties
const filteredSchedules = computed(() => {
    let filtered = schedules.value
    if (selectedType.value) {
        const typeMap:any = { 'study': 'Lịch học', 'exam': 'Lịch thi' }
        filtered = filtered.filter(schedule => schedule.type === typeMap[selectedType.value])
    }
    return filtered
})

// Methods
const getStatusType = (status: string) => {
    switch (status) {
        case 'Đang diễn ra': return 'success'
        case 'Sắp tới': return 'warning'
        case 'Đã kết thúc': return 'info'
        default: return 'danger'
    }
}

const getTypeColor = (type: string) => {
    switch (type) {
        case 'Lịch học': return 'success'
        case 'Lịch thi': return 'danger'
        default: return 'info'
    }
}

const getScheduleClass = (type: string) => {
    switch (type) {
        case 'study': return 'bg-blue-50 border-blue-200'
        case 'exam': return 'bg-red-50 border-red-200'
        default: return 'bg-gray-50 border-gray-200'
    }
}

const handleFilter = () => { ElMessage.success('Lọc kết quả hoàn tất') }

onMounted(async () => {
    try {
        const res = await AcademicService.getSchedules({ page_size: 200 })
        const data = res && res.data ? res.data : res
        const list = Array.isArray(data) ? data : (data.results || [])
        if (list.length) {
            schedules.value = list
            const today = new Date().toISOString().split('T')[0]
            todayClasses.value = list.filter((s:any) => s.date === today).length
            weekClasses.value = list.length
            upcomingExams.value = list.filter((s:any) => (s.type || '').toLowerCase().includes('exam')).length
            totalSubjects.value = new Set(list.map((s:any) => s.subject)).size
        } else {
            schedules.value = fallbackSchedules
            todayClasses.value = 2
            weekClasses.value = 8
            upcomingExams.value = 3
            totalSubjects.value = 5
        }
    } catch (err) {
        console.warn('schedules fetch failed', err)
        schedules.value = fallbackSchedules
        todayClasses.value = 2
        weekClasses.value = 8
        upcomingExams.value = 3
        totalSubjects.value = 5
    }
})
</script>

<style scoped>
.el-table {
    font-size: 14px;
}
</style>
