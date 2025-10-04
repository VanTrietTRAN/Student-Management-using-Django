<template>
  <div class="container mx-auto py-8 mt-20">
    <h1 class="text-2xl font-bold mb-4">Thông tin sinh viên</h1>
    <el-card>
      <el-form label-position="top" label-width="120px" :model="student" class="w-full grid grid-cols-1 md:grid-cols-2 gap-x-8">
        <el-form-item label="Mã sinh viên">
          <el-input v-model="student.id" disabled />
        </el-form-item>
        <el-form-item label="Họ và tên">
          <el-input v-model="student.name" />
        </el-form-item>
        <el-form-item label="Email">
          <el-input v-model="student.email" />
        </el-form-item>
        <el-form-item label="Số điện thoại">
          <el-input v-model="student.phone" />
        </el-form-item>
        <el-form-item label="Lớp">
          <el-input v-model="student.classroom" />
        </el-form-item>
        <el-form-item label="Ngành">
          <el-input v-model="student.major" />
        </el-form-item>
        <el-form-item label="Trạng thái">
          <el-select v-model="student.status" placeholder="Chọn trạng thái">
            <el-option label="Đang học" value="Đang học" />
            <el-option label="Đã tốt nghiệp" value="Đã tốt nghiệp" />
            <el-option label="Tạm nghỉ" value="Tạm nghỉ" />
            <el-option label="Đã xóa" value="Đã xóa" />
          </el-select>
        </el-form-item>
        <el-form-item label="Điểm TB">
          <el-input-number v-model="student.gpa" :min="0" :max="10" step="0.1" />
        </el-form-item>
        <el-form-item label="Ảnh thẻ">
          <el-upload
            class="avatar-uploader"
            action="#"
            :show-file-list="false"
            :on-change="handleAvatarChange"
          >
            <el-button>Chọn ảnh</el-button>
            <span class="ml-2">{{ student.avatarName }}</span>
          </el-upload>
        </el-form-item>
        <el-form-item class="col-span-2 flex gap-2">
          <el-button type="primary" @click="updateStudent">Cập nhật</el-button>
          <el-button @click="resetForm">Hủy</el-button>
          <el-button type="danger" @click="deleteStudent">Xóa</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const student = ref({
  id: 'SV001',
  name: 'Nguyễn Văn An',
  email: 'an.nguyen@email.com',
  phone: '0123456789',
  classroom: 'CNTT21A',
  major: 'Công nghệ thông tin',
  status: 'Đang học',
  gpa: 8.5,
  avatarName: '',
})
function handleAvatarChange(file) {
  student.value.avatarName = file.name
}
function updateStudent() {
  // TODO: Gọi API cập nhật thông tin
  alert('Đã cập nhật thông tin!')
}
function resetForm() {
  // TODO: Reset về thông tin ban đầu
  window.location.reload()
}
function deleteStudent() {
  // TODO: Gọi API xóa sinh viên hoặc reset dữ liệu demo
  Object.keys(student.value).forEach(key => student.value[key] = '')
  student.value.status = 'Đã xóa'
  student.value.gpa = 0
  alert('Đã xóa sinh viên!')
}
</script>

<style scoped>
.avatar-uploader {
  display: flex;
  align-items: center;
}
.avatar-uploader .el-button {
  margin-right: 10px;
}
</style>
