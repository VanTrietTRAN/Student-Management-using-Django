&lt;template>
  &lt;div class="p-6">
    &lt;!-- Page Header -->
    &lt;div class="mb-6">
      &lt;h1 class="text-2xl font-bold text-gray-900">{{ $t('Lịch học/thi') }}&lt;/h1>
    &lt;/div>

    &lt;!-- Schedule Type Tabs -->
    &lt;el-tabs v-model="activeTab" class="mb-6">
      &lt;el-tab-pane :label="$t('Lịch học')" name="class" />
      &lt;el-tab-pane :label="$t('Lịch thi')" name="exam" />
    &lt;/el-tabs>

    &lt;!-- Week Navigation -->
    &lt;div class="flex items-center justify-between mb-6">
      &lt;div class="flex items-center gap-4">
        &lt;el-button-group>
          &lt;el-button @click="previousWeek">
            &lt;el-icon>&lt;ArrowLeft />&lt;/el-icon>
          &lt;/el-button>
          &lt;el-button @click="nextWeek">
            &lt;el-icon>&lt;ArrowRight />&lt;/el-icon>
          &lt;/el-button>
        &lt;/el-button-group>
        &lt;el-button @click="currentWeek">{{ $t('Tuần này') }}&lt;/el-button>
      &lt;/div>
      &lt;div class="text-lg font-semibold text-gray-700">
        {{ weekRange }}
      &lt;/div>
    &lt;/div>

    &lt;!-- Weekly Schedule -->
    &lt;div v-if="activeTab === 'class'" class="bg-white rounded-lg shadow overflow-hidden">
      &lt;div class="grid grid-cols-6 gap-px bg-gray-200">
        &lt;!-- Time Column -->
        &lt;div class="bg-white p-2">
          &lt;div class="h-12 border-b border-gray-200 flex items-center justify-center font-semibold">
            {{ $t('Thời gian') }}
          &lt;/div>
          &lt;div v-for="slot in timeSlots" :key="slot" class="h-24 flex items-center justify-center text-sm text-gray-500">
            {{ slot }}
          &lt;/div>
        &lt;/div>

        &lt;!-- Day Columns -->
        &lt;div v-for="day in weekDays" :key="day.date" class="bg-white">
          &lt;div class="h-12 p-2 border-b border-gray-200">
            &lt;div class="text-center font-semibold">{{ day.name }}&lt;/div>
            &lt;div class="text-sm text-gray-500 text-center">{{ day.date }}&lt;/div>
          &lt;/div>
          &lt;div class="relative">
            &lt;div v-for="slot in timeSlots" :key="slot" class="h-24 border-b border-gray-100" />
            &lt;div
              v-for="class_ in getClassesForDay(day.date)"
              :key="class_.id"
              class="absolute left-0 right-0 mx-2 rounded-md overflow-hidden shadow-sm"
              :style="getClassStyle(class_)"
            >
              &lt;div
                class="p-2 h-full"
                :class="getClassColorClass(class_)"
              >
                &lt;div class="font-semibold text-sm">{{ class_.courseName }}&lt;/div>
                &lt;div class="text-xs">{{ class_.room }}&lt;/div>
                &lt;div class="text-xs">{{ class_.instructor }}&lt;/div>
              &lt;/div>
            &lt;/div>
          &lt;/div>
        &lt;/div>
      &lt;/div>
    &lt;/div>

    &lt;!-- Exam Schedule -->
    &lt;div v-else class="bg-white rounded-lg shadow">
      &lt;el-table :data="examSchedule" stripe>
        &lt;el-table-column prop="date" :label="$t('Ngày thi')" width="150">
          &lt;template #default="{ row }">
            {{ formatDate(row.date) }}
          &lt;/template>
        &lt;/el-table-column>
        &lt;el-table-column prop="time" :label="$t('Giờ thi')" width="120" />
        &lt;el-table-column prop="courseCode" :label="$t('Mã học phần')" width="150" />
        &lt;el-table-column prop="courseName" :label="$t('Tên học phần')" min-width="250" />
        &lt;el-table-column prop="room" :label="$t('Phòng thi')" width="120" />
        &lt;el-table-column prop="type" :label="$t('Hình thức thi')" width="150">
          &lt;template #default="{ row }">
            &lt;el-tag :type="getExamTypeTag(row.type)">{{ row.type }}&lt;/el-tag>
          &lt;/template>
        &lt;/el-table-column>
        &lt;el-table-column prop="notes" :label="$t('Ghi chú')" min-width="200" />
      &lt;/el-table>
    &lt;/div>
  &lt;/div>
