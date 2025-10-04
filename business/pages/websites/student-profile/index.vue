<template>
    <div class="min-h-screen bg-gray-50 pt-32 px-4 md:px-6 pb-6">
        <!-- Header Section -->
        <div class="mb-8">
            <h1 class="text-3xl font-bold text-gray-900 mb-2">Thông tin cá nhân</h1>
            <p class="text-gray-600">Xem và cập nhật thông tin cá nhân</p>
        </div>

        <div class="max-w-4xl mx-auto">
            <!-- Profile Card -->
            <div class="bg-white rounded-lg shadow-md p-8 mb-6">
                <div class="flex flex-col md:flex-row items-center space-y-6 md:space-y-0 md:space-x-8">
                    <!-- Profile Picture -->
                    <div class="flex-shrink-0">
                        <div class="relative">
                            <img 
                                :src="studentInfo.profilePicture || '/default-avatar.png'" 
                                :alt="studentInfo.fullName"
                                class="w-32 h-32 rounded-full object-cover border-4 border-gray-200"
                            />
                            <button 
                                @click="showImageUpload = true"
                                class="absolute bottom-0 right-0 bg-blue-500 text-white rounded-full p-2 hover:bg-blue-600 transition-colors"
                            >
                                <IconCamera class="w-4 h-4" />
                            </button>
                        </div>
                        <div class="mt-2 text-center text-gray-400 text-sm">
                            Ảnh thẻ<br>
                            <span v-if="!studentInfo.profilePicture">Chưa có ảnh</span>
                        </div>
                    </div>
                    <!-- Student Info -->
                    <div class="flex-1">
                        <div class="grid grid-cols-2 gap-x-8 gap-y-2">
                            <div>
                                <span class="text-gray-600">Mã sinh viên</span><br>
                                <span class="font-medium">{{ studentInfo.studentId }}</span>
                            </div>
                            <div>
                                <span class="text-gray-600">Họ và tên</span><br>
                                <span class="font-medium">{{ studentInfo.fullName }}</span>
                            </div>
                            <div>
                                <span class="text-gray-600">Email</span><br>
                                <span class="font-medium">{{ studentInfo.email }}</span>
                            </div>
                            <div>
                                <span class="text-gray-600">Số điện thoại</span><br>
                                <span class="font-medium">{{ studentInfo.phone }}</span>
                            </div>
                            <div>
                                <span class="text-gray-600">Lớp</span><br>
                                <span class="font-medium">{{ studentInfo.classroom }}</span>
                            </div>
                            <div>
                                <span class="text-gray-600">Ngành</span><br>
                                <span class="font-medium">{{ studentInfo.major }}</span>
                            </div>
                            <div>
                                <span class="text-gray-600">Trạng thái</span><br>
                                <el-tag :type="getStatusType(studentInfo.status)">
                                    {{ studentInfo.status }}
                                </el-tag>
                            </div>
                            <div>
                                <span class="text-gray-600">Điểm TB</span><br>
                                <span class="font-bold text-lg" :class="getGPAClass(studentInfo.gpa)">{{ studentInfo.gpa }}</span>
                            </div>
                        </div>
                        <div class="flex gap-2 mt-6">
                            <el-button type="primary" @click="showEditDialog = true">Sửa</el-button>
                            <el-button type="danger" @click="confirmDelete">Xóa</el-button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Detailed Information -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <!-- Personal Information -->
                <div class="bg-white rounded-lg shadow-md p-6">
                    <h3 class="text-lg font-semibold text-gray-900 mb-4">Thông tin cá nhân</h3>
                    <div class="space-y-4">
                        <div class="flex justify-between">
                            <span class="text-gray-600">Họ và tên:</span>
                            <span class="font-medium">{{ studentInfo.fullName }}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-600">Mã sinh viên:</span>
                            <span class="font-medium">{{ studentInfo.studentId }}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-600">Email:</span>
                            <span class="font-medium">{{ studentInfo.email }}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-600">Số điện thoại:</span>
                            <span class="font-medium">{{ studentInfo.phone }}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-600">Ngày sinh:</span>
                            <span class="font-medium">{{ studentInfo.dateOfBirth }}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-600">Giới tính:</span>
                            <span class="font-medium">{{ studentInfo.gender }}</span>
                        </div>
                    </div>
                </div>

                <!-- Academic Information -->
                <div class="bg-white rounded-lg shadow-md p-6">
                    <h3 class="text-lg font-semibold text-gray-900 mb-4">Thông tin học tập</h3>
                    <div class="space-y-4">
                        <div class="flex justify-between">
                            <span class="text-gray-600">Lớp:</span>
                            <span class="font-medium">{{ studentInfo.classroom }}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-600">Ngành:</span>
                            <span class="font-medium">{{ studentInfo.major }}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-600">Khóa:</span>
                            <span class="font-medium">{{ studentInfo.year }}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-600">Điểm TB:</span>
                            <span class="font-bold text-lg" :class="getGPAClass(studentInfo.gpa)">
                                {{ studentInfo.gpa }}
                            </span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-600">Trạng thái:</span>
                            <el-tag :type="getStatusType(studentInfo.status)">
                                {{ studentInfo.status }}
                            </el-tag>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-600">Ngày nhập học:</span>
                            <span class="font-medium">{{ studentInfo.enrollmentDate }}</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Academic Progress -->
            <div class="bg-white rounded-lg shadow-md p-6 mt-6">
                <h3 class="text-lg font-semibold text-gray-900 mb-4">Tiến độ học tập</h3>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div class="text-center">
                        <div class="text-3xl font-bold text-blue-600 mb-2">{{ completedCredits }}</div>
                        <div class="text-gray-600">Tín chỉ đã hoàn thành</div>
                    </div>
                    <div class="text-center">
                        <div class="text-3xl font-bold text-green-600 mb-2">{{ totalCredits }}</div>
                        <div class="text-gray-600">Tổng tín chỉ</div>
                    </div>
                    <div class="text-center">
                        <div class="text-3xl font-bold text-purple-600 mb-2">{{ progressPercentage }}%</div>
                        <div class="text-gray-600">Tiến độ</div>
                    </div>
                </div>
                <div class="mt-4">
                    <el-progress :percentage="progressPercentage" :color="getProgressColor(progressPercentage)" />
                </div>
            </div>
        </div>

        <!-- Edit Profile Dialog -->
        <el-dialog v-model="showEditDialog" title="Chỉnh sửa thông tin cá nhân" width="600px">
            <el-form :model="editingInfo" label-width="120px">
                <el-form-item label="Họ và tên">
                    <el-input v-model="editingInfo.fullName" />
                </el-form-item>
                <el-form-item label="Email">
                    <el-input v-model="editingInfo.email" type="email" />
                </el-form-item>
                <el-form-item label="Số điện thoại">
                    <el-input v-model="editingInfo.phone" />
                </el-form-item>
                <el-form-item label="Ngày sinh">
                    <el-date-picker v-model="editingInfo.dateOfBirth" type="date" />
                </el-form-item>
                <el-form-item label="Giới tính">
                    <el-select v-model="editingInfo.gender" placeholder="Chọn giới tính">
                        <el-option label="Nam" value="Nam" />
                        <el-option label="Nữ" value="Nữ" />
                    </el-select>
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button @click="showEditDialog = false">Hủy</el-button>
                <el-button type="primary" @click="updateProfile">Cập nhật</el-button>
            </template>
        </el-dialog>

        <!-- Image Upload Dialog -->
        <el-dialog v-model="showImageUpload" title="Cập nhật ảnh đại diện" width="400px">
            <div class="text-center">
                <div class="mb-4">
                    <img 
                        :src="previewImage || studentInfo.profilePicture || '/default-avatar.png'" 
                        alt="Preview"
                        class="w-32 h-32 rounded-full object-cover mx-auto border-4 border-gray-200"
                    />
                </div>
                <el-upload
                    ref="uploadRef"
                    :auto-upload="false"
                    :on-change="handleImageChange"
                    :show-file-list="false"
                    accept="image/*"
                    class="mb-4"
                >
                    <el-button type="primary">Chọn ảnh</el-button>
                </el-upload>
                <p class="text-sm text-gray-500">Chọn ảnh JPG, PNG hoặc GIF (tối đa 5MB)</p>
            </div>
            <template #footer>
                <el-button @click="showImageUpload = false">Hủy</el-button>
                <el-button type="primary" @click="uploadImage">Cập nhật ảnh</el-button>
            </template>
        </el-dialog>
    </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Camera as IconCamera } from '@element-plus/icons-vue'

definePageMeta({
    layout: 'websites'
})

// Reactive data
const showEditDialog = ref(false)
const showImageUpload = ref(false)
const previewImage = ref('')
const uploadRef = ref()

const studentInfo = ref({
    fullName: 'Nguyễn Văn An',
    studentId: 'SV001',
    email: 'an.nguyen@email.com',
    phone: '0123456789',
    classroom: 'CNTT21A',
    major: 'Công nghệ thông tin',
    year: '2021',
    gpa: 8.5,
    status: 'Đang học',
    profilePicture: null,
    dateOfBirth: '2003-05-15',
    gender: 'Nam',
    enrollmentDate: '2021-09-01'
})

const editingInfo = ref({ ...studentInfo.value })

import { ElMessageBox } from 'element-plus'

const confirmDelete = () => {
    ElMessageBox.confirm(
        'Bạn có chắc chắn muốn xóa sinh viên này?',
        'Xác nhận xóa',
        {
            confirmButtonText: 'Xóa',
            cancelButtonText: 'Hủy',
            type: 'warning',
        }
    ).then(() => {
        // Xóa thông tin sinh viên (ở đây chỉ reset dữ liệu demo)
        Object.keys(studentInfo.value).forEach(key => studentInfo.value[key] = '')
        studentInfo.value.gpa = 0
        studentInfo.value.status = 'Đã xóa'
        ElMessage.success('Đã xóa sinh viên')
    }).catch(() => {
        // Hủy xóa
    })
}

const completedCredits = ref(45)
const totalCredits = ref(120)
const progressPercentage = computed(() => Math.round((completedCredits.value / totalCredits.value) * 100))

// Methods
const getStatusType = (status: string) => {
    switch (status) {
        case 'Đang học': return 'success'
        case 'Tốt nghiệp': return 'info'
        case 'Tạm nghỉ': return 'warning'
        default: return 'danger'
    }
}

const getGPAClass = (gpa: number) => {
    if (gpa >= 8.0) return 'text-green-600'
    if (gpa >= 6.5) return 'text-blue-600'
    if (gpa >= 5.0) return 'text-yellow-600'
    return 'text-red-600'
}

const getProgressColor = (percentage: number) => {
    if (percentage >= 80) return '#10B981'
    if (percentage >= 60) return '#3B82F6'
    if (percentage >= 40) return '#F59E0B'
    return '#EF4444'
}

const updateProfile = () => {
    // Update student info
    Object.assign(studentInfo.value, editingInfo.value)
    showEditDialog.value = false
    ElMessage.success('Cập nhật thông tin thành công')
}

const handleImageChange = (file: any) => {
    const reader = new FileReader()
    reader.onload = (e) => {
        previewImage.value = e.target?.result as string
    }
    reader.readAsDataURL(file.raw)
}

const uploadImage = () => {
    if (previewImage.value) {
        studentInfo.value.profilePicture = previewImage.value
        showImageUpload.value = false
        previewImage.value = ''
        ElMessage.success('Cập nhật ảnh đại diện thành công')
    } else {
        ElMessage.error('Vui lòng chọn ảnh')
    }
}
</script>

<style scoped>
.el-table {
    font-size: 14px;
}
</style>
