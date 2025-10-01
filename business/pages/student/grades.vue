<template>
  <div class="grades">
    <el-card class="grades-summary">
      <template #header>
        <div class="card-header">
          <span>{{ $t('Bảng điểm tổng hợp') }}</span>
          <el-select v-model="selectedSemester" :placeholder="$t('Chọn học kỳ')">
            <el-option
              v-for="sem in semesters"
              :key="sem.id"
              :label="sem.name"
              :value="sem.id"
            />
          </el-select>
        </div>
      </template>

      <el-table :data="grades" style="width: 100%">
        <el-table-column :label="$t('Mã học phần')" prop="courseCode" />
        <el-table-column :label="$t('Tên học phần')" prop="courseName" />
        <el-table-column :label="$t('Số tín chỉ')" prop="credits" width="100" />
        <el-table-column :label="$t('Điểm chuyên cần')" prop="attendanceGrade" width="120" />
        <el-table-column :label="$t('Điểm giữa kỳ')" prop="midtermGrade" width="120" />
        <el-table-column :label="$t('Điểm cuối kỳ')" prop="finalGrade" width="120" />
        <el-table-column :label="$t('Điểm tổng kết')" prop="totalGrade" width="120" />
        <el-table-column :label="$t('Kết quả')" prop="status">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>

      <div class="semester-summary mt-4">
        <el-descriptions :column="3" border>
          <el-descriptions-item :label="$t('GPA Học kỳ')">
            {{ semesterGPA }}
          </el-descriptions-item>
          <el-descriptions-item :label="$t('Số tín chỉ đạt')">
            {{ passedCredits }}
          </el-descriptions-item>
          <el-descriptions-item :label="$t('Xếp loại')">
            {{ classification }}
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const selectedSemester = ref('')

const semesters = ref([
  { id: 1, name: 'Học kỳ 1 - 2023-2024' },
  { id: 2, name: 'Học kỳ 2 - 2023-2024' }
])

const grades = ref([
  {
    courseCode: 'INT1234',
    courseName: 'Lập trình Web',
    credits: 3,
    attendanceGrade: 9.0,
    midtermGrade: 8.5,
    finalGrade: 8.0,
    totalGrade: 8.3,
    status: 'passed'
  },
  {
    courseCode: 'INT2345',
    courseName: 'Cơ sở dữ liệu',
    credits: 4,
    attendanceGrade: 8.0,
    midtermGrade: 7.5,
    finalGrade: 8.5,
    totalGrade: 8.2,
    status: 'passed'
  }
])

const getStatusType = (status: string) => {
  switch (status) {
    case 'passed':
      return 'success'
    case 'failed':
      return 'danger'
    default:
      return 'info'
  }
}

const getStatusText = (status: string) => {
  switch (status) {
    case 'passed':
      return 'Đạt'
    case 'failed':
      return 'Không đạt'
    default:
      return 'Chưa có kết quả'
  }
}

const semesterGPA = computed(() => {
  // Calculate GPA logic here
  return '3.5'
})

const passedCredits = computed(() => {
  return grades.value.reduce((total, grade) => {
    return grade.status === 'passed' ? total + grade.credits : total
  }, 0)
})

const classification = computed(() => {
  const gpa = parseFloat(semesterGPA.value)
  if (gpa >= 3.6) return 'Xuất sắc'
  if (gpa >= 3.2) return 'Giỏi'
  if (gpa >= 2.5) return 'Khá'
  if (gpa >= 2.0) return 'Trung bình'
  return 'Yếu'
})
</script>

<style scoped>
.grades {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.mt-4 {
  margin-top: 1rem;
}
</style>