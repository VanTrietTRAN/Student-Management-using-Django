<template>
  <div class="student-profile">
    <el-card class="profile-card">
      <template #header>
        <div class="card-header">
          <span>{{ $t('Thông tin sinh viên') }}</span>
          <el-button type="primary" @click="editMode = !editMode">
            {{ editMode ? $t('Lưu') : $t('Chỉnh sửa') }}
          </el-button>
        </div>
      </template>

      <el-form 
        ref="formRef"
        :model="profileData"
        :disabled="!editMode"
        label-width="120px"
      >
        <el-form-item :label="$t('Mã sinh viên')">
          <el-input v-model="profileData.studentId" disabled />
        </el-form-item>

        <el-form-item :label="$t('Họ và tên')">
          <el-input v-model="profileData.fullName" />
        </el-form-item>

        <el-form-item :label="$t('Ngày sinh')">
          <el-date-picker
            v-model="profileData.dateOfBirth"
            type="date"
            :placeholder="$t('Chọn ngày')"
          />
        </el-form-item>

        <el-form-item :label="$t('Email')">
          <el-input v-model="profileData.email" />
        </el-form-item>

        <el-form-item :label="$t('Số điện thoại')">
          <el-input v-model="profileData.phone" />
        </el-form-item>

        <el-form-item :label="$t('Địa chỉ')">
          <el-input v-model="profileData.address" type="textarea" />
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="academic-history mt-4">
      <template #header>
        <div class="card-header">
          <span>{{ $t('Lịch sử học tập') }}</span>
        </div>
      </template>

      <el-table :data="academicHistory" style="width: 100%">
        <el-table-column :label="$t('Học kỳ')" prop="semester" />
        <el-table-column :label="$t('Năm học')" prop="academicYear" />
        <el-table-column :label="$t('GPA')" prop="gpa" />
        <el-table-column :label="$t('Số tín chỉ')" prop="credits" />
        <el-table-column :label="$t('Xếp loại')" prop="classification" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const editMode = ref(false)

const profileData = ref({
  studentId: '2023001',
  fullName: 'Nguyễn Văn A',
  dateOfBirth: new Date('2000-01-01'),
  email: 'nguyenvana@student.edu.vn',
  phone: '0123456789',
  address: 'Hà Nội, Việt Nam'
})

const academicHistory = ref([
  {
    semester: '1',
    academicYear: '2023-2024',
    gpa: '3.5',
    credits: '15',
    classification: 'Giỏi'
  },
  // Add more semesters here
])
</script>

<style scoped>
.student-profile {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.profile-card {
  margin-bottom: 20px;
}

.mt-4 {
  margin-top: 1rem;
}
</style>