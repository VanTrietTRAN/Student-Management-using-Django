<template>
  <div>
    <el-card class="mb-4">
      <template #header>
        <div class="flex justify-between items-center">
          <h2 class="text-lg font-semibold">Thông tin khen thưởng</h2>
          <el-select v-model="selectedYear" placeholder="Chọn năm học">
            <el-option
              v-for="year in academicYears"
              :key="year.value"
              :label="year.label"
              :value="year.value"
            />
          </el-select>
        </div>
      </template>

      <!-- Summary Cards -->
      <div class="grid grid-cols-4 gap-4 mb-6">
        <el-card shadow="hover" class="text-center">
          <h3 class="text-lg font-medium mb-2">Tổng số khen thưởng</h3>
          <div class="text-2xl font-bold text-primary">{{ totalRewards }}</div>
        </el-card>

        <el-card shadow="hover" class="text-center">
          <h3 class="text-lg font-medium mb-2">Thành tích nổi bật</h3>
          <div class="text-xl font-medium text-success">{{ topAchievement }}</div>
        </el-card>

        <el-card shadow="hover" class="text-center">
          <h3 class="text-lg font-medium mb-2">Giá trị phần thưởng</h3>
          <div class="text-2xl font-bold text-warning">{{ totalValue }}</div>
        </el-card>

        <el-card shadow="hover" class="text-center">
          <h3 class="text-lg font-medium mb-2">Danh hiệu hiện tại</h3>
          <el-tag :type="getAchievementType(currentTitle)">
            {{ currentTitle }}
          </el-tag>
        </el-card>
      </div>

      <!-- Rewards List -->
      <div>
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-medium">Danh sách khen thưởng</h3>
          <el-input
            v-model="searchQuery"
            placeholder="Tìm kiếm..."
            prefix-icon="Search"
            style="width: 300px"
            clearable
          />
        </div>

        <el-table
          :data="filteredRewards"
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
                  <el-descriptions-item label="Đơn vị">
                    {{ props.row.department }}
                  </el-descriptions-item>
                </el-descriptions>

                <div class="mt-4">
                  <h4 class="font-medium mb-2">Nội dung chi tiết</h4>
                  <p class="text-gray-600">{{ props.row.details }}</p>
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

          <el-table-column prop="title" label="Thành tích" min-width="300">
            <template #default="{ row }">
              <div class="font-medium">{{ row.title }}</div>
              <div class="text-xs text-gray-500">{{ row.category }}</div>
            </template>
          </el-table-column>

          <el-table-column prop="level" label="Cấp" width="150">
            <template #default="{ row }">
              <el-tag :type="getAchievementLevelType(row.level)">
                {{ getAchievementLevelLabel(row.level) }}
              </el-tag>
            </template>
          </el-table-column>

          <el-table-column prop="value" label="Giá trị" width="150">
            <template #default="{ row }">
              {{ formatCurrency(row.value) }}
            </template>
          </el-table-column>

          <el-table-column prop="status" label="Trạng thái" width="150">
            <template #default="{ row }">
              <el-tag :type="getStatusType(row.status)">
                {{ getStatusLabel(row.status) }}
              </el-tag>
            </template>
          </el-table-column>

          <el-table-column fixed="right" label="Thao tác" width="120">
            <template #default="{ row }">
              <el-button-group>
                <el-button
                  type="primary"
                  :icon="View"
                  circle
                  @click="viewDetails(row)"
                />
                <el-button
                  type="success"
                  :icon="Download"
                  circle
                  @click="downloadCertificate(row)"
                />
              </el-button-group>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- Achievement Categories Chart -->
      <div class="mt-6">
        <h3 class="text-lg font-medium mb-4">Phân loại thành tích</h3>
        <div class="grid grid-cols-2 gap-6">
          <div>
            <!-- Add pie chart for categories -->
            <el-table :data="categoryStats" style="width: 100%">
              <el-table-column prop="category" label="Loại" min-width="200" />
              <el-table-column prop="count" label="Số lượng" width="120" align="center" />
              <el-table-column prop="percentage" label="Tỷ lệ" width="150">
                <template #default="{ row }">
                  <el-progress
                    :percentage="row.percentage"
                    :color="row.color"
                  />
                </template>
              </el-table-column>
            </el-table>
          </div>
          <div>
            <!-- Add bar chart for trend -->
            <el-table :data="levelStats" style="width: 100%">
              <el-table-column prop="level" label="Cấp" min-width="150" />
              <el-table-column prop="count" label="Số lượng" width="120" align="center" />
              <el-table-column prop="value" label="Giá trị" width="150">
                <template #default="{ row }">
                  {{ formatCurrency(row.value) }}
                </template>
              </el-table-column>
            </el-table>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { format } from 'date-fns'
