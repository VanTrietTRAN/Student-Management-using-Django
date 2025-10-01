&lt;template&gt;
  &lt;div class="student-profile"&gt;
    &lt;el-card class="profile-card"&gt;
      &lt;template #header&gt;
        &lt;div class="card-header"&gt;
          &lt;span&gt;{{ $t('Thông tin sinh viên') }}&lt;/span&gt;
          &lt;el-button type="primary" @click="editMode = !editMode"&gt;
            {{ editMode ? $t('Lưu') : $t('Chỉnh sửa') }}
          &lt;/el-button&gt;
        &lt;/div&gt;
      &lt;/template&gt;

      &lt;el-form 
        ref="formRef"
        :model="profileData"
        :disabled="!editMode"
        label-width="120px"
      &gt;
        &lt;el-form-item :label="$t('Mã sinh viên')"&gt;
          &lt;el-input v-model="profileData.studentId" disabled /&gt;
        &lt;/el-form-item&gt;

        &lt;el-form-item :label="$t('Họ và tên')"&gt;
          &lt;el-input v-model="profileData.fullName" /&gt;
        &lt;/el-form-item&gt;

        &lt;el-form-item :label="$t('Ngày sinh')"&gt;
          &lt;el-date-picker
            v-model="profileData.dateOfBirth"
            type="date"
            :placeholder="$t('Chọn ngày')"
          /&gt;
        &lt;/el-form-item&gt;

        &lt;el-form-item :label="$t('Email')"&gt;
          &lt;el-input v-model="profileData.email" /&gt;
        &lt;/el-form-item&gt;

        &lt;el-form-item :label="$t('Số điện thoại')"&gt;
          &lt;el-input v-model="profileData.phone" /&gt;
        &lt;/el-form-item&gt;

        &lt;el-form-item :label="$t('Địa chỉ')"&gt;
          &lt;el-input v-model="profileData.address" type="textarea" /&gt;
        &lt;/el-form-item&gt;
      &lt;/el-form&gt;
    &lt;/el-card&gt;

    &lt;el-card class="academic-history mt-4"&gt;
      &lt;template #header&gt;
        &lt;div class="card-header"&gt;
          &lt;span&gt;{{ $t('Lịch sử học tập') }}&lt;/span&gt;
        &lt;/div&gt;
      &lt;/template&gt;

      &lt;el-table :data="academicHistory" style="width: 100%"&gt;
        &lt;el-table-column :label="$t('Học kỳ')" prop="semester" /&gt;
        &lt;el-table-column :label="$t('Năm học')" prop="academicYear" /&gt;
        &lt;el-table-column :label="$t('GPA')" prop="gpa" /&gt;
        &lt;el-table-column :label="$t('Số tín chỉ')" prop="credits" /&gt;
        &lt;el-table-column :label="$t('Xếp loại')" prop="classification" /&gt;
      &lt;/el-table&gt;
    &lt;/el-card&gt;
  &lt;/div&gt;
&lt;/template&gt;

&lt;script setup lang="ts"&gt;
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
&lt;/script&gt;

&lt;style scoped&gt;
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
&lt;/style&gt;