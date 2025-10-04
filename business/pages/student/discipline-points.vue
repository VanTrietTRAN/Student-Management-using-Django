<template>
  <div>
    <el-card class="mb-4">
      <template #header>
        <div class="flex justify-between items-center">
          <h2 class="text-lg font-semibold">Điểm rèn luyện</h2>
          <el-select v-model="selectedSemester" placeholder="Chọn học kỳ">
            <el-option
              v-for="semester in semesters"
              :key="semester.value"
              :label="semester.label"
              :value="semester.value"
            />
          </el-select>
        </div>
      </template>

      <!-- Summary Cards -->
      <div class="grid grid-cols-4 gap-4 mb-6">
        <el-card shadow="hover" class="text-center">
          <h3 class="text-lg font-medium mb-2">Điểm kỳ này</h3>
          <div class="text-2xl font-bold" :class="getDisciplineScoreClass(currentScore)">
            {{ currentScore }}/100
          </div>
        </el-card>

        <el-card shadow="hover" class="text-center">
          <h3 class="text-lg font-medium mb-2">Điểm trung bình</h3>
          <div class="text-2xl font-bold" :class="getDisciplineScoreClass(averageScore)">
            {{ averageScore }}/100
          </div>
        </el-card>

        <el-card shadow="hover" class="text-center">
          <h3 class="text-lg font-medium mb-2">Xếp loại</h3>
          <el-tag :type="getRankingType(currentRanking)">
            {{ currentRanking }}
          </el-tag>
        </el-card>

        <el-card shadow="hover" class="text-center">
          <h3 class="text-lg font-medium mb-2">Trạng thái</h3>
          <el-tag :type="getStatusType(status)">
            {{ getStatusLabel(status) }}
          </el-tag>
        </el-card>
      </div>

      <!-- Score Details -->
      <div>
        <h3 class="text-lg font-medium mb-4">Chi tiết điểm rèn luyện</h3>
        <el-table
          :data="disciplineScores"
          style="width: 100%"
        >
          <el-table-column type="expand">
            <template #default="props">
              <div class="p-4">
                <el-table
                  :data="props.row.details"
                  style="width: 100%"
                  border
                >
                  <el-table-column prop="criteria" label="Tiêu chí" min-width="400" />
                  <el-table-column prop="maxScore" label="Điểm tối đa" width="120" align="center" />
                  <el-table-column prop="score" label="Điểm đạt" width="120" align="center">
                    <template #default="{ row }">
                      <span :class="getScoreClass(row.score, row.maxScore)">
                        {{ row.score }}
                      </span>
                    </template>
                  </el-table-column>
                  <el-table-column prop="note" label="Ghi chú" min-width="200" />
                </el-table>
              </div>
            </template>
          </el-table-column>

          <el-table-column prop="category" label="Danh mục đánh giá" min-width="400" />
          <el-table-column prop="maxScore" label="Điểm tối đa" width="120" align="center" />
          <el-table-column prop="score" label="Điểm đạt" width="120" align="center">
            <template #default="{ row }">
              <span :class="getScoreClass(row.score, row.maxScore)">
                {{ row.score }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="percentage" label="Tỷ lệ đạt" width="150">
            <template #default="{ row }">
              <el-progress
                :percentage="(row.score / row.maxScore) * 100"
                :status="getProgressStatus(row.score / row.maxScore)"
              />
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- History Chart -->
      <div class="mt-6">
        <h3 class="text-lg font-medium mb-4">Lịch sử điểm rèn luyện</h3>
        <div style="height: 400px">
          <!-- Add chart component here -->
          <el-table
            :data="scoreHistory"
            style="width: 100%"
          >
            <el-table-column prop="semester" label="Học kỳ" width="200" />
            <el-table-column prop="score" label="Điểm" width="120" align="center">
              <template #default="{ row }">
                <span :class="getDisciplineScoreClass(row.score)">
                  {{ row.score }}
                </span>
              </template>
            </el-table-column>
            <el-table-column prop="ranking" label="Xếp loại" width="150">
              <template #default="{ row }">
                <el-tag :type="getRankingType(row.ranking)">
                  {{ row.ranking }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="note" label="Ghi chú" min-width="200" />
          </el-table>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

// State
const selectedSemester = ref('2025-1')
const currentScore = ref(85)
const averageScore = ref(82)
const currentRanking = ref('Tốt')
const status = ref('submitted')

// Mock data - replace with API calls
const semesters = ref([
  { label: 'Học kỳ 1 - 2025-2026', value: '2025-1' },
  { label: 'Học kỳ 2 - 2024-2025', value: '2024-2' },
  { label: 'Học kỳ 1 - 2024-2025', value: '2024-1' }
])

const disciplineScores = ref([
  {
    category: 'Ý thức học tập',
    maxScore: 30,
    score: 25,
    details: [
      {
        criteria: 'Kết quả học tập',
        maxScore: 20,
        score: 17,
        note: 'GPA: 3.45'
      },
      {
        criteria: 'Tham gia nghiên cứu khoa học',
        maxScore: 10,
        score: 8,
        note: 'Tham gia 1 đề tài NCKH cấp trường'
      }
    ]
  },
  {
    category: 'Ý thức chấp hành nội quy',
    maxScore: 25,
    score: 23,
    details: [
      {
        criteria: 'Thực hiện nội quy, quy chế',
        maxScore: 15,
        score: 15,
        note: 'Không vi phạm'
      },
      {
        criteria: 'Tham gia sinh hoạt lớp',
        maxScore: 10,
        score: 8,
        note: 'Vắng 1 buổi có phép'
      }
    ]
  },
  // Add more categories
])

const scoreHistory = ref([
  {
    semester: 'HK1 2025-2026',
    score: 85,
    ranking: 'Tốt',
    note: 'Đã phê duyệt'
  },
  {
    semester: 'HK2 2024-2025',
    score: 82,
    ranking: 'Tốt',
    note: 'Đã phê duyệt'
  },
  {
    semester: 'HK1 2024-2025',
    score: 78,
    ranking: 'Khá',
    note: 'Đã phê duyệt'
  }
])

// Methods
function getDisciplineScoreClass(score: number) {
  if (score >= 90) return 'text-success'
  if (score >= 80) return 'text-primary'
  if (score >= 65) return 'text-warning'
  if (score >= 50) return 'text-orange'
  return 'text-danger'
}

function getScoreClass(score: number, maxScore: number) {
  const percentage = (score / maxScore) * 100
  return getDisciplineScoreClass(percentage)
}

function getRankingType(ranking: string) {
  const types = {
    'Xuất sắc': 'success',
    'Tốt': 'primary',
    'Khá': 'warning',
    'Trung bình': 'info',
    'Yếu': 'danger'
  }
  return types[ranking] || 'info'
}

function getStatusType(status: string) {
  const types = {
    draft: 'info',
    submitted: 'warning',
    approved: 'success',
    rejected: 'danger'
  }
  return types[status] || 'info'
}

function getStatusLabel(status: string) {
  const labels = {
    draft: 'Bản nháp',
    submitted: 'Đã nộp',
    approved: 'Đã duyệt',
    rejected: 'Từ chối'
  }
  return labels[status] || status
}

function getProgressStatus(progress: number) {
  if (progress >= 0.9) return 'success'
  if (progress >= 0.7) return ''
  if (progress >= 0.5) return 'warning'
  return 'exception'
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