import { vi } from 'date-fns/locale'
import { Document, Download, View } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

// State
const selectedYear = ref('2025-2026')
const searchQuery = ref('')

// Mock data - replace with API calls
const academicYears = ref([
  { label: 'Năm học 2025-2026', value: '2025-2026' },
  { label: 'Năm học 2024-2025', value: '2024-2025' }
])

const rewards = ref([
  {
    id: 1,
    date: '2025-10-01',
    title: 'Sinh viên xuất sắc học kỳ',
    category: 'Thành tích học tập',
    level: 'university',
    value: 2000000,
    status: 'approved',
    decisionNumber: 'QD123/2025',
    decisionDate: '2025-09-30',
    signedBy: 'PGS.TS. Nguyễn Văn A',
    department: 'Phòng Công tác Sinh viên',
    details: 'Đạt thành tích xuất sắc trong học tập học kỳ 1 năm học 2025-2026',
    attachments: [
      {
        id: 1,
        name: 'Quyết định khen thưởng.pdf',
        size: 1500000,
        url: '#'
      }
    ]
  },
  // Add more rewards
])

const totalRewards = computed(() => rewards.value.length)
const topAchievement = ref('Sinh viên xuất sắc cấp trường')
const totalValue = computed(() => 
  formatCurrency(rewards.value.reduce((sum, reward) => sum + reward.value, 0))
)
const currentTitle = ref('Sinh viên Xuất sắc')

const filteredRewards = computed(() => {
  let result = rewards.value

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(reward =>
      reward.title.toLowerCase().includes(query) ||
      reward.category.toLowerCase().includes(query) ||
      reward.decisionNumber?.toLowerCase().includes(query)
    )
  }

  return result.filter(reward => reward.date.startsWith(selectedYear.value.split('-')[0]))
})

const categoryStats = ref([
  {
    category: 'Thành tích học tập',
    count: 5,
    percentage: 45,
    color: '#409EFF'
  },
  {
    category: 'Hoạt động đoàn thể',
    count: 3,
    percentage: 27,
    color: '#67C23A'
  },
  {
    category: 'Nghiên cứu khoa học',
    count: 2,
    percentage: 18,
    color: '#E6A23C'
  },
  {
    category: 'Khác',
    count: 1,
    percentage: 10,
    color: '#909399'
  }
])

const levelStats = ref([
  {
    level: 'Cấp trường',
    count: 6,
    value: 5000000
  },
  {
    level: 'Cấp khoa',
    count: 4,
    value: 2000000
  },
  {
    level: 'Cấp lớp',
    count: 1,
    value: 500000
  }
])

// Methods
function formatDate(date: string) {
  return format(new Date(date), 'dd/MM/yyyy', { locale: vi })
}

function formatCurrency(amount: number) {
  return new Intl.NumberFormat('vi-VN', {
    style: 'currency',
    currency: 'VND'
  }).format(amount)
}

function formatFileSize(bytes: number) {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

function getAchievementType(achievement: string) {
  const types = {
    'Sinh viên Xuất sắc': 'success',
    'Sinh viên Giỏi': 'primary',
    'Sinh viên Khá': 'warning'
  }
  return types[achievement] || 'info'
}

function getAchievementLevelType(level: string) {
  const types = {
    ministry: 'danger',
    university: 'success',
    faculty: 'primary',
    class: 'info'
  }
  return types[level] || 'info'
}

function getAchievementLevelLabel(level: string) {
  const labels = {
    ministry: 'Cấp Bộ',
    university: 'Cấp trường',
    faculty: 'Cấp khoa',
    class: 'Cấp lớp'
  }
  return labels[level] || level
}

function getStatusType(status: string) {
  const types = {
    pending: 'warning',
    approved: 'success',
    completed: 'info'
  }
  return types[status] || 'info'
}

function getStatusLabel(status: string) {
  const labels = {
    pending: 'Chờ duyệt',
    approved: 'Đã duyệt',
    completed: 'Đã nhận'
  }
  return labels[status] || status
}

function viewDetails(reward: any) {
  console.log('Viewing details:', reward.id)
}

async function downloadCertificate(reward: any) {
  try {
    // Implement certificate download
    ElMessage.success('Tải chứng nhận thành công')
  } catch (error) {
    ElMessage.error('Tải chứng nhận thất bại. Vui lòng thử lại.')
  }
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

.text-danger {
  color: var(--el-color-danger);
}

.el-card :deep(.el-card__header) {
  padding: 12px 20px;
}
</style>