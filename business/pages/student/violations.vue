<template>
  <div>
    <el-card class="mb-4">
      <template #header>
        <div class="flex justify-between items-center">
          <h2 class="text-lg font-semibold">Vi phạm & Kỷ luật</h2>
          <div class="flex items-center space-x-4">
            <el-select v-model="selectedYear" placeholder="Chọn năm học">
              <el-option
                v-for="year in academicYears"
                :key="year.value"
                :label="year.label"
                :value="year.value"
              />
            </el-select>
          </div>
        </div>
      </template>

      <!-- Summary Cards -->
      <div class="grid grid-cols-4 gap-4 mb-6">
        <el-card shadow="hover" class="text-center">
          <h3 class="text-lg font-medium mb-2">Tổng số vi phạm</h3>
          <div class="text-2xl font-bold" :class="getViolationCountClass(totalViolations)">
            {{ totalViolations }}
          </div>
        </el-card>

        <el-card shadow="hover" class="text-center">
          <h3 class="text-lg font-medium mb-2">Vi phạm nghiêm trọng</h3>
          <div class="text-2xl font-bold text-danger">
            {{ seriousViolations }}
          </div>
        </el-card>

        <el-card shadow="hover" class="text-center">
          <h3 class="text-lg font-medium mb-2">Điểm trừ tích lũy</h3>
          <div class="text-2xl font-bold" :class="getPenaltyPointsClass(totalPenaltyPoints)">
            -{{ totalPenaltyPoints }}
          </div>
        </el-card>

        <el-card shadow="hover" class="text-center">
          <h3 class="text-lg font-medium mb-2">Trạng thái</h3>
          <el-tag :type="getStatusType(currentStatus)">
            {{ getStatusLabel(currentStatus) }}
          </el-tag>
        </el-card>
      </div>

      <!-- Active Disciplinary Actions -->
      <div v-if="activeActions.length" class="mb-6">
        <h3 class="text-lg font-medium mb-4">Kỷ luật đang hiệu lực</h3>
        <el-alert
          v-for="action in activeActions"
          :key="action.id"
          :title="action.title"
          :description="action.description"
          :type="action.type"
          :closable="false"
          class="mb-4"
        >
          <template #default>
            <div class="mt-2">
              <div class="text-sm">
                Thời hạn: {{ formatDate(action.startDate) }} - {{ formatDate(action.endDate) }}
              </div>
              <div class="text-sm">
                Quyết định số: {{ action.decisionNumber }}
              </div>
            </div>
          </template>
        </el-alert>
      </div>

      <!-- Violations List -->
      <div>
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-medium">Danh sách vi phạm</h3>
          <el-input
            v-model="searchQuery"
            placeholder="Tìm kiếm..."
            prefix-icon="Search"
            style="width: 300px"
            clearable
          />
        </div>

        <el-table
          :data="filteredViolations"
          style="width: 100%"
        >
          <el-table-column type="expand">
            <template #default="props">
              <div class="p-4">
                <el-descriptions :column="2" border>
                  <el-descriptions-item label="Mã quyết định">
                    {{ props.row.decisionNumber }}
                  </el-descriptions-item>
                  <el-descriptions-item label="Ngày quyết định">
                    {{ formatDate(props.row.decisionDate) }}
                  </el-descriptions-item>
                  <el-descriptions-item label="Người ký">
                    {{ props.row.signedBy }}
                  </el-descriptions-item>
                  <el-descriptions-item label="Đơn vị xử lý">
                    {{ props.row.department }}
                  </el-descriptions-item>
                </el-descriptions>

                <div class="mt-4">
                  <h4 class="font-medium mb-2">Chi tiết vi phạm</h4>
                  <p class="text-gray-600 whitespace-pre-line">{{ props.row.details }}</p>
                </div>

                <div v-if="props.row.consequences" class="mt-4">
                  <h4 class="font-medium mb-2">Hình thức xử lý</h4>
                  <ul class="list-disc list-inside space-y-1 text-gray-600">
                    <li v-for="(item, index) in props.row.consequences" :key="index">
                      {{ item }}
                    </li>
                  </ul>
                </div>

                <div v-if="props.row.remedial" class="mt-4">
                  <h4 class="font-medium mb-2">Biện pháp khắc phục</h4>
                  <ul class="list-disc list-inside space-y-1 text-gray-600">
                    <li v-for="(item, index) in props.row.remedial" :key="index">
                      {{ item }}
                    </li>
                  </ul>
                </div>

                <div v-if="props.row.attachments?.length" class="mt-4">
                  <h4 class="font-medium mb-2">Tài liệu đính kèm</h4>
                  <div class="space-y-2">
                    <div
                      v-for="file in props.row.attachments"
                      :key="file.id"
                      class="flex items-center space-x-2 p-2 border rounded hover:bg-gray-50 cursor-pointer"
                      @click="downloadAttachment(file)"
                    >
                      <el-icon><Document /></el-icon>
                      <span>{{ file.name }}</span>
                      <span class="text-gray-400 text-sm">({{ formatFileSize(file.size) }})</span>
                    </div>
                  </div>
                </div>
              </div>
            </template>
          </el-table-column>

          <el-table-column prop="date" label="Thời gian" width="150" sortable>
            <template #default="{ row }">
              {{ formatDate(row.date) }}
            </template>
          </el-table-column>

          <el-table-column prop="violation" label="Vi phạm" min-width="300">
            <template #default="{ row }">
              <div>
                <div class="font-medium">{{ row.violation }}</div>
                <div class="text-xs text-gray-500">{{ row.category }}</div>
              </div>
            </template>
          </el-table-column>

          <el-table-column prop="severity" label="Mức độ" width="150">
            <template #default="{ row }">
              <el-tag :type="getSeverityType(row.severity)">
                {{ getSeverityLabel(row.severity) }}
              </el-tag>
            </template>
          </el-table-column>

          <el-table-column prop="penaltyPoints" label="Điểm trừ" width="120" align="center">
            <template #default="{ row }">
              <span class="text-danger">-{{ row.penaltyPoints }}</span>
            </template>
          </el-table-column>

          <el-table-column prop="status" label="Trạng thái" width="150">
            <template #default="{ row }">
              <el-tag :type="getViolationStatusType(row.status)">
                {{ getViolationStatusLabel(row.status) }}
              </el-tag>
            </template>
          </el-table-column>

          <el-table-column fixed="right" label="Thao tác" width="120">
            <template #default="{ row }">
              <el-button
                type="primary"
                :icon="Document"
                circle
                @click="viewDetails(row)"
              />
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- Statistics Charts -->
      <div class="mt-6 grid grid-cols-2 gap-6">
        <div>
          <h3 class="text-lg font-medium mb-4">Phân loại vi phạm</h3>
          <!-- Add pie chart for violation categories -->
          <el-table :data="violationStats" style="width: 100%">
            <el-table-column prop="category" label="Loại" min-width="200" />
            <el-table-column prop="count" label="Số lượng" width="120" align="center" />
            <el-table-column prop="points" label="Điểm trừ" width="120" align="center">
              <template #default="{ row }">
                <span class="text-danger">-{{ row.points }}</span>
              </template>
            </el-table-column>
          </el-table>
        </div>
        <div>
          <h3 class="text-lg font-medium mb-4">Diễn biến theo thời gian</h3>
          <!-- Add line chart for violation trend -->
          <el-table :data="violationTrend" style="width: 100%">
            <el-table-column prop="month" label="Tháng" width="120" />
            <el-table-column prop="count" label="Số vi phạm" width="120" align="center" />
            <el-table-column prop="trend" label="Xu hướng" min-width="200">
              <template #default="{ row }">
                <el-progress
                  :percentage="row.percentage"
                  :status="row.trend === 'increase' ? 'exception' : 'success'"
                />
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { format } from 'date-fns'
import { vi } from 'date-fns/locale'
import { Document } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

