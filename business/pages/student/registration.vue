<template>
  <div class="registration">
    <el-card class="available-courses">
      <template #header>
        <div class="card-header">
          <span>{{ $t('Đăng ký học phần') }}</span>
        </div>
      </template>

      <el-table 
        :data="availableCourses"
        style="width: 100%"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column :label="$t('Mã học phần')" prop="courseCode" />
        <el-table-column :label="$t('Tên học phần')" prop="courseName" />
        <el-table-column :label="$t('Số tín chỉ')" prop="credits" width="100" />
        <el-table-column :label="$t('Giảng viên')" prop="teacher" />
        <el-table-column :label="$t('Lịch học')" prop="schedule" />
        <el-table-column :label="$t('Số chỗ còn lại')" width="120">
          <template #default="{ row }">
            {{ row.remainingSlots }}/{{ row.maxSlots }}
          </template>
        </el-table-column>
      </el-table>

      <div class="registration-actions mt-4">
        <el-button 
          type="primary"
          :disabled="!selectedCourses.length"
          @click="registerCourses"
        >
          {{ $t('Đăng ký các môn đã chọn') }}
        </el-button>
      </div>
    </el-card>

    <el-card class="registered-courses mt-4">
      <template #header>
        <div class="card-header">
          <span>{{ $t('Học phần đã đăng ký') }}</span>
        </div>
      </template>

      <el-table :data="registeredCourses" style="width: 100%">
        <el-table-column :label="$t('Mã học phần')" prop="courseCode" />
        <el-table-column :label="$t('Tên học phần')" prop="courseName" />
        <el-table-column :label="$t('Số tín chỉ')" prop="credits" width="100" />
        <el-table-column :label="$t('Giảng viên')" prop="teacher" />
        <el-table-column :label="$t('Lịch học')" prop="schedule" />
        <el-table-column :label="$t('Trạng thái')" width="120">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column :label="$t('Thao tác')" width="120">
          <template #default="{ row }">
            <el-button 
              type="danger" 
              link
              :disabled="!canCancel(row)"
              @click="cancelRegistration(row)"
            >
              {{ $t('Hủy đăng ký') }}
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="registration-summary mt-4">
        <el-descriptions :column="3" border>
          <el-descriptions-item :label="$t('Tổng số tín chỉ')">
            {{ totalCredits }}
          </el-descriptions-item>
          <el-descriptions-item :label="$t('Số môn đã đăng ký')">
            {{ registeredCourses.length }}
          </el-descriptions-item>
          <el-descriptions-item :label="$t('Học phí dự kiến')">
            {{ estimatedTuition }}
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const selectedCourses = ref([])

const availableCourses = ref([
  {
    courseCode: 'INT3001',
    courseName: 'Trí tuệ nhân tạo',
    credits: 3,
    teacher: 'Nguyễn Văn A',
    schedule: 'Thứ 2 (7:00 - 9:00)',
    remainingSlots: 15,
    maxSlots: 40
  },
  {
    courseCode: 'INT3002',
    courseName: 'Phát triển ứng dụng di động',
    credits: 3,
    teacher: 'Trần Thị B',
    schedule: 'Thứ 3 (13:00 - 15:00)',
    remainingSlots: 20,
    maxSlots: 35
  }
])

const registeredCourses = ref([
  {
    courseCode: 'INT2001',
    courseName: 'Lập trình Web',
    credits: 3,
    teacher: 'Lê Văn C',
    schedule: 'Thứ 4 (7:00 - 9:00)',
    status: 'approved'
  },
  {
    courseCode: 'INT2002',
    courseName: 'Cơ sở dữ liệu',
    credits: 3,
    teacher: 'Phạm Thị D',
    schedule: 'Thứ 5 (13:00 - 15:00)',
    status: 'pending'
  }
])

const handleSelectionChange = (selection) => {
  selectedCourses.value = selection
}

const registerCourses = async () => {
  try {
    // API call to register courses
    console.log('Registering courses:', selectedCourses.value)
    // Update UI after successful registration
  } catch (error) {
    console.error('Registration failed:', error)
  }
}

const getStatusType = (status: string) => {
  const types = {
    approved: 'success',
    pending: 'warning',
    rejected: 'danger'
  }
  return types[status] || 'info'
}

const getStatusText = (status: string) => {
  const texts = {
    approved: 'Đã duyệt',
    pending: 'Chờ duyệt',
    rejected: 'Bị từ chối'
  }
  return texts[status] || status
}

const canCancel = (course) => {
  return course.status === 'pending'
}

const cancelRegistration = async (course) => {
  try {
    // API call to cancel registration
    console.log('Cancelling registration:', course)
    // Update UI after successful cancellation
  } catch (error) {
    console.error('Cancellation failed:', error)
  }
}

const totalCredits = computed(() => {
  return registeredCourses.value.reduce((sum, course) => sum + course.credits, 0)
})

const estimatedTuition = computed(() => {
  // Calculate estimated tuition based on credits and course type
  const creditsPrice = 850000 // Price per credit
  return new Intl.NumberFormat('vi-VN', {
    style: 'currency',
    currency: 'VND'
  }).format(totalCredits.value * creditsPrice)
})
</script>

<style scoped>
.registration {
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

.registration-actions {
  display: flex;
  justify-content: flex-end;
}
</style>