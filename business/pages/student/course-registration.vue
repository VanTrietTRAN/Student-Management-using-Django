<template>
  <div>
    <el-card class="mb-4">
      <template #header>
        <div class="flex justify-between items-center">
          <div>
            <h2 class="text-lg font-semibold">Đăng ký môn học Học kỳ 1 - Năm học 2025-2026</h2>
            <p class="text-sm text-gray-500">
              Thời gian đăng ký: 01/10/2025 - 15/10/2025
            </p>
          </div>
          <el-button type="primary" @click="showCart">
            <el-icon><ShoppingCart /></el-icon>
            Môn học đã chọn ({{ selectedCourses.length }})
          </el-button>
        </div>
      </template>

      <!-- Filters -->
      <div class="mb-4 flex items-center space-x-4">
        <el-input
          v-model="searchQuery"
          placeholder="Tìm kiếm môn học..."
          prefix-icon="Search"
          style="width: 300px"
          clearable
        />
        <el-select v-model="selectedDepartment" placeholder="Khoa/Ngành" clearable>
          <el-option
            v-for="dept in departments"
            :key="dept.value"
            :label="dept.label"
            :value="dept.value"
          />
        </el-select>
        <el-checkbox v-model="showAvailableOnly">
          Chỉ hiện môn còn slot
        </el-checkbox>
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
                <el-descriptions-item label="Điều kiện tiên quyết">
                  {{ props.row.prerequisites?.join(', ') || 'Không' }}
                </el-descriptions-item>
                <el-descriptions-item label="Học phí">
                  {{ formatCurrency(props.row.fee) }}
                </el-descriptions-item>
                <el-descriptions-item label="Trạng thái">
                  <el-tag :type="getStatusType(props.row.status)">
                    {{ getStatusLabel(props.row.status) }}
                  </el-tag>
                </el-descriptions-item>
              </el-descriptions>

              <h4 class="font-medium mt-4 mb-2">Lịch học</h4>
              <el-table :data="props.row.schedule" border style="width: 100%">
                <el-table-column prop="day" label="Thứ" width="100" />
                <el-table-column prop="time" label="Giờ" width="150" />
                <el-table-column prop="room" label="Phòng" width="120" />
                <el-table-column prop="lecturer" label="Giảng viên" min-width="200" />
                <el-table-column prop="type" label="Loại" width="120">
                  <template #default="{ row }">
                    <el-tag size="small" :type="row.type === 'theory' ? 'primary' : 'success'">
                      {{ row.type === 'theory' ? 'Lý thuyết' : 'Thực hành' }}
                    </el-tag>
                  </template>
                </el-table-column>
              </el-table>
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

        <el-table-column prop="lecturer" label="Giảng viên" min-width="200" />

        <el-table-column prop="slots" label="Slot" width="150">
          <template #default="{ row }">
            <div class="text-center">
              <div>{{ row.registeredSlots }}/{{ row.totalSlots }}</div>
              <el-progress
                :percentage="(row.registeredSlots / row.totalSlots) * 100"
                :status="getSlotStatus(row)"
              />
            </div>
          </template>
        </el-table-column>

        <el-table-column fixed="right" label="Thao tác" width="120">
          <template #default="{ row }">
            <el-button
              :type="isSelected(row) ? 'danger' : 'primary'"
              :icon="isSelected(row) ? 'Delete' : 'Plus'"
              circle
              @click="toggleCourse(row)"
              :disabled="!canRegister(row)"
            />
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- Shopping Cart Dialog -->
    <el-dialog
      v-model="showCartDialog"
      title="Môn học đã chọn"
      width="800px"
    >
      <el-table :data="selectedCourses" style="width: 100%">
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

        <el-table-column prop="fee" label="Học phí" width="150">
          <template #default="{ row }">
            {{ formatCurrency(row.fee) }}
          </template>
        </el-table-column>

        <el-table-column fixed="right" label="Thao tác" width="120">
          <template #default="{ row }">
            <el-button
              type="danger"
              icon="Delete"
              circle
              @click="toggleCourse(row)"
            />
          </template>
        </el-table-column>
      </el-table>

      <div class="mt-4 flex justify-between items-center">
        <div>
          <div class="text-lg font-medium">Tổng học phí:</div>
          <div class="text-xl text-primary font-bold">
            {{ formatCurrency(totalFee) }}
          </div>
        </div>
        <el-button type="primary" @click="confirmRegistration" :disabled="!selectedCourses.length">
          Xác nhận đăng ký
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessageBox, ElMessage } from 'element-plus'
import { ShoppingCart } from '@element-plus/icons-vue'