// State
const selectedYear = ref('2025-2026')
const searchQuery = ref('')

// Mock data - replace with API calls
const academicYears = ref([
  { label: 'Năm học 2025-2026', value: '2025-2026' },
  { label: 'Năm học 2024-2025', value: '2024-2025' }
])

const violations = ref([
  {
    id: 1,
    date: '2025-10-01',
    violation: 'Vắng học không phép',
    category: 'Vi phạm quy chế học tập',
    severity: 'minor',
    penaltyPoints: 2,
    status: 'processed',
    decisionNumber: 'QD456/2025',
    decisionDate: '2025-10-02',
    signedBy: 'TS. Nguyễn Văn B',
    department: 'Phòng Công tác Sinh viên',
    details: 'Vắng học không phép 3 buổi liên tiếp môn Lập trình Web',
    consequences: [
      'Trừ 2 điểm rèn luyện',
      'Nhắc nhở và cảnh báo'
    ],
    remedial: [
      'Viết bản kiểm điểm',
      'Cam kết không tái phạm'
    ],
    attachments: [
      {
        id: 1,
        name: 'Biên bản vi phạm.pdf',
        size: 1200000,
        url: '#'
      }
    ]
  }
])

const activeActions = ref([
  {
    id: 1,
    title: 'Cảnh cáo',
    description: 'Vi phạm quy chế học tập nhiều lần',
    type: 'warning',
    startDate: '2025-09-01',
    endDate: '2025-12-31',
    decisionNumber: 'QD789/2025'
  }
])

