<template>
  <div>
    <el-card class="mb-4">
      <template #header>
        <div class="flex justify-between items-center">
          <h2 class="text-lg font-semibold">Môn học đang theo học Học kỳ 1 - Năm học 2025-2026</h2>
          <div class="flex items-center space-x-4">
            <el-input
              v-model="searchQuery"
              placeholder="Tìm kiếm môn học..."
              prefix-icon="Search"
              clearable
              style="width: 300px"
            />
          </div>
        </div>
      </template>

      <!-- Progress Summary -->
      <div class="grid grid-cols-4 gap-4 mb-6">
        <el-card shadow="hover" class="text-center">
          <h3 class="text-lg font-medium mb-2">Tổng số môn</h3>
          <div class="text-2xl font-bold text-primary">{{ totalCourses }}</div>
        </el-card>

        <el-card shadow="hover" class="text-center">
          <h3 class="text-lg font-medium mb-2">Tổng tín chỉ</h3>
          <div class="text-2xl font-bold text-success">{{ totalCredits }}</div>
        </el-card>

        <el-card shadow="hover" class="text-center">
          <h3 class="text-lg font-medium mb-2">Điểm trung bình</h3>
          <div class="text-2xl font-bold text-warning">{{ averageGrade || 'N/A' }}</div>
        </el-card>

        <el-card shadow="hover" class="text-center">
          <h3 class="text-lg font-medium mb-2">Tiến độ học tập</h3>
          <el-progress
            :percentage="overallProgress"
            :status="getProgressStatus(overallProgress)"
          />
        </el-card>
      </div>

      <!-- Course List -->
      <el-table
        :data="filteredCourses"
        style="width: 100%"
      >
        <el-table-column type="expand">
          <template #default="props">
            <div class="p-4">
              <h4 class="font-medium mb-2">Thông tin chi tiết</h4>
              <el-descriptions :column="3" border>
                <el-descriptions-item label="Mã môn">
                  {{ props.row.courseCode }}
                </el-descriptions-item>
                <el-descriptions-item label="Số tín chỉ">
                  {{ props.row.credits }}
                </el-descriptions-item>
                <el-descriptions-item label="Loại môn">
                  {{ props.row.type }}
                </el-descriptions-item>
                <el-descriptions-item label="Tiến độ">
                  <el-progress :percentage="props.row.progress" />
                </el-descriptions-item>
                <el-descriptions-item label="Giảng viên">
                  {{ props.row.lecturer }}
                </el-descriptions-item>
                <el-descriptions-item label="Trạng thái">
                  <el-tag :type="getCourseStatusType(props.row.status)">
                    {{ getCourseStatusLabel(props.row.status) }}
                  </el-tag>
                </el-descriptions-item>
              </el-descriptions>

              <!-- Schedule -->
              <h4 class="font-medium mt-4 mb-2">Lịch học</h4>
              <el-table :data="props.row.schedule" border style="width: 100%">
                <el-table-column prop="day" label="Thứ" width="100" />
                <el-table-column prop="time" label="Giờ" width="150" />
                <el-table-column prop="room" label="Phòng" width="120" />
                <el-table-column prop="type" label="Loại" width="120">
                  <template #default="{ row }">
                    <el-tag size="small" :type="row.type === 'theory' ? 'primary' : 'success'">
                      {{ row.type === 'theory' ? 'Lý thuyết' : 'Thực hành' }}
                    </el-tag>
                  </template>
                </el-table-column>
              </el-table>

              <!-- Assignments -->
              <h4 class="font-medium mt-4 mb-2">Bài tập & Kiểm tra</h4>
              <el-table :data="props.row.assignments" border style="width: 100%">
                <el-table-column prop="name" label="Tên bài" min-width="200" />
                <el-table-column prop="dueDate" label="Hạn nộp" width="150">
                  <template #default="{ row }">
                    {{ formatDate(row.dueDate) }}
                  </template>
                </el-table-column>
                <el-table-column prop="weight" label="Trọng số" width="120">
                  <template #default="{ row }">
                    {{ row.weight }}%
                  </template>
                </el-table-column>
                <el-table-column prop="status" label="Trạng thái" width="150">
                  <template #default="{ row }">
                    <el-tag :type="getAssignmentStatusType(row.status)">
                      {{ getAssignmentStatusLabel(row.status) }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="grade" label="Điểm" width="100">
                  <template #default="{ row }">
                    {{ row.grade ?? 'N/A' }}
                  </template>
                </el-table-column>
              </el-table>

              <!-- Materials -->
              <h4 class="font-medium mt-4 mb-2">Tài liệu học tập</h4>
              <div class="grid grid-cols-2 gap-4">
                <div v-for="material in props.row.materials" :key="material.id"
                  class="p-3 border rounded-lg hover:bg-gray-50 cursor-pointer"
                  @click="downloadMaterial(material)"
                >
                  <div class="flex items-center">
                    <el-icon class="mr-2"><Document /></el-icon>
                    <div class="flex-1">
                      <div class="font-medium">{{ material.name }}</div>
                      <div class="text-xs text-gray-500">
                        {{ formatFileSize(material.size) }} - Cập nhật: {{ formatDate(material.updatedAt) }}
                      </div>
                    </div>
                    <el-button link type="primary" :icon="Download" />
                  </div>
                </div>
              </div>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="name" label="Tên môn học" min-width="300">
          <template #default="{ row }">
            <div>
              <div class="font-medium">{{ row.name }}</div>
              <div class="text-xs text-gray-500">
                Mã môn: {{ row.courseCode }} | {{ row.credits }} tín chỉ
              </div>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="progress" label="Tiến độ" width="200">
          <template #default="{ row }">
            <el-progress :percentage="row.progress" />
          </template>
        </el-table-column>

        <el-table-column prop="grade" label="Điểm hiện tại" width="150">
          <template #default="{ row }">
            <span :class="getGradeClass(row.grade)">
              {{ row.grade ?? 'N/A' }}
            </span>
          </template>
        </el-table-column>

        <el-table-column prop="status" label="Trạng thái" width="150">
          <template #default="{ row }">
            <el-tag :type="getCourseStatusType(row.status)">
              {{ getCourseStatusLabel(row.status) }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column fixed="right" label="Thao tác" width="150">
          <template #default="{ row }">
            <el-button-group>
              <el-button
                type="primary"
                :icon="List"
                circle
                @click="viewAssignments(row)"
              />
              <el-button
                type="success"
                :icon="Document"
                circle
                @click="viewMaterials(row)"
              />
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- Assignment Details Dialog -->
    <el-dialog
      v-if="selectedCourse"
      v-model="showAssignmentsDialog"
      :title="`Bài tập & Kiểm tra - ${selectedCourse.name}`"
      width="800px"
    >
      <el-table :data="selectedCourse.assignments" border style="width: 100%">
        <el-table-column prop="name" label="Tên bài" min-width="200" />
        <el-table-column prop="dueDate" label="Hạn nộp" width="150">
          <template #default="{ row }">
            {{ formatDate(row.dueDate) }}
          </template>
        </el-table-column>
        <el-table-column prop="weight" label="Trọng số" width="120">
          <template #default="{ row }">
            {{ row.weight }}%
          </template>
        </el-table-column>
        <el-table-column prop="status" label="Trạng thái" width="150">
          <template #default="{ row }">
            <el-tag :type="getAssignmentStatusType(row.status)">
              {{ getAssignmentStatusLabel(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="grade" label="Điểm" width="100">
          <template #default="{ row }">
            {{ row.grade ?? 'N/A' }}
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>

    <!-- Materials Dialog -->
    <el-dialog
      v-if="selectedCourse"
      v-model="showMaterialsDialog"
      :title="`Tài liệu học tập - ${selectedCourse.name}`"
      width="800px"
    >
      <div class="grid grid-cols-1 gap-4">
        <div v-for="material in selectedCourse.materials" :key="material.id"
          class="p-4 border rounded-lg hover:bg-gray-50 cursor-pointer"
          @click="downloadMaterial(material)"
        >
          <div class="flex items-center">
            <el-icon class="mr-3" :size="24"><Document /></el-icon>
            <div class="flex-1">
              <div class="font-medium">{{ material.name }}</div>
              <div class="text-sm text-gray-500">
                {{ formatFileSize(material.size) }} - Cập nhật: {{ formatDate(material.updatedAt) }}
              </div>
            </div>
            <el-button type="primary" :icon="Download">Tải xuống</el-button>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { format } from 'date-fns'
import { vi } from 'date-fns/locale'
import { 
  Document,
  Download,
  List
} from '@element-plus/icons-vue'

// State
const searchQuery = ref('')
const showAssignmentsDialog = ref(false)
const showMaterialsDialog = ref(false)
const selectedCourse = ref(null)

// Mock data - replace with API calls
const courses = ref([
  {
    id: 1,
    courseCode: 'IT001',
    name: 'Lập trình Web',
    credits: 3,
    type: 'Bắt buộc',
    lecturer: 'Nguyễn Văn A',
    progress: 45,
    grade: 8.5,
    status: 'in_progress',
    schedule: [
      {
        day: 'Thứ 2',
        time: '07:30 - 09:30',
        room: 'A1.01',
        type: 'theory'
      },
      {
        day: 'Thứ 4',
        time: '13:30 - 15:30',
        room: 'Lab 1',
        type: 'practice'
      }
    ],
    assignments: [
      {
        id: 1,
        name: 'Bài tập 1: HTML & CSS',
        dueDate: '2025-10-10',
        weight: 20,
        status: 'submitted',
        grade: 9.0
      },
      {
        id: 2,
        name: 'Bài tập 2: JavaScript',
        dueDate: '2025-10-20',
        weight: 30,
        status: 'pending',
        grade: null
      }
    ],
    materials: [
      {
        id: 1,
        name: 'Slide bài giảng tuần 1',
        size: 2500000,
        updatedAt: '2025-10-01',
        url: '#'
      },
      {
        id: 2,
        name: 'Tài liệu thực hành Lab 1',
        size: 1500000,
        updatedAt: '2025-10-02',
        url: '#'
      }
    ]
  },
  // Add more courses
])

// Computed
const filteredCourses = computed(() => {
  if (!searchQuery.value) return courses.value

  const query = searchQuery.value.toLowerCase()
  return courses.value.filter(course =>
    course.name.toLowerCase().includes(query) ||
    course.courseCode.toLowerCase().includes(query)
  )
})

const totalCourses = computed(() => courses.value.length)
const totalCredits = computed(() => 
  courses.value.reduce((sum, course) => sum + course.credits, 0)
)
const averageGrade = computed(() => {
  const coursesWithGrades = courses.value.filter(c => c.grade !== null)
  if (!coursesWithGrades.length) return null
  
  const sum = coursesWithGrades.reduce((total, course) => total + course.grade, 0)
  return (sum / coursesWithGrades.length).toFixed(2)
})
const overallProgress = computed(() => {
  return Math.round(
    courses.value.reduce((sum, course) => sum + course.progress, 0) / courses.value.length
  )
})

// Methods
function formatDate(date: string) {
  return format(new Date(date), 'dd/MM/yyyy', { locale: vi })
}

function formatFileSize(bytes: number) {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

function getProgressStatus(value: number) {
  if (value >= 80) return 'success'
  if (value >= 60) return 'warning'
  return 'exception'
}

function getCourseStatusType(status: string) {
  const types = {
    not_started: 'info',
    in_progress: 'success',
    at_risk: 'warning',
    completed: 'primary'
  }
  return types[status] || 'info'
}

function getCourseStatusLabel(status: string) {
  const labels = {
    not_started: 'Chưa bắt đầu',
    in_progress: 'Đang học',
    at_risk: 'Cần chú ý',
    completed: 'Đã hoàn thành'
  }
  return labels[status] || status
}

function getAssignmentStatusType(status: string) {
  const types = {
    pending: 'warning',
    submitted: 'success',
    late: 'danger',
    graded: 'info'
  }
  return types[status] || 'info'
}

function getAssignmentStatusLabel(status: string) {
  const labels = {
    pending: 'Chưa nộp',
    submitted: 'Đã nộp',
    late: 'Nộp trễ',
    graded: 'Đã chấm'
  }
  return labels[status] || status
}

function getGradeClass(grade: number | null) {
  if (grade === null) return 'text-gray-400'
  if (grade >= 8.5) return 'text-success font-bold'
  if (grade >= 7) return 'text-primary font-bold'
  if (grade >= 5) return 'text-warning font-bold'
  return 'text-danger font-bold'
}

function viewAssignments(course: any) {
  selectedCourse.value = course
  showAssignmentsDialog.value = true
}

function viewMaterials(course: any) {
  selectedCourse.value = course
  showMaterialsDialog.value = true
}

function downloadMaterial(material: any) {
  // Implement download functionality
  console.log('Downloading material:', material.name)
}
</script>

<style scoped>
.text-primary {
  color: var(--el-color-primary);
}

.text-success {
  color: var(--el-color-success);
}

.text-warning {
  color: var(--el-color-warning);
}

.text-danger {
  color: var(--el-color-danger);
}

.el-card :deep(.el-card__header) {
  padding: 12px 20px;
}
</style>