// State
const searchQuery = ref('')
const selectedDepartment = ref('')
const showAvailableOnly = ref(false)
const showCartDialog = ref(false)
const selectedCourses = ref([])

// Mock data - replace with API calls
const courses = ref([
  {
    id: 1,
    courseCode: 'IT001',
    name: 'Lập trình Web',
    credits: 3,
    type: 'Bắt buộc',
    lecturer: 'Nguyễn Văn A',
    department: 'it',
    prerequisites: ['IT000'],
    fee: 1500000,
    totalSlots: 40,
    registeredSlots: 35,
    status: 'available',
    schedule: [
      {
        day: 'Thứ 2',
        time: '07:30 - 09:30',
        room: 'A1.01',
        lecturer: 'Nguyễn Văn A',
        type: 'theory'
      },
      {
        day: 'Thứ 4',
        time: '13:30 - 15:30',
        room: 'Lab 1',
        lecturer: 'Nguyễn Văn A',
        type: 'practice'
      }
    ]
  },
  // Add more courses
])

const departments = ref([
  { label: 'Công nghệ thông tin', value: 'it' },
  { label: 'Kỹ thuật phần mềm', value: 'se' },
  { label: 'Khoa học máy tính', value: 'cs' },
  // Add more departments
])

// Computed
const filteredCourses = computed(() => {
  let result = courses.value

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(course =>
      course.name.toLowerCase().includes(query) ||
      course.courseCode.toLowerCase().includes(query) ||
      course.lecturer.toLowerCase().includes(query)
    )
  }

  if (selectedDepartment.value) {
    result = result.filter(course => course.department === selectedDepartment.value)
  }

  if (showAvailableOnly.value) {
    result = result.filter(course => course.registeredSlots < course.totalSlots)
  }

  return result
})

const totalFee = computed(() => {
  return selectedCourses.value.reduce((total, course) => total + course.fee, 0)
})

// Methods
function formatCurrency(amount: number) {
  return new Intl.NumberFormat('vi-VN', {
    style: 'currency',
    currency: 'VND'
  }).format(amount)
}

function getStatusType(status: string) {
  const types = {
    available: 'success',
    full: 'danger',
    pending: 'warning',
    registered: 'info'
  }
  return types[status] || 'info'
}

function getStatusLabel(status: string) {
  const labels = {
    available: 'Có thể đăng ký',
    full: 'Hết slot',
    pending: 'Đang xử lý',
    registered: 'Đã đăng ký'
  }
  return labels[status] || status
}

function getSlotStatus(course: any) {
  const percentage = (course.registeredSlots / course.totalSlots) * 100
  if (percentage >= 100) return 'exception'
  if (percentage >= 80) return 'warning'
  return 'success'
}

function isSelected(course: any) {
  return selectedCourses.value.some(c => c.id === course.id)
}

function canRegister(course: any) {
  return course.registeredSlots < course.totalSlots && !isSelected(course)
}

function toggleCourse(course: any) {
  const index = selectedCourses.value.findIndex(c => c.id === course.id)
  if (index === -1) {
    selectedCourses.value.push(course)
    ElMessage.success(`Đã thêm môn ${course.name} vào danh sách đăng ký`)
  } else {
    selectedCourses.value.splice(index, 1)
    ElMessage.warning(`Đã xóa môn ${course.name} khỏi danh sách đăng ký`)
  }
}

function showCart() {
  showCartDialog.value = true
}

async function confirmRegistration() {
  try {
    await ElMessageBox.confirm(
      `Bạn có chắc chắn muốn đăng ký ${selectedCourses.value.length} môn học đã chọn?`,
      'Xác nhận đăng ký',
      {
        confirmButtonText: 'Xác nhận',
        cancelButtonText: 'Hủy',
        type: 'warning'
      }
    )

    // Call API to register courses
    // await registerCourses(selectedCourses.value.map(c => c.id))

    ElMessage.success('Đăng ký môn học thành công')
    selectedCourses.value = []
    showCartDialog.value = false
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('Đăng ký môn học thất bại. Vui lòng thử lại.')
    }
  }
}
</script>

<style scoped>
.text-primary {
  color: var(--el-color-primary);
}

.el-card :deep(.el-card__header) {
  padding: 12px 20px;
}
</style>