&lt;/template>

&lt;script setup lang="ts">
import { ref, computed } from 'vue'
import { ArrowLeft, ArrowRight } from '@element-plus/icons-vue'
import dayjs from 'dayjs'
import 'dayjs/locale/vi'

dayjs.locale('vi')

const activeTab = ref('class')
const currentDate = ref(dayjs())

// Time slots for the schedule
const timeSlots = [
  '07:00 - 09:00',
  '09:10 - 11:10',
  '11:20 - 13:20',
  '13:30 - 15:30',
  '15:40 - 17:40'
]

// Calculate week days
const weekDays = computed(() => {
  const days = []
  for (let i = 0; i &lt; 5; i++) {
    const date = currentDate.value.startOf('week').add(i + 1, 'day')
    days.push({
      name: date.format('dddd'),
      date: date.format('DD/MM'),
      fullDate: date
    })
  }
  return days
})

// Format week range for display
const weekRange = computed(() => {
  const start = currentDate.value.startOf('week').add(1, 'day')
  const end = start.add(4, 'day')
  return `${start.format('DD/MM/YYYY')} - ${end.format('DD/MM/YYYY')}`
})

// Navigation functions
const previousWeek = () => {
  currentDate.value = currentDate.value.subtract(1, 'week')
}

const nextWeek = () => {
  currentDate.value = currentDate.value.add(1, 'week')
}

const currentWeek = () => {
  currentDate.value = dayjs()
}

// Sample class schedule data
const classes = [
  {
    id: 1,
    courseName: 'Web Programming',
    courseCode: 'INT3306',
    room: 'D3-201',
    instructor: 'Nguyễn Văn A',
    day: '15/01',
    startSlot: 0, // 0-based index of timeSlots
    duration: 2, // number of slots
    color: 'blue'
  },
  {
    id: 2,
    courseName: 'Database Systems',
    courseCode: 'INT3307',
    room: 'D3-203',
    instructor: 'Lê Văn C',
    day: '16/01',
    startSlot: 2,
    duration: 2,
    color: 'green'
  }
]

// Sample exam schedule data
const examSchedule = ref([
  {
    date: '2024-02-01',
    time: '08:00 - 10:00',
    courseCode: 'INT3306',
    courseName: 'Web Programming',
    room: 'D3-201',
    type: 'Trực tiếp',
    notes: 'Không được sử dụng tài liệu'
  },
  {
    date: '2024-02-03',
    time: '08:00 - 10:00',
    courseCode: 'INT3307',
    courseName: 'Database Systems',
    room: 'D3-203',
    type: 'Trực tuyến',
    notes: 'Được sử dụng tài liệu'
  }
])

// Helper functions
const getClassesForDay = (date: string) => {
  return classes.filter(c => c.day === date)
}

const getClassStyle = (class_: any) => {
  const top = class_.startSlot * 96 // 24px * 4 (height of time slot)
  const height = class_.duration * 96 - 4 // -4 for gap
  return {
    top: `${top}px`,
    height: `${height}px`
  }
}

const getClassColorClass = (class_: any) => {
  const colors = {
    blue: 'bg-blue-100 text-blue-900',
    green: 'bg-green-100 text-green-900',
    orange: 'bg-orange-100 text-orange-900',
    purple: 'bg-purple-100 text-purple-900'
  }
  return colors[class_.color as keyof typeof colors] || colors.blue
}

const getExamTypeTag = (type: string) => {
  switch (type) {
    case 'Trực tiếp':
      return 'danger'
    case 'Trực tuyến':
      return 'success'
    default:
      return 'info'
  }
}

const formatDate = (date: string) => {
  return dayjs(date).format('DD/MM/YYYY')
}
&lt;/script>

&lt;style scoped>
.el-table {
  @apply rounded-lg;
}
&lt;/style>