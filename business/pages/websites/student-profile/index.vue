<template>
<<<<<<< HEAD
    <div class="min-h-screen bg-gray-50 pt-20 px-4 md:px-6 pb-6">
=======
    <div class="min-h-screen bg-gray-50 pt-32 px-4 md:px-6 pb-6">
        <!-- Header Section -->
>>>>>>> 3b3381a6d34ff10ab244e9176bf5c5305c89c0c0
        <div class="mb-8">
            <h1 class="text-3xl font-bold text-gray-900 mb-2">Thông tin cá nhân</h1>
            <p class="text-gray-600">Xem và cập nhật thông tin cá nhân</p>
        </div>

        <div class="max-w-4xl mx-auto">
            <div class="bg-white rounded-lg shadow-md p-8 mb-6">
                <div class="flex flex-col md:flex-row items-center space-y-6 md:space-y-0 md:space-x-8">
                    <div class="flex-shrink-0">
                        <img :src="studentInfo.profilePicture || '/default-avatar.png'" :alt="studentInfo.fullName" class="w-32 h-32 rounded-full object-cover border-4 border-gray-200" />
                    </div>
                    <div class="flex-1">
                        <h2 class="text-xl font-semibold">{{ studentInfo.fullName }}</h2>
                        <p class="text-sm text-gray-600">{{ studentInfo.studentId }}</p>
                        <div class="mt-4">
                            <el-button size="small" type="primary" @click="showEditDialog = true">Chỉnh sửa</el-button>
                        </div>
<<<<<<< HEAD
                    </div>
                    <div class="text-3xl font-bold text-purple-600 mb-2">{{ progressPercentage }}%</div>
                    <div class="text-gray-600">Tiến độ</div>
=======
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
>>>>>>> 3b3381a6d34ff10ab244e9176bf5c5305c89c0c0
                </div>
                <div class="mt-4">
                    <el-progress :percentage="progressPercentage" :color="getProgressColor(progressPercentage)" />
                </div>
            </div>
        </div>

        <el-dialog v-model="showEditDialog" title="Chỉnh sửa thông tin cá nhân" width="600px">
            <el-form :model="editingInfo" label-width="120px">
                <el-form-item label="Họ và tên">
                    <el-input v-model="editingInfo.fullName" />
                </el-form-item>
                <el-form-item label="Email">
                    <el-input v-model="editingInfo.email" type="email" />
                </el-form-item>
                <el-form-item label="Giới tính">
                    <el-select v-model="editingInfo.gender" placeholder="Chọn giới tính">
                        <el-option label="Nam" value="male" />
                        <el-option label="Nữ" value="female" />
                        <el-option label="Khác" value="other" />
                    </el-select>
                </el-form-item>
                <el-form-item label="Số điện thoại">
                    <el-input v-model="editingInfo.phone" />
                </el-form-item>
                <el-form-item label="Ngày sinh">
                    <el-input v-model="editingInfo.dateOfBirth" />
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button @click="showEditDialog = false">Hủy</el-button>
                <el-button type="primary" @click="updateProfile">Lưu</el-button>
            </template>
        </el-dialog>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
<<<<<<< HEAD
import { useOauthStore } from '@/stores/oauth'
import AcademicService from '@/services/websites/academic'
=======
import { Camera as IconCamera } from '@element-plus/icons-vue'
>>>>>>> 3b3381a6d34ff10ab244e9176bf5c5305c89c0c0

definePageMeta({ layout: 'websites' })

const showEditDialog = ref(false)
const studentInfo = ref<any>({ fullName: '', studentId: '', profilePicture: '', completed_credits: 0, total_credits: 0 })
const editingInfo = ref<any>({})

const completedCredits = ref(0)
const totalCredits = ref(0)
const progressPercentage = computed(() => totalCredits.value ? Math.round((completedCredits.value / totalCredits.value) * 100) : 0)

const oauth = useOauthStore()

<<<<<<< HEAD
onMounted(async () => {
    const userId = oauth.userId
    if (userId) {
        try {
            const res = await AcademicService.getStudent(userId)
            const data = res && res.data ? res.data : res
            studentInfo.value = data || studentInfo.value
            editingInfo.value = { ...studentInfo.value }
            completedCredits.value = data?.completed_credits || 0
            totalCredits.value = data?.total_credits || 0
        } catch (err) {
            ElMessage.error('Không thể tải thông tin cá nhân')
            console.error(err)
        }
=======
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
>>>>>>> 3b3381a6d34ff10ab244e9176bf5c5305c89c0c0
    }
})

const getProgressColor = (percentage: number) => {
    if (percentage >= 80) return '#10B981'
    if (percentage >= 60) return '#3B82F6'
    if (percentage >= 40) return '#F59E0B'
    return '#EF4444'
}

const updateProfile = async () => {
    try {
        if (studentInfo.value.id) {
            await AcademicService.updateStudent(studentInfo.value.id, editingInfo.value)
        }
        Object.assign(studentInfo.value, editingInfo.value)
        showEditDialog.value = false
        ElMessage.success('Cập nhật thông tin thành công')
    } catch (err) {
        ElMessage.error('Cập nhật thất bại')
        console.error(err)
    }
}
</script>

<style scoped>
.el-table {
    font-size: 14px;
}
</style>