const violationStats = ref([
  {
    category: 'Vi phạm quy chế học tập',
    count: 3,
    points: 6
  },
  {
    category: 'Vi phạm nội quy',
    count: 2,
    points: 4
  },
  {
    category: 'Vi phạm kỷ luật',
    count: 1,
    points: 5
  }
])

const violationTrend = ref([
  {
    month: '10/2025',
    count: 2,
    percentage: 20,
    trend: 'decrease'
  },
  {
    month: '09/2025',
    count: 3,
    percentage: 30,
    trend: 'increase'
  },
  {
    month: '08/2025',
    count: 1,
    percentage: 10,
    trend: 'decrease'
  }
])

// Computed
const filteredViolations = computed(() => {
  let result = violations.value

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(violation =>
      violation.violation.toLowerCase().includes(query) ||
      violation.category.toLowerCase().includes(query) ||
      violation.decisionNumber?.toLowerCase().includes(query)
    )
  }

  return result.filter(violation => violation.date.startsWith(selectedYear.value.split('-')[0]))
})

const totalViolations = computed(() => violations.value.length)
const seriousViolations = computed(() => 
  violations.value.filter(v => v.severity === 'serious').length
)
const totalPenaltyPoints = computed(() =>
  violations.value.reduce((sum, v) => sum + v.penaltyPoints, 0)
)
const currentStatus = computed(() => 'warning')

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

function getViolationCountClass(count: number) {
  if (count === 0) return 'text-success'
  if (count <= 2) return 'text-warning'
  return 'text-danger'
}

function getPenaltyPointsClass(points: number) {
  if (points <= 5) return 'text-warning'
  if (points <= 10) return 'text-orange'
  return 'text-danger'
}

function getStatusType(status: string) {
  const types = {
    good: 'success',
    warning: 'warning',
    serious: 'danger'
  }
  return types[status] || 'info'
}

function getStatusLabel(status: string) {
  const labels = {
    good: 'Tốt',
    warning: 'Cần chú ý',
    serious: 'Nghiêm trọng'
  }
  return labels[status] || status
}

function getSeverityType(severity: string) {
  const types = {
    minor: 'info',
    moderate: 'warning',
    serious: 'danger'
  }
  return types[severity] || 'info'
}

function getSeverityLabel(severity: string) {
  const labels = {
    minor: 'Nhẹ',
    moderate: 'Trung bình',
    serious: 'Nghiêm trọng'
  }
  return labels[severity] || severity
}

function getViolationStatusType(status: string) {
  const types = {
    pending: 'warning',
    processed: 'success',
    appealing: 'info'
  }
  return types[status] || 'info'
}

function getViolationStatusLabel(status: string) {
  const labels = {
    pending: 'Chờ xử lý',
    processed: 'Đã xử lý',
    appealing: 'Đang khiếu nại'
  }
  return labels[status] || status
}

function viewDetails(violation: any) {
  console.log('Viewing details:', violation.id)
}

async function downloadAttachment(file: any) {
  try {
    // Implement file download
    ElMessage.success('Tải file thành công')
  } catch (error) {
    ElMessage.error('Tải file thất bại. Vui lòng thử lại.')
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

.text-orange {
  color: #ff7700;
}

.text-danger {
  color: var(--el-color-danger);
}

.el-card :deep(.el-card__header) {
  padding: 12px 20px;
}
</style>