<template>
    <div class="min-h-screen bg-gray-50 pt-20 px-4 md:px-6 pb-6">
        <!-- Header Section -->
        <div class="mb-8">
            <h1 class="text-3xl font-bold text-gray-900 mb-2">Hệ thống thông tin sinh viên</h1>
            <p class="text-gray-600">Quản lý toàn bộ thông tin sinh viên, lớp học, điểm số và các hoạt động học tập</p>
        </div>

        <!-- Statistics Cards -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-blue-500">
                <div class="flex items-center">
                    <div class="p-3 bg-blue-100 rounded-full">
                        <IconUsers class="w-8 h-8 text-blue-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Tổng sinh viên</p>
                        <p class="text-2xl font-bold text-gray-900">2,847</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-green-500">
                <div class="flex items-center">
                    <div class="p-3 bg-green-100 rounded-full">
                        <IconCalendar class="w-8 h-8 text-green-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Lớp học</p>
                        <p class="text-2xl font-bold text-gray-900">156</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-purple-500">
                <div class="flex items-center">
                    <div class="p-3 bg-purple-100 rounded-full">
                        <IconFile class="w-8 h-8 text-purple-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Môn học</p>
                        <p class="text-2xl font-bold text-gray-900">89</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-orange-500">
                <div class="flex items-center">
                    <div class="p-3 bg-orange-100 rounded-full">
                        <IconAppraisal class="w-8 h-8 text-orange-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Điểm TB</p>
                        <p class="text-2xl font-bold text-gray-900">8.2</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Quick Actions -->
        <div class="mb-8">
            <h2 class="text-xl font-semibold text-gray-900 mb-4">Truy cập nhanh</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <NuxtLink to="/websites/students" class="group">
                    <div class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow duration-200 border border-gray-200 hover:border-blue-300">
                        <div class="flex items-center">
                            <div class="p-3 bg-blue-100 rounded-full group-hover:bg-blue-200 transition-colors">
                                <IconUsers class="w-8 h-8 text-blue-600" />
                            </div>
                            <div class="ml-4">
                                <h3 class="text-lg font-semibold text-gray-900">Quản lý sinh viên</h3>
                                <p class="text-sm text-gray-600">Hồ sơ cá nhân, quá trình học tập</p>
                            </div>
                        </div>
                    </div>
                </NuxtLink>

                <NuxtLink to="/websites/classes" class="group">
                    <div class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow duration-200 border border-gray-200 hover:border-green-300">
                        <div class="flex items-center">
                            <div class="p-3 bg-green-100 rounded-full group-hover:bg-green-200 transition-colors">
                                <IconCalendar class="w-8 h-8 text-green-600" />
                            </div>
                            <div class="ml-4">
                                <h3 class="text-lg font-semibold text-gray-900">Quản lý lớp học</h3>
                                <p class="text-sm text-gray-600">Danh sách lớp, sinh viên, giảng viên</p>
                            </div>
                        </div>
                    </div>
                </NuxtLink>

                <NuxtLink to="/websites/subjects" class="group">
                    <div class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow duration-200 border border-gray-200 hover:border-purple-300">
                        <div class="flex items-center">
                            <div class="p-3 bg-purple-100 rounded-full group-hover:bg-purple-200 transition-colors">
                                <IconFile class="w-8 h-8 text-purple-600" />
                            </div>
                            <div class="ml-4">
                                <h3 class="text-lg font-semibold text-gray-900">Quản lý môn học</h3>
                                <p class="text-sm text-gray-600">Thông tin môn học, chương trình đào tạo</p>
                            </div>
                        </div>
                    </div>
                </NuxtLink>

                <NuxtLink to="/websites/grades" class="group">
                    <div class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow duration-200 border border-gray-200 hover:border-orange-300">
                        <div class="flex items-center">
                            <div class="p-3 bg-orange-100 rounded-full group-hover:bg-orange-200 transition-colors">
                                <IconAppraisal class="w-8 h-8 text-orange-600" />
                            </div>
                            <div class="ml-4">
                                <h3 class="text-lg font-semibold text-gray-900">Quản lý điểm số</h3>
                                <p class="text-sm text-gray-600">Nhập điểm, xem điểm, thống kê</p>
                            </div>
                        </div>
                    </div>
                </NuxtLink>

                <NuxtLink to="/websites/schedule" class="group">
                    <div class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow duration-200 border border-gray-200 hover:border-indigo-300">
                        <div class="flex items-center">
                            <div class="p-3 bg-indigo-100 rounded-full group-hover:bg-indigo-200 transition-colors">
                                <IconCalendar class="w-8 h-8 text-indigo-600" />
                            </div>
                            <div class="ml-4">
                                <h3 class="text-lg font-semibold text-gray-900">Lịch học & thi</h3>
                                <p class="text-sm text-gray-600">Thời khóa biểu, lịch thi, phòng học</p>
                            </div>
                        </div>
                    </div>
                </NuxtLink>

                <NuxtLink to="/websites/tuition" class="group">
                    <div class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow duration-200 border border-gray-200 hover:border-red-300">
                        <div class="flex items-center">
                            <div class="p-3 bg-red-100 rounded-full group-hover:bg-red-200 transition-colors">
                                <IconFile class="w-8 h-8 text-red-600" />
                            </div>
                            <div class="ml-4">
                                <h3 class="text-lg font-semibold text-gray-900">Quản lý học phí</h3>
                                <p class="text-sm text-gray-600">Tra cứu, đóng học phí, lịch sử</p>
                            </div>
                        </div>
                    </div>
                </NuxtLink>
            </div>
        </div>

        <!-- Recent Activities -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- Recent Notifications -->
            <div class="bg-white rounded-lg shadow-md p-6">
                <h3 class="text-lg font-semibold text-gray-900 mb-4">Thông báo mới nhất</h3>
                <div class="space-y-4">
                    <div class="flex items-start space-x-3 p-3 bg-blue-50 rounded-lg">
                        <div class="w-2 h-2 bg-blue-500 rounded-full mt-2"></div>
                        <div>
                            <p class="text-sm font-medium text-gray-900">Lịch thi cuối kỳ học kỳ 1</p>
                            <p class="text-xs text-gray-600">2 giờ trước</p>
                        </div>
                    </div>
                    <div class="flex items-start space-x-3 p-3 bg-green-50 rounded-lg">
                        <div class="w-2 h-2 bg-green-500 rounded-full mt-2"></div>
                        <div>
                            <p class="text-sm font-medium text-gray-900">Đăng ký môn học tự chọn</p>
                            <p class="text-xs text-gray-600">1 ngày trước</p>
                        </div>
                    </div>
                    <div class="flex items-start space-x-3 p-3 bg-yellow-50 rounded-lg">
                        <div class="w-2 h-2 bg-yellow-500 rounded-full mt-2"></div>
                        <div>
                            <p class="text-sm font-medium text-gray-900">Thông báo nghỉ lễ</p>
                            <p class="text-xs text-gray-600">3 ngày trước</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Quick Stats -->
            <div class="bg-white rounded-lg shadow-md p-6">
                <h3 class="text-lg font-semibold text-gray-900 mb-4">Thống kê nhanh</h3>
                <div class="space-y-4">
                    <div class="flex justify-between items-center">
                        <span class="text-sm text-gray-600">Sinh viên mới trong tháng</span>
                        <span class="text-lg font-semibold text-blue-600">45</span>
                    </div>
                    <div class="flex justify-between items-center">
                        <span class="text-sm text-gray-600">Tỷ lệ tốt nghiệp</span>
                        <span class="text-lg font-semibold text-green-600">94.2%</span>
                    </div>
                    <div class="flex justify-between items-center">
                        <span class="text-sm text-gray-600">Sinh viên có học bổng</span>
                        <span class="text-lg font-semibold text-purple-600">156</span>
                    </div>
                    <div class="flex justify-between items-center">
                        <span class="text-sm text-gray-600">Hoạt động ngoại khóa</span>
                        <span class="text-lg font-semibold text-orange-600">23</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import IconUsers from '@/assets/icons/users.svg';
import IconCalendar from '@/assets/icons/calendar.svg';
import IconFile from '@/assets/icons/file.svg';
import IconAppraisal from '@/assets/icons/appraisal.svg';

definePageMeta({
    layout: 'websites'
})
</script>

<style scoped>
a {
    text-decoration: none;
}
</style>