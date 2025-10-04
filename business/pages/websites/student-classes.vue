<template>
  <div class="p-6">
    <!-- Page Header -->
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-900">{{ $t('Lớp học') }}</h1>
    </div>

    <!-- Class Information Tabs -->
    <el-tabs v-model="activeTab" class="mb-6">
      <el-tab-pane :label="$t('Lớp khóa học')" name="class" />
      <el-tab-pane :label="$t('Lớp học phần')" name="course" />
    </el-tabs>

    <!-- Study Class Info -->
    <div v-if="activeTab === 'class'" class="space-y-6">
      <!-- Main Class Card -->
      <el-card class="w-full">
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-xl font-bold mb-2">K65-Công nghệ thông tin 2</h2>
            <div class="flex gap-4 text-gray-600">
              <div>
                <span class="font-semibold">{{ $t('Khóa học') }}:</span> K65 (2021-2025)
              </div>
              <div>
                <span class="font-semibold">{{ $t('Sĩ số') }}:</span> 45
              </div>
              <div>
                <span class="font-semibold">{{ $t('GVCN') }}:</span> TS. Nguyễn Văn A
              </div>
            </div>
          </div>
          <el-button type="primary" @click="showClassmates = true">
            {{ $t('Xem danh sách lớp') }}
          </el-button>
        </div>
      </el-card>

      <!-- Class Statistics -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <el-card class="text-center">
          <h3 class="text-lg font-semibold mb-2">{{ $t('Điểm TB lớp') }}</h3>
          <p class="text-3xl font-bold text-primary-600">3.42</p>
        </el-card>

        <el-card class="text-center">
          <h3 class="text-lg font-semibold mb-2">{{ $t('Xếp hạng') }}</h3>
          <p class="text-3xl font-bold text-success-600">15/45</p>
        </el-card>

        <el-card class="text-center">
          <h3 class="text-lg font-semibold mb-2">{{ $t('Tín chỉ tích lũy') }}</h3>
          <p class="text-3xl font-bold text-warning-600">90/150</p>
        </el-card>

        <el-card class="text-center">
          <h3 class="text-lg font-semibold mb-2">{{ $t('Điểm rèn luyện') }}</h3>
          <p class="text-3xl font-bold text-info-600">85</p>
        </el-card>
      </div>

      <!-- Class Events -->
      <el-card>
        <template #header>
          <div class="flex items-center justify-between">
            <span class="font-bold">{{ $t('Hoạt động lớp') }}</span>
            <el-button type="primary" plain>{{ $t('Xem tất cả') }}</el-button>
          </div>
        </template>
        <el-timeline>
          <el-timeline-item
            v-for="event in classEvents"
            :key="event.id"
            :timestamp="event.time"
            :type="event.type"
          >
            {{ event.content }}
          </el-timeline-item>
        </el-timeline>
      </el-card>
    </div>

    <!-- Course Classes -->
    <div v-else>
      <el-table :data="courseClasses" stripe>
        <el-table-column type="expand">
          <template #default="props">
            <div class="p-4">
              <h4 class="font-bold mb-4">{{ $t('Thông tin chi tiết') }}:</h4>
              <el-descriptions :column="3" border>
                <el-descriptions-item :label="$t('Mã lớp')">
                  {{ props.row.classCode }}
                </el-descriptions-item>
                <el-descriptions-item :label="$t('Phòng học')">
                  {{ props.row.room }}
                </el-descriptions-item>
                <el-descriptions-item :label="$t('Sĩ số')">
                  {{ props.row.enrolled }}/{{ props.row.capacity }}
                </el-descriptions-item>
                <el-descriptions-item :label="$t('Lịch học')">
                  {{ props.row.schedule }}
                </el-descriptions-item>
                <el-descriptions-item :label="$t('Giảng viên')">
                  {{ props.row.instructor }}
                </el-descriptions-item>
                <el-descriptions-item :label="$t('Trạng thái')">
                  <el-tag :type="props.row.status === 'Đang học' ? 'success' : 'info'">
                    {{ props.row.status }}
                  </el-tag>
                </el-descriptions-item>
              </el-descriptions>

              <h4 class="font-bold mt-6 mb-4">{{ $t('Điểm quá trình') }}:</h4>
              <el-table :data="props.row.grades" border>
                <el-table-column prop="type" :label="$t('Loại điểm')" width="200" />
                <el-table-column prop="weight" :label="$t('Trọng số')" width="120" />
                <el-table-column prop="score" :label="$t('Điểm số')" width="120" />
                <el-table-column prop="date" :label="$t('Ngày cập nhật')" width="150" />
                <el-table-column prop="note" :label="$t('Ghi chú')" min-width="200" />
              </el-table>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="courseCode" :label="$t('Mã học phần')" width="150" />
        <el-table-column prop="courseName" :label="$t('Tên học phần')" min-width="300" />
        <el-table-column prop="schedule" :label="$t('Lịch học')" width="200" />
        <el-table-column prop="instructor" :label="$t('Giảng viên')" width="200" />
        <el-table-column prop="status" :label="$t('Trạng thái')" width="120">
          <template #default="{ row }">
            <el-tag :type="row.status === 'Đang học' ? 'success' : 'info'">
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- Classmates Dialog -->
    <el-dialog
      v-model="showClassmates"
      :title="$t('Danh sách lớp')"
      width="80%"
    >
      <el-table :data="classmates" stripe>
        <el-table-column prop="studentId" :label="$t('Mã sinh viên')" width="150" />
        <el-table-column prop="name" :label="$t('Họ và tên')" min-width="200" />
        <el-table-column prop="email" :label="$t('Email')" min-width="250" />
        <el-table-column prop="phone" :label="$t('Số điện thoại')" width="150" />
        <el-table-column prop="status" :label="$t('Trạng thái')" width="120">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const activeTab = ref('class')
const showClassmates = ref(false)

// Sample class events data
const classEvents = ref([
  {
    id: 1,
    content: 'Họp lớp tháng 1/2024',
    time: '20/01/2024 14:00',
    type: 'primary'
  },
  {
    id: 2,
    content: 'Nộp báo cáo rèn luyện học kỳ 1',
    time: '15/01/2024 23:59',
    type: 'warning'
  },
  {
    id: 3,
    content: 'Sinh hoạt lớp đầu kỳ',
    time: '08/01/2024 09:00',
    type: 'success'
  }
])

// Sample course classes data
const courseClasses = ref([
  {
    courseCode: 'INT3306',
    courseName: 'Web Programming',
    classCode: '123456',
    schedule: 'Thứ 2 (1-3), Thứ 4 (1-3)',
    room: 'D3-201',
    instructor: 'Nguyễn Văn A',
    enrolled: 45,
    capacity: 50,
    status: 'Đang học',
    grades: [
      {
        type: 'Chuyên cần',
        weight: '10%',
        score: '9.0',
        date: '15/01/2024',
        note: 'Đi học đầy đủ'
      },
      {
        type: 'Bài tập',
        weight: '20%',
        score: '8.5',
        date: '10/01/2024',
        note: 'Nộp đúng hạn'
      }
    ]
  },
  {
    courseCode: 'INT3307',
    courseName: 'Database Systems',
    classCode: '123457',
    schedule: 'Thứ 3 (1-3), Thứ 5 (1-3)',
    room: 'D3-202',
    instructor: 'Trần Thị B',
    enrolled: 48,
    capacity: 50,
    status: 'Đang học',
    grades: [
      {
        type: 'Giữa kỳ',
        weight: '30%',
        score: '8.0',
        date: '12/01/2024',
        note: ''
      }
    ]
  }
])

// Sample classmates data
const classmates = ref([
  {
    studentId: '20020001',
    name: 'Nguyễn Văn X',
    email: 'x.nv20020001@sis.hust.edu.vn',
    phone: '0123456789',
    status: 'Đang học'
  },
  {
    studentId: '20020002',
    name: 'Trần Thị Y',
    email: 'y.tt20020002@sis.hust.edu.vn',
    phone: '0123456788',
    status: 'Đang học'
  },
  {
    studentId: '20020003',
    name: 'Lê Văn Z',
    email: 'z.lv20020003@sis.hust.edu.vn',
    phone: '0123456787',
    status: 'Bảo lưu'
  }
])

const getStatusType = (status: string) => {
  switch (status) {
    case 'Đang học':
      return 'success'
    case 'Bảo lưu':
      return 'warning'
    case 'Thôi học':
      return 'danger'
    default:
      return 'info'
  }
}
</script>

<style scoped>
.el-card {
  @apply rounded-lg;
}

.el-table {
  @apply rounded-lg;
}
</style>