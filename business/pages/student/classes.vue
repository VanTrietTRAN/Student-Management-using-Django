<template>
  <div class="classes">
    <el-card class="current-classes">
      <template #header>
        <div class="card-header">
          <span>{{ $t('Danh sách lớp học') }}</span>
        </div>
      </template>

      <el-table :data="classes" style="width: 100%">
        <el-table-column :label="$t('Mã lớp')" prop="classCode" />
        <el-table-column :label="$t('Tên học phần')" prop="courseName" />
        <el-table-column :label="$t('Giảng viên')" prop="teacherName" />
        <el-table-column :label="$t('Phòng học')" prop="room" />
        <el-table-column :label="$t('Thời gian')" prop="schedule" />
        <el-table-column :label="$t('Tài liệu')" width="150">
          <template #default="{ row }">
            <el-button @click="showMaterials(row)" type="primary" link>
              {{ $t('Xem tài liệu') }}
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- Materials Dialog -->
    <el-dialog
      v-model="materialsDialogVisible"
      :title="$t('Tài liệu học tập')"
      width="70%"
    >
      <el-table :data="currentMaterials" style="width: 100%">
        <el-table-column :label="$t('Tên tài liệu')" prop="title" />
        <el-table-column :label="$t('Loại')" prop="type" width="120">
          <template #default="{ row }">
            <el-tag>{{ getMaterialTypeText(row.type) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column :label="$t('Ngày tải lên')" prop="uploadDate" width="150" />
        <el-table-column :label="$t('Tải xuống')" width="100">
          <template #default="{ row }">
            <el-button @click="downloadMaterial(row)" type="primary" link>
              {{ $t('Tải xuống') }}
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const classes = ref([
  {
    id: 1,
    classCode: 'WEB101',
    courseName: 'Lập trình Web',
    teacherName: 'Nguyễn Văn A',
    room: 'A101',
    schedule: 'Thứ 2 (7:00 - 9:00)'
  },
  {
    id: 2,
    classCode: 'DB102',
    courseName: 'Cơ sở dữ liệu',
    teacherName: 'Trần Thị B',
    room: 'B202',
    schedule: 'Thứ 3 (13:00 - 15:00)'
  }
])

const materialsDialogVisible = ref(false)
const currentMaterials = ref([])

const showMaterials = (classData) => {
  currentMaterials.value = [
    {
      title: 'Đề cương môn học',
      type: 'syllabus',
      uploadDate: '2023-09-01',
      url: '#'
    },
    {
      title: 'Bài giảng tuần 1',
      type: 'lecture',
      uploadDate: '2023-09-05',
      url: '#'
    },
    {
      title: 'Bài tập số 1',
      type: 'assignment',
      uploadDate: '2023-09-07',
      url: '#'
    }
  ]
  materialsDialogVisible.value = true
}

const getMaterialTypeText = (type: string) => {
  const types = {
    syllabus: 'Đề cương',
    lecture: 'Bài giảng',
    assignment: 'Bài tập',
    reading: 'Tài liệu đọc',
    other: 'Khác'
  }
  return types[type] || type
}

const downloadMaterial = (material) => {
  // Download logic here
  window.open(material.url, '_blank')
}
</script>

<style scoped>
.classes {
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