<template>
    <div class="min-h-screen bg-gray-50 pt-20 px-4 md:px-6 pb-6">
        <!-- Header Section -->
        <div class="mb-8">
            <h1 class="text-3xl font-bold text-gray-900 mb-2">Thông tin cá nhân</h1>
            <template>
                <div class="min-h-screen bg-gray-50 pt-20 px-4 md:px-6 pb-6">
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
                                </div>
                                <div class="text-3xl font-bold text-purple-600 mb-2">{{ progressPercentage }}%</div>
                                <div class="text-gray-600">Tiến độ</div>
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
                            <el-form-item label="Giới tính">
                                <el-select v-model="editingInfo.gender" placeholder="Chọn giới tính">
                                    <el-option label="Nam" value="male" />
                                    <el-option label="Nữ" value="female" />
                                    <el-option label="Khác" value="other" />
                                </el-select>
                            </el-form-item>
                            <el-form-item label="Số điện thoại">
                                <template>
                                    <div class="min-h-screen bg-gray-50 pt-20 px-4 md:px-6 pb-6">
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
                                                    </div>
                                                    <div class="text-3xl font-bold text-purple-600 mb-2">{{ progressPercentage }}%</div>
                                                    <div class="text-gray-600">Tiến độ</div>
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
                                import { useOauthStore } from '@/stores/oauth'
                                import AcademicService from '@/services/websites/academic'

                                definePageMeta({ layout: 'websites' })

                                const showEditDialog = ref(false)
                                const studentInfo = ref<any>({ fullName: '', studentId: '', profilePicture: '', completed_credits: 0, total_credits: 0 })
                                const editingInfo = ref<any>({})

                                const completedCredits = ref(0)
                                const totalCredits = ref(0)
                                const progressPercentage = computed(() => totalCredits.value ? Math.round((completedCredits.value / totalCredits.value) * 100) : 0)

                                const oauth = useOauthStore()

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
