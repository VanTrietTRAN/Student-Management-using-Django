&lt;template>
  &lt;div class="p-6">
    &lt;!-- Page Header -->
    &lt;div class="mb-6">
      &lt;h1 class="text-2xl font-bold text-gray-900">{{ $t('Điểm số') }}&lt;/h1>
    &lt;/div>

    &lt;!-- Semester Selection -->
    &lt;div class="mb-6">
      &lt;el-select v-model="selectedSemester" class="w-64">
        &lt;el-option
          v-for="semester in semesters"
          :key="semester.value"
          :label="semester.label"
          :value="semester.value"
        />
      &lt;/el-select>
    &lt;/div>

    &lt;!-- Grades Table -->
    &lt;el-table :data="grades" stripe>
      &lt;el-table-column prop="courseCode" :label="$t('Mã học phần')" width="150" />
      &lt;el-table-column prop="courseName" :label="$t('Tên học phần')" min-width="250" />
      &lt;el-table-column prop="credits" :label="$t('Số tín chỉ')" width="120" align="center" />
      &lt;el-table-column prop="attendance" :label="$t('Chuyên cần')" width="120" align="center" />
      &lt;el-table-column prop="midterm" :label="$t('Giữa kỳ')" width="120" align="center" />
      &lt;el-table-column prop="final" :label="$t('Cuối kỳ')" width="120" align="center" />
      &lt;el-table-column prop="average" :label="$t('Trung bình')" width="120" align="center">
        &lt;template #default="{ row }">
          &lt;span :class="getGradeColor(row.average)">{{ row.average }}&lt;/span>
        &lt;/template>
      &lt;/el-table-column>
      &lt;el-table-column prop="letterGrade" :label="$t('Điểm chữ')" width="120" align="center">
        &lt;template #default="{ row }">
          &lt;el-tag :type="getGradeTagType(row.letterGrade)">{{ row.letterGrade }}&lt;/el-tag>
        &lt;/template>
      &lt;/el-table-column>
    &lt;/el-table>

    &lt;!-- Semester Summary -->
    &lt;div class="mt-6 bg-white p-6 rounded-lg shadow">
      &lt;div class="grid grid-cols-3 gap-6">
        &lt;div class="text-center">
          &lt;p class="text-sm text-gray-600">{{ $t('GPA Học kỳ') }}&lt;/p>
          &lt;p class="text-2xl font-bold text-primary-600">3.67&lt;/p>
        &lt;/div>
        &lt;div class="text-center">
          &lt;p class="text-sm text-gray-600">{{ $t('Số tín chỉ đạt') }}&lt;/p>
          &lt;p class="text-2xl font-bold text-primary-600">15/15&lt;/p>
        &lt;/div>
        &lt;div class="text-center">
          &lt;p class="text-sm text-gray-600">{{ $t('Xếp loại') }}&lt;/p>
          &lt;p class="text-2xl font-bold text-primary-600">{{ $t('Giỏi') }}&lt;/p>
        &lt;/div>
      &lt;/div>
    &lt;/div>
  &lt;/div>
&lt;/template>

&lt;script setup lang="ts">
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
&lt;/script>

&lt;style scoped>
.el-table {
  @apply rounded-lg shadow;
}
&lt;/style>