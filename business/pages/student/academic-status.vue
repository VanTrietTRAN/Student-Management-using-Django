<template>
  <div>
    <el-card class="mb-4">
      <template #header>
        <div class="flex justify-between items-center">
          <h2 class="text-lg font-semibold">Tình trạng học tập</h2>
          <el-button type="primary" @click="downloadReport">
            <el-icon class="mr-1"><Download /></el-icon>
            Tải báo cáo
          </el-button>
        </div>
      </template>

      <!-- Overall Status -->
      <div class="grid grid-cols-4 gap-4 mb-6">
        <el-card shadow="hover" class="text-center">
          <h3 class="text-lg font-medium mb-2">Trạng thái</h3>
          <el-tag :type="getStatusType(academicStatus.status)">
            {{ getStatusLabel(academicStatus.status) }}
          </el-tag>
        </el-card>

        <el-card shadow="hover" class="text-center">
          <h3 class="text-lg font-medium mb-2">GPA Tích lũy</h3>
          <div 
            class="text-2xl font-bold"
            :class="getGPAClass(academicStatus.cumulativeGPA)"
          >
            {{ academicStatus.cumulativeGPA }}
          </div>
        </el-card>

        <el-card shadow="hover" class="text-center">
          <h3 class="text-lg font-medium mb-2">Tín chỉ tích lũy</h3>
          <div class="text-2xl font-bold text-primary">
            {{ academicStatus.totalCredits }}/{{ academicStatus.requiredCredits }}
          </div>
        </el-card>

        <el-card shadow="hover" class="text-center">
          <h3 class="text-lg font-medium mb-2">Dự kiến tốt nghiệp</h3>
          <div class="text-xl font-medium" :class="getGraduationClass()">
            {{ academicStatus.expectedGraduation }}
          </div>
        </el-card>
      </div>

      <!-- Progress by Category -->
      <div class="mb-6">
        <h3 class="text-lg font-medium mb-4">Tiến độ theo nhóm môn học</h3>
        <el-table
          :data="creditsByCategory"
          style="width: 100%"
        >
          <el-table-column prop="category" label="Nhóm môn" min-width="200" />
          <el-table-column prop="completed" label="Đã hoàn thành" width="150">
            <template #default="{ row }">
              {{ row.completed }}/{{ row.required }} tín chỉ
            </template>
          </el-table-column>
          <el-table-column prop="progress" label="Tiến độ" width="300">
            <template #default="{ row }">
              <el-progress
                :percentage="(row.completed / row.required) * 100"
                :status="getProgressStatus(row.completed / row.required)"
              />
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- Academic Warnings -->
      <div v-if="academicWarnings.length" class="mb-6">
        <h3 class="text-lg font-medium mb-4">Cảnh báo học vụ</h3>
        <el-timeline>
          <el-timeline-item
            v-for="warning in academicWarnings"
            :key="warning.id"
            :type="warning.level"
            :color="getWarningColor(warning.level)"
            :timestamp="warning.date"
          >
            <el-card class="mb-4">
              <h4>{{ warning.title }}</h4>
              <p class="text-gray-600">{{ warning.description }}</p>
              <div class="mt-2">
                <el-tag size="small">{{ warning.semester }}</el-tag>
                <el-tag 
                  size="small" 
                  :type="warning.status === 'active' ? 'danger' : 'info'"
                  class="ml-2"
                >
                  {{ warning.status === 'active' ? 'Đang hiệu lực' : 'Đã hết hiệu lực' }}
                </el-tag>
              </div>
            </el-card>
          </el-timeline-item>
        </el-timeline>
      </div>

      <!-- Graduation Requirements -->
      <div>
        <h3 class="text-lg font-medium mb-4">Yêu cầu tốt nghiệp</h3>
        <el-collapse>
          <el-collapse-item title="Yêu cầu tín chỉ" name="1">
            <el-descriptions :column="2" border>
              <el-descriptions-item label="Tổng tín chỉ yêu cầu">
                {{ academicStatus.requiredCredits }}
              </el-descriptions-item>
              <el-descriptions-item label="Tổng tín chỉ đã đạt">
                {{ academicStatus.totalCredits }}
              </el-descriptions-item>
              <el-descriptions-item label="GPA tối thiểu">
                2.00
              </el-descriptions-item>
              <el-descriptions-item label="GPA hiện tại">
                <span :class="getGPAClass(academicStatus.cumulativeGPA)">
                  {{ academicStatus.cumulativeGPA }}
                </span>
              </el-descriptions-item>
            </el-descriptions>
          </el-collapse-item>

          <el-collapse-item title="Yêu cầu ngoại ngữ" name="2">
            <el-descriptions :column="1" border>
              <el-descriptions-item label="Yêu cầu">
                TOEIC 450+ hoặc tương đương
              </el-descriptions-item>
              <el-descriptions-item label="Trạng thái">
                <el-tag :type="academicStatus.englishRequirement ? 'success' : 'warning'">
                  {{ academicStatus.englishRequirement ? 'Đã đạt' : 'Chưa đạt' }}
                </el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="Chi tiết" v-if="academicStatus.englishDetails">
                {{ academicStatus.englishDetails }}
              </el-descriptions-item>
            </el-descriptions>
          </el-collapse-item>

          <el-collapse-item title="Các yêu cầu khác" name="3">
            <el-table :data="otherRequirements" style="width: 100%">
              <el-table-column prop="name" label="Yêu cầu" min-width="200" />
              <el-table-column prop="status" label="Trạng thái" width="150">
                <template #default="{ row }">
                  <el-tag :type="row.completed ? 'success' : 'warning'">
                    {{ row.completed ? 'Đã đạt' : 'Chưa đạt' }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="details" label="Chi tiết" min-width="200" />
            </el-table>
          </el-collapse-item>
        </el-collapse>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Download } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

// Mock data - replace with API calls
const academicStatus = ref({
  status: 'good',
  cumulativeGPA: '3.45',
  totalCredits: 90,
  requiredCredits: 120,
  expectedGraduation: '2026-05',
  englishRequirement: true,
  englishDetails: 'TOEIC: 650 (đạt ngày 15/09/2025)'
})

const creditsByCategory = ref([
  {
    category: 'Kiến thức đại cương',
    completed: 32,
    required: 35
  },
  {
    category: 'Cơ sở ngành',
    completed: 28,
    required: 40
  },
  {
    category: 'Chuyên ngành',
    completed: 25,
    required: 35
  },
  {
    category: 'Tự chọn',
    completed: 5,
    required: 10
  }
])

const academicWarnings = ref([
  {
    id: 1,
    level: 'warning',
    title: 'Cảnh báo học vụ lần 1',
    description: 'GPA học kỳ dưới 2.0',
    date: '2024-12-30',
    semester: 'HK1 2024-2025',
    status: 'resolved'
  }
])

const otherRequirements = ref([
  {
    name: 'Chứng chỉ GDQP-AN',
    completed: true,
    details: 'Hoàn thành ngày 20/08/2024'
  },
  {
    name: 'Chứng chỉ Giáo dục thể chất',
    completed: true,
    details: 'Hoàn thành ngày 15/12/2024'
  },
  {
    name: 'Hoạt động ngoại khóa',
    completed: false,
    details: 'Yêu cầu: 3 hoạt động - Đã tham gia: 1'
  }
])

// Methods
function getStatusType(status: string) {
  const types = {
    excellent: 'success',
    good: 'primary',
    warning: 'warning',
    probation: 'danger'
  }
  return types[status] || 'info'
}

function getStatusLabel(status: string) {
  const labels = {
    excellent: 'Xuất sắc',
    good: 'Tốt',
    warning: 'Cảnh báo',
    probation: 'Theo dõi đặc biệt'
  }
  return labels[status] || status
}

function getGPAClass(gpa: string) {
  const value = parseFloat(gpa)
  if (value >= 3.6) return 'text-success'
  if (value >= 3.2) return 'text-primary'
  if (value >= 2.5) return 'text-warning'
  return 'text-danger'
}

function getProgressStatus(progress: number) {
  if (progress >= 1) return 'success'
  if (progress >= 0.7) return ''
  if (progress >= 0.4) return 'warning'
  return 'exception'
}

function getWarningColor(level: string) {
  const colors = {
    warning: '#E6A23C',
    danger: '#F56C6C',
    info: '#909399'
  }
  return colors[level] || colors.info
}

function getGraduationClass() {
  const onTime = new Date(academicStatus.value.expectedGraduation) <= new Date('2026-06')
  return onTime ? 'text-success' : 'text-warning'
}

async function downloadReport() {
  try {
    // Implement report download functionality
    // await generateAcademicReport()
    ElMessage.success('Tải báo cáo thành công')
  } catch (error) {
    ElMessage.error('Tải báo cáo thất bại. Vui lòng thử lại.')
  }
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

.el-timeline :deep(.el-timeline-item__node) {
  size: 12px;
}
</style>