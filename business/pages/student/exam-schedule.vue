<template>
  <div>
    <el-card class="mb-4">
      <template #header>
        <div class="flex justify-between items-center">
          <h2 class="text-lg font-semibold">Lịch thi Học kỳ 1 - Năm học 2025-2026</h2>
          <div class="flex items-center space-x-4">
            <el-input
              v-model="searchQuery"
              placeholder="Tìm kiếm môn thi..."
              prefix-icon="Search"
              clearable
            />
          </div>
        </div>
      </template>

      <el-table
        :data="filteredExams"
        style="width: 100%"
        :default-sort="{ prop: 'date', order: 'ascending' }"
      >
        <el-table-column prop="subject" label="Môn thi" min-width="200">
          <template #default="{ row }">
            <div>
              <div class="font-medium">{{ row.subject }}</div>
              <div class="text-xs text-gray-500">Mã môn: {{ row.courseCode }}</div>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="date" label="Ngày thi" width="150" sortable>
          <template #default="{ row }">
            {{ formatDate(row.date) }}
          </template>
        </el-table-column>
        
        <el-table-column prop="time" label="Giờ thi" width="120">
          <template #default="{ row }">
            {{ formatTime(row.startTime) }} - {{ formatTime(row.endTime) }}
          </template>
        </el-table-column>
        
        <el-table-column prop="room" label="Phòng thi" width="120" />
        
        <el-table-column prop="type" label="Hình thức" width="150">
          <template #default="{ row }">
            <el-tag :type="getExamType(row.type).type" size="small">
              {{ getExamType(row.type).label }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="status" label="Trạng thái" width="150">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)" size="small">
              {{ getStatusLabel(row.status) }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column fixed="right" label="Thao tác" width="120">
          <template #default="{ row }">
            <el-button 
              link 
              type="primary" 
              :disabled="!canRegisterRetake(row)"
              @click="handleRegisterRetake(row)"
            >
              {{ getActionButtonLabel(row) }}
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- Registration Dialog -->
    <el-dialog
      v-model="showRegistrationDialog"
      title="Đăng ký thi lại"
      width="500px"
      :destroy-on-close="true"
    >
      <template #default>
        <template v-if="selectedExam">
          <div class="space-y-4">
            <div class="text-lg font-medium mb-4">
              {{ selectedExam.subject }}
            </div>
            
            <div class="grid grid-cols-2 gap-4">
              <div>
                <div class="text-sm text-gray-500">Ngày thi</div>
                <div>{{ formatDate(selectedExam.date) }}</div>
              </div>
              
              <div>
                <div class="text-sm text-gray-500">Giờ thi</div>
                <div>{{ formatTime(selectedExam.startTime) }} - {{ formatTime(selectedExam.endTime) }}</div>
              </div>
              
              <div>
                <div class="text-sm text-gray-500">Phòng thi</div>
                <div>{{ selectedExam.room }}</div>
              </div>
              
              <div>
                <div class="text-sm text-gray-500">Hình thức</div>
                <div>{{ getExamType(selectedExam.type).label }}</div>
              </div>
            </div>

            <div class="mt-4">
              <div class="text-sm text-gray-500 mb-2">Lệ phí thi lại</div>
              <div class="text-lg font-medium text-primary">
                {{ formatCurrency(selectedExam.retakeFee) }}
              </div>
            </div>

            <el-alert
              v-if="selectedExam.notes"
              :title="selectedExam.notes"
              type="warning"
              :closable="false"
              class="mt-4"
            />
          </div>
        </template>
      </template>

      <template #footer>
        <div class="flex justify-end space-x-3">
          <el-button @click="showRegistrationDialog = false">Hủy</el-button>
          <el-button 
            v-if="selectedExam" 
            type="primary" 
            @click="confirmRegistration"
          >
            Xác nhận đăng ký
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { format } from 'date-fns'
import { vi } from 'date-fns/locale'
import { ElMessage, ElMessageBox } from 'element-plus'

// Types
interface Exam {
  id: number
  subject: string
  courseCode: string
  date: string
  startTime: string
  endTime: string
  room: string
  type: string
  status: string
  retakeFee: number
  notes: string | null
}

// State
const searchQuery = ref('')
const showRegistrationDialog = ref(false)
const selectedExam = ref<Exam | null>(null)

// Mock data - replace with API calls
const examsList = ref([
  {
    id: 1,
    subject: 'Lập trình Web',
    courseCode: 'IT001',
    date: '2025-10-15',
    startTime: '07:30',
    endTime: '09:30',
    room: 'A1.01',
    type: 'final',
    status: 'scheduled',
    retakeFee: 200000,
    notes: 'Mang theo thẻ sinh viên và bút'
  },
  {
    id: 2,
    subject: 'Cơ sở dữ liệu',
    courseCode: 'IT002',
    date: '2025-10-17',
    startTime: '09:30',
    endTime: '11:30',
    room: 'A2.02',
    type: 'midterm',
    status: 'registered',
    retakeFee: 150000,
    notes: null
  },
  // Add more exams as needed
])

// Computed
const filteredExams = computed(() => {
  if (!searchQuery.value) return examsList.value
  
  const query = searchQuery.value.toLowerCase()
  return examsList.value.filter(exam => 
    exam.subject.toLowerCase().includes(query) ||
    exam.courseCode.toLowerCase().includes(query)
  )
})

// Methods
function getExamType(type: string) {
  const types = {
    final: { label: 'Thi cuối kỳ', type: 'danger' },
    midterm: { label: 'Giữa kỳ', type: 'warning' },
    retake: { label: 'Thi lại', type: 'info' },
    makeup: { label: 'Thi bù', type: 'success' }
  }
  return types[type] || { label: type, type: 'info' }
}

function getStatusType(status: string) {
  const types = {
    scheduled: 'info',
    registered: 'success',
    completed: 'warning',
    missed: 'danger'
  }
  return types[status] || 'info'
}

function getStatusLabel(status: string) {
  const labels = {
    scheduled: 'Đã lên lịch',
    registered: 'Đã đăng ký',
    completed: 'Đã thi',
    missed: 'Vắng thi'
  }
  return labels[status] || status
}

function formatDate(date: string) {
  return format(new Date(date), 'EEEE, dd/MM/yyyy', { locale: vi })
}

function formatTime(time: string) {
  return time
}

function formatCurrency(amount: number) {
  return new Intl.NumberFormat('vi-VN', {
    style: 'currency',
    currency: 'VND'
  }).format(amount)
}

function canRegisterRetake(exam: Exam) {
  return exam.type === 'retake' && exam.status === 'scheduled'
}

function getActionButtonLabel(exam: Exam) {
  if (exam.status === 'registered') return 'Chi tiết'
  if (exam.type === 'retake' && exam.status === 'scheduled') return 'Đăng ký'
  return 'Xem'
}

function handleRegisterRetake(exam: Exam) {
  if (exam.type === 'retake' && exam.status === 'scheduled') {
    selectedExam.value = exam
    showRegistrationDialog.value = true
  } else {
    // Show exam details
    selectedExam.value = exam
    showRegistrationDialog.value = true
  }
}

async function confirmRegistration() {
  try {
    await ElMessageBox.confirm(
      'Bạn có chắc chắn muốn đăng ký thi lại môn này?',
      'Xác nhận đăng ký',
      {
        confirmButtonText: 'Xác nhận',
        cancelButtonText: 'Hủy',
        type: 'warning'
      }
    )

    // Call API to register for retake exam
    // await registerRetakeExam(selectedExam.value.id)

    // Update local state
    const index = examsList.value.findIndex(e => e.id === selectedExam.value.id)
    if (index !== -1) {
      examsList.value[index].status = 'registered'
    }

    ElMessage.success('Đăng ký thi lại thành công')
    showRegistrationDialog.value = false
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('Đăng ký thi lại thất bại. Vui lòng thử lại.')
    }
  }
}
</script>

<style scoped>
.el-card :deep(.el-card__header) {
  padding: 12px 20px;
}

.text-primary {
  color: var(--el-color-primary);
}
</style>