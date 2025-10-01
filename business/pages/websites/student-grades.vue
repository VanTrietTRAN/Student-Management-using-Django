<template>
  <div class="p-6">
    <!-- Page Header -->
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-900">{{ $t('Điểm số') }}</h1>
    </div>

    <!-- Semester Selection -->
    <div class="mb-6">
      <el-select v-model="selectedSemester" class="w-64">
        <el-option
          v-for="semester in semesters"
          :key="semester.value"
          :label="semester.label"
          :value="semester.value"
        />
      </el-select>
    </div>

    <!-- Grades Table -->
    <el-table :data="grades" stripe>
      <el-table-column prop="courseCode" :label="$t('Mã học phần')" width="150" />
      <el-table-column prop="courseName" :label="$t('Tên học phần')" min-width="250" />
      <el-table-column prop="credits" :label="$t('Số tín chỉ')" width="120" align="center" />
      <el-table-column prop="attendance" :label="$t('Chuyên cần')" width="120" align="center" />
      <el-table-column prop="midterm" :label="$t('Giữa kỳ')" width="120" align="center" />
      <el-table-column prop="final" :label="$t('Cuối kỳ')" width="120" align="center" />
      <el-table-column prop="average" :label="$t('Trung bình')" width="120" align="center">
        <template #default="{ row }">
          <span :class="getGradeColor(row.average)">{{ row.average }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="letterGrade" :label="$t('Điểm chữ')" width="120" align="center">
        <template #default="{ row }">
          <el-tag :type="getGradeTagType(row.letterGrade)">{{ row.letterGrade }}</el-tag>
        </template>
      </el-table-column>
    </el-table>

    <!-- Semester Summary -->
    <div class="mt-6 bg-white p-6 rounded-lg shadow">
      <div class="grid grid-cols-3 gap-6">
        <div class="text-center">
          <p class="text-sm text-gray-600">{{ $t('GPA Học kỳ') }}</p>
          <p class="text-2xl font-bold text-primary-600">3.67</p>
        </div>
        <div class="text-center">
          <p class="text-sm text-gray-600">{{ $t('Số tín chỉ đạt') }}</p>
          <p class="text-2xl font-bold text-primary-600">15/15</p>
        </div>
        <div class="text-center">
          <p class="text-sm text-gray-600">{{ $t('Xếp loại') }}</p>
          <p class="text-2xl font-bold text-primary-600">{{ $t('Giỏi') }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const selectedSemester = ref('2023-2')

const semesters = [
  { label: 'Học kỳ 2 - 2023/2024', value: '2023-2' },
  { label: 'Học kỳ 1 - 2023/2024', value: '2023-1' },
  { label: 'Học kỳ 2 - 2022/2023', value: '2022-2' },
]

const grades = ref([
  {
    courseCode: 'INT3306',
    courseName: 'Web Programming',
    credits: 3,
    attendance: 10,
    midterm: 9.0,
    final: 8.5,
    average: 8.8,
    letterGrade: 'A'
  },
  {
    courseCode: 'INT3307',
    courseName: 'Database Systems',
    credits: 3,
    attendance: 9,
    midterm: 8.5,
    final: 9.0,
    average: 8.8,
    letterGrade: 'A'
  },
  {
    courseCode: 'INT3308',
    courseName: 'Software Engineering',
    credits: 3,
    attendance: 8,
    midterm: 7.5,
    final: 8.0,
    average: 7.8,
    letterGrade: 'B+'
  },
])

const getGradeColor = (grade: number) => {
  if (grade >= 8.5) return 'text-green-600 font-bold'
  if (grade >= 7.0) return 'text-blue-600 font-bold'
  if (grade >= 5.5) return 'text-yellow-600 font-bold'
  return 'text-red-600 font-bold'
}

const getGradeTagType = (grade: string) => {
  switch (grade) {
    case 'A':
    case 'A+':
      return 'success'
    case 'B+':
    case 'B':
      return 'primary'
    case 'C+':
    case 'C':
      return 'warning'
    default:
      return 'danger'
  }
}
</script>

<style scoped>
.el-table {
  @apply rounded-lg shadow;
}
</style>