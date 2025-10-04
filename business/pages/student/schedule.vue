<template>
  <div class="schedule">
    <el-card class="schedule-card">
      <template #header>
        <div class="card-header">
          <span>{{ $t('Lịch học') }}</span>
          <el-radio-group v-model="viewMode" size="small">
            <el-radio-button label="week">{{ $t('Tuần') }}</el-radio-button>
            <el-radio-button label="month">{{ $t('Tháng') }}</el-radio-button>
          </el-radio-group>
        </div>
      </template>

      <!-- Calendar View -->
      <div class="calendar-view" v-if="viewMode === 'month'">
        <el-calendar v-model="selectedDate">
          <template #dateCell="{ data }">
            <div class="calendar-cell">
              <p :class="{ 'is-selected': data.isSelected }">
                {{ data.day.split('-').slice(2).join('') }}
              </p>
              <div class="calendar-events">
                <div 
                  v-for="event in getEventsForDate(data.day)" 
                  :key="event.id"
                  class="calendar-event"
                  :class="event.type"
                >
                  {{ event.title }}
                </div>
              </div>
            </div>
          </template>
        </el-calendar>
      </div>

      <!-- Weekly Schedule -->
      <div class="weekly-schedule" v-else>
        <div class="week-navigation">
          <el-button @click="previousWeek">
            <el-icon><ArrowLeft /></el-icon>
          </el-button>
          <span class="week-info">{{ weekDateRange }}</span>
          <el-button @click="nextWeek">
            <el-icon><ArrowRight /></el-icon>
          </el-button>
        </div>

        <el-table :data="weeklySchedule" style="width: 100%">
          <el-table-column prop="time" :label="$t('Thời gian')" width="120" />
          <el-table-column 
            v-for="day in weekDays" 
            :key="day.value"
            :label="day.label"
          >
            <template #default="{ row }">
              <div 
                v-for="classItem in getClassesForTimeAndDay(row.time, day.value)"
                :key="classItem.id"
                class="schedule-class"
                :class="classItem.type"
              >
                <div class="class-name">{{ classItem.courseName }}</div>
                <div class="class-room">{{ classItem.room }}</div>
                <div class="class-teacher">{{ classItem.teacher }}</div>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- Upcoming Events -->
      <div class="upcoming-events mt-4">
        <h3>{{ $t('Sự kiện sắp tới') }}</h3>
        <el-timeline>
          <el-timeline-item
            v-for="event in upcomingEvents"
            :key="event.id"
            :timestamp="event.time"
            :type="event.type"
          >
            <div class="event-card">
              <h4>{{ event.title }}</h4>
              <p>{{ event.description }}</p>
              <div class="event-location" v-if="event.location">
                <el-icon><Location /></el-icon>
                {{ event.location }}
              </div>
            </div>
          </el-timeline-item>
        </el-timeline>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ArrowLeft, ArrowRight, Location } from '@element-plus/icons-vue'
import { format, addWeeks, startOfWeek, endOfWeek } from 'date-fns'
import { vi } from 'date-fns/locale'

const viewMode = ref('week')
const selectedDate = ref(new Date())

// Weekly schedule data
const weeklySchedule = ref([
  { time: '07:00 - 09:00' },
  { time: '09:10 - 11:10' },
  { time: '13:00 - 15:00' },
  { time: '15:10 - 17:10' }
])

const weekDays = [
  { label: 'Thứ 2', value: 1 },
  { label: 'Thứ 3', value: 2 },
  { label: 'Thứ 4', value: 3 },
  { label: 'Thứ 5', value: 4 },
  { label: 'Thứ 6', value: 5 },
  { label: 'Thứ 7', value: 6 }
]

// Sample class data
const courseClasses = ref([
  {
    id: 1,
    courseName: 'Trí tuệ nhân tạo',
    teacher: 'Nguyễn Văn A',
    room: 'D9-301',
    day: 1, // Monday
    time: '07:00 - 09:00',
    type: 'lecture'
  },
  {
    id: 2,
    courseName: 'Lập trình Web',
    teacher: 'Trần Thị B',
    room: 'D9-405',
    day: 3, // Wednesday
    time: '13:00 - 15:00',
    type: 'practical'
  }
])

// Sample upcoming events
const upcomingEvents = ref([
  {
    id: 1,
    title: 'Kiểm tra giữa kỳ - Trí tuệ nhân tạo',
    description: 'Kiểm tra lý thuyết + Thực hành',
    time: '2025-10-15 09:00',
    location: 'D9-301',
    type: 'warning'
  },
  {
    id: 2,
    title: 'Deadline Project - Lập trình Web',
    description: 'Nộp báo cáo và source code',
    time: '2025-10-20 23:59',
    type: 'danger'
  }
])

// Navigation methods
const previousWeek = () => {
  selectedDate.value = addWeeks(selectedDate.value, -1)
}

const nextWeek = () => {
  selectedDate.value = addWeeks(selectedDate.value, 1)
}

// Computed properties
const weekDateRange = computed(() => {
  const start = startOfWeek(selectedDate.value, { weekStartsOn: 1 })
  const end = endOfWeek(selectedDate.value, { weekStartsOn: 1 })
  return `${format(start, 'dd/MM/yyyy', { locale: vi })} - ${format(end, 'dd/MM/yyyy', { locale: vi })}`
})

// Helper methods
const getClassesForTimeAndDay = (time: string, day: number) => {
  return courseClasses.value.filter(cls => cls.time === time && cls.day === day)
}

const getEventsForDate = (date: string) => {
  // Implementation for getting events for a specific date
  return []
}
</script>

<style scoped>
.schedule {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.week-navigation {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 20px;
  gap: 16px;
}

.week-info {
  font-size: 16px;
  font-weight: 500;
  min-width: 200px;
  text-align: center;
}

.schedule-class {
  padding: 8px;
  border-radius: 4px;
  margin-bottom: 4px;
}

.schedule-class.lecture {
  background-color: var(--el-color-primary-light-9);
  border-left: 4px solid var(--el-color-primary);
}

.schedule-class.practical {
  background-color: var(--el-color-success-light-9);
  border-left: 4px solid var(--el-color-success);
}

.class-name {
  font-weight: 500;
  margin-bottom: 4px;
}

.class-room, .class-teacher {
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.calendar-cell {
  height: 100%;
  padding: 4px;
}

.calendar-events {
  margin-top: 4px;
}

.calendar-event {
  font-size: 12px;
  padding: 2px 4px;
  margin-bottom: 2px;
  border-radius: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.event-card {
  padding: 12px;
  background-color: var(--el-bg-color-page);
  border-radius: 4px;
  box-shadow: var(--el-box-shadow-lighter);
}

.event-card h4 {
  margin: 0 0 8px;
}

.event-location {
  margin-top: 8px;
  font-size: 13px;
  color: var(--el-text-color-secondary);
  display: flex;
  align-items: center;
  gap: 4px;
}

.mt-4 {
  margin-top: 1rem;
}
</style>