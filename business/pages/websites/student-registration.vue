<template>
  <div class="p-6">
    <!-- Page Header -->
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-900">{{ $t('Đăng ký học phần') }}</h1>
    </div>

    <!-- Registration Period Info -->
    <el-alert
      v-if="registrationPeriod.isActive"
      type="success"
      :title="$t('Thời gian đăng ký:')"
      :description="registrationPeriod.timeRange"
      show-icon
      class="mb-6"
    />
    <el-alert
      v-else
      type="info"
      :title="$t('Chưa đến thời gian đăng ký')"
      :description="$t('Thời gian đăng ký sẽ được thông báo qua email')"
      show-icon
      class="mb-6"
    />

    <!-- Course Search and Filters -->
    <div class="mb-6 flex gap-4">
      <el-input
        v-model="searchQuery"
        :placeholder="$t('Tìm kiếm theo mã hoặc tên học phần')"
        class="w-96"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
      
      <el-select v-model="selectedDepartment" :placeholder="$t('Khoa/Viện')" class="w-64">
        <el-option
          v-for="dept in departments"
          :key="dept.value"
          :label="dept.label"
          :value="dept.value"
        />
      </el-select>
    </div>

    <!-- Available Courses Table -->
    <el-table :data="filteredCourses" stripe>
      <el-table-column type="expand">
        <template #default="scope">
          <div class="p-4">
            <h4 class="font-bold mb-2">{{ $t('Lớp học phần có sẵn:') }}</h4>
            <el-table :data="scope.row.sections" border>
              <el-table-column prop="sectionCode" :label="$t('Mã lớp')" width="120" />
              <el-table-column prop="instructor" :label="$t('Giảng viên')" width="200" />
              <el-table-column prop="schedule" :label="$t('Lịch học')" min-width="200" />
              <el-table-column prop="room" :label="$t('Phòng học')" width="120" />
              <el-table-column prop="enrolled" :label="$t('Đã đăng ký')" width="120">
                <template #default="scope">
                  {{ scope.row.enrolled }}/{{ scope.row.capacity }}
                </template>
              </el-table-column>
              <el-table-column align="right" width="120">
                <template #default="scope">
                  <el-button
                    type="primary"
                    :disabled="scope.row.enrolled >= scope.row.capacity"
                    @click="registerSection(scope.row)"
                  >
                    {{ $t('Đăng ký') }}
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="courseCode" :label="$t('Mã học phần')" width="150" />
      <el-table-column prop="courseName" :label="$t('Tên học phần')" min-width="300" />
      <el-table-column prop="credits" :label="$t('Số tín chỉ')" width="120" align="center" />
      <el-table-column prop="type" :label="$t('Loại học phần')" width="150">
        <template #default="scope">
          <el-tag :type="getCourseTypeTag(scope.row.type)">{{ scope.row.type }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="prerequisite" :label="$t('Học phần tiên quyết')" width="200" />
    </el-table>

    <!-- Registered Courses -->
    <div class="mt-8">
      <h2 class="text-xl font-bold mb-4">{{ $t('Các học phần đã đăng ký') }}</h2>
      <el-table :data="registeredCourses" stripe>
        <el-table-column prop="courseCode" :label="$t('Mã học phần')" width="150" />
        <el-table-column prop="courseName" :label="$t('Tên học phần')" min-width="300" />
        <el-table-column prop="sectionCode" :label="$t('Mã lớp')" width="120" />
        <el-table-column prop="schedule" :label="$t('Lịch học')" width="200" />
        <el-table-column prop="room" :label="$t('Phòng học')" width="120" />
        <el-table-column prop="instructor" :label="$t('Giảng viên')" width="200" />
        <el-table-column align="right" width="120">
          <template #default="scope">
            <el-button type="danger" @click="unregisterCourse(scope.row)">
              {{ $t('Hủy đăng ký') }}
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- Registration Summary -->
      <div class="mt-6 bg-white p-6 rounded-lg shadow">
        <div class="grid grid-cols-2 gap-6">
          <div class="text-center">
            <p class="text-sm text-gray-600">{{ $t('Tổng số tín chỉ đăng ký') }}</p>
            <p class="text-2xl font-bold text-primary-600">12/24</p>
          </div>
          <div class="text-center">
            <p class="text-sm text-gray-600">{{ $t('Học phí tạm tính') }}</p>
            <p class="text-2xl font-bold text-primary-600">12,000,000 VNĐ</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { Search } from '@element-plus/icons-vue'
import { ElMessageBox, ElMessage } from 'element-plus'
import { useI18n } from 'vue-i18n'

const { t: $t } = useI18n()

interface Section {
  sectionCode: string
  instructor: string
  schedule: string
  room: string
  enrolled: number
  capacity: number
}

interface Course {
  courseCode: string
  courseName: string
  credits: number
  type: string
  prerequisite: string
  sections: Section[]
}

interface RegisteredCourse {
  courseCode: string
  courseName: string
  sectionCode: string
  schedule: string
  room: string
  instructor: string
}

const searchQuery = ref('')
const selectedDepartment = ref('')

const registrationPeriod = ref({
  isActive: true,
  timeRange: '15/01/2024 - 25/01/2024'
})

const departments = [
  { value: 'fit', label: 'Viện Công nghệ Thông tin' },
  { value: 'fee', label: 'Viện Điện tử - Viễn thông' },
  { value: 'sem', label: 'Viện Kinh tế & Quản lý' },
]

const courses = ref<Course[]>([
  {
    courseCode: 'INT3306',
    courseName: 'Web Programming',
    credits: 3,
    type: 'Bắt buộc',
    prerequisite: 'INT2020',
    sections: [
      {
        sectionCode: '123456',
        instructor: 'Nguyễn Văn A',
        schedule: 'Thứ 2 (1-3), Thứ 4 (1-3)',
        room: 'D3-201',
        enrolled: 45,
        capacity: 50
      },
      {
        sectionCode: '123457',
        instructor: 'Trần Thị B',
        schedule: 'Thứ 3 (1-3), Thứ 5 (1-3)',
        room: 'D3-202',
        enrolled: 50,
        capacity: 50
      }
    ]
  },
  {
    courseCode: 'INT3307',
    courseName: 'Database Systems',
    credits: 3,
    type: 'Bắt buộc',
    prerequisite: 'INT2020',
    sections: [
      {
        sectionCode: '123458',
        instructor: 'Lê Văn C',
        schedule: 'Thứ 2 (4-6), Thứ 4 (4-6)',
        room: 'D3-203',
        enrolled: 40,
        capacity: 50
      }
    ]
  }
])

const registeredCourses = ref<RegisteredCourse[]>([
  {
    courseCode: 'INT3308',
    courseName: 'Software Engineering',
    sectionCode: '123459',
    schedule: 'Thứ 3 (4-6), Thứ 5 (4-6)',
    room: 'D3-204',
    instructor: 'Phạm Thị D'
  }
])

const filteredCourses = computed(() => {
  return courses.value.filter(course => {
    const matchesSearch = searchQuery.value === '' || 
      course.courseCode.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      course.courseName.toLowerCase().includes(searchQuery.value.toLowerCase())
    
    const matchesDepartment = selectedDepartment.value === '' || 
      course.courseCode.startsWith(selectedDepartment.value.toUpperCase())
    
    return matchesSearch && matchesDepartment
  })
})

const getCourseTypeTag = (type: string) => {
  switch (type) {
    case 'Bắt buộc':
      return 'danger'
    case 'Tự chọn':
      return 'warning'
    default:
      return 'info'
  }
}

const registerSection = async (section: Section) => {
  try {
    await ElMessageBox.confirm(
      $t('Bạn có chắc chắn muốn đăng ký học phần này?'),
      $t('Xác nhận đăng ký'),
      {
        confirmButtonText: $t('Đăng ký'),
        cancelButtonText: $t('Hủy'),
        type: 'warning',
      }
    )
    // TODO: Implement registration logic
    ElMessage.success($t('Đăng ký thành công!'))
  } catch {
    // User cancelled
  }
}

const unregisterCourse = async (course: RegisteredCourse) => {
  try {
    await ElMessageBox.confirm(
      $t('Bạn có chắc chắn muốn hủy đăng ký học phần này?'),
      $t('Xác nhận hủy đăng ký'),
      {
        confirmButtonText: $t('Hủy đăng ký'),
        cancelButtonText: $t('Giữ lại'),
        type: 'warning',
      }
    )
    // TODO: Implement unregistration logic
    ElMessage.success($t('Hủy đăng ký thành công!'))
  } catch {
    // User cancelled
  }
}
</script>

<style scoped>
.el-table {
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
}
</style>