<template>
    <div class="min-h-screen bg-gray-50 pt-20 px-4 md:px-6 pb-6">
        <!-- Header Section -->
        <div class="mb-8">
            <div class="flex justify-between items-center">
                <div>
                    <h1 class="text-3xl font-bold text-gray-900 mb-2">Quản lý thông báo</h1>
                    <p class="text-gray-600">Gửi, nhận thông báo và tin tức từ nhà trường</p>
                </div>
                <el-button type="primary" :icon="Plus" @click="showAddDialog = true">
                    Gửi thông báo mới
                </el-button>
            </div>
        </div>

        <!-- Statistics Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6 mb-6">
            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-blue-500">
                <div class="flex items-center">
                    <div class="p-3 bg-blue-100 rounded-full">
                        <IconBulb class="w-8 h-8 text-blue-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Tổng thông báo</p>
                        <p class="text-2xl font-bold text-gray-900">{{ totalNotifications }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-green-500">
                <div class="flex items-center">
                    <div class="p-3 bg-green-100 rounded-full">
                        <IconBulb class="w-8 h-8 text-green-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Đã đọc</p>
                        <p class="text-2xl font-bold text-gray-900">{{ readNotifications }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-orange-500">
                <div class="flex items-center">
                    <div class="p-3 bg-orange-100 rounded-full">
                        <IconBulb class="w-8 h-8 text-orange-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Chưa đọc</p>
                        <p class="text-2xl font-bold text-gray-900">{{ unreadNotifications }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-purple-500">
                <div class="flex items-center">
                    <div class="p-3 bg-purple-100 rounded-full">
                        <IconBulb class="w-8 h-8 text-purple-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Thông báo quan trọng</p>
                        <p class="text-2xl font-bold text-gray-900">{{ importantNotifications }}</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Notifications List -->
        <div class="bg-white rounded-lg shadow-md">
            <div class="p-6 border-b border-gray-200">
                <h3 class="text-lg font-semibold text-gray-900">Danh sách thông báo</h3>
            </div>
            <div class="divide-y divide-gray-200">
                <div v-for="notification in notifications" :key="notification.id" 
                     class="p-6 hover:bg-gray-50 cursor-pointer"
                     @click="viewNotification(notification)">
                    <div class="flex items-start justify-between">
                        <div class="flex-1">
                            <div class="flex items-center gap-2 mb-2">
                                <h4 class="text-lg font-medium text-gray-900">{{ notification.title }}</h4>
                                <el-tag v-if="notification.isImportant" type="danger" size="small">
                                    Quan trọng
                                </el-tag>
                                <el-tag v-if="!notification.isRead" type="warning" size="small">
                                    Mới
                                </el-tag>
                            </div>
                            <p class="text-gray-600 mb-2">{{ notification.content }}</p>
                            <div class="flex items-center gap-4 text-sm text-gray-500">
                                <span>{{ notification.sender }}</span>
                                <span>{{ notification.createdAt }}</span>
                                <span>{{ notification.target }}</span>
                            </div>
                        </div>
                        <div class="flex gap-2 ml-4">
                            <el-button size="small" @click.stop="editNotification(notification)">
                                Sửa
                            </el-button>
                            <el-button size="small" type="danger" @click.stop="deleteNotification(notification)">
                                Xóa
                            </el-button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Add Notification Dialog -->
        <el-dialog v-model="showAddDialog" title="Gửi thông báo mới" width="600px">
            <el-form :model="newNotification" label-width="120px">
                <el-form-item label="Tiêu đề">
                    <el-input v-model="newNotification.title" />
                </el-form-item>
                <el-form-item label="Nội dung">
                    <el-input v-model="newNotification.content" type="textarea" :rows="4" />
                </el-form-item>
                <el-form-item label="Người nhận">
                    <el-select v-model="newNotification.target" placeholder="Chọn đối tượng">
                        <el-option label="Tất cả sinh viên" value="Tất cả sinh viên" />
                        <el-option label="Sinh viên CNTT" value="Sinh viên CNTT" />
                        <el-option label="Sinh viên KTPM" value="Sinh viên KTPM" />
                        <el-option label="Sinh viên ATTT" value="Sinh viên ATTT" />
                    </el-select>
                </el-form-item>
                <el-form-item label="Quan trọng">
                    <el-switch v-model="newNotification.isImportant" />
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button @click="showAddDialog = false">Hủy</el-button>
                <el-button type="primary" @click="addNotification">Gửi</el-button>
            </template>
        </el-dialog>
    </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Plus } from '@element-plus/icons-vue';
import IconBulb from '@/assets/icons/bulb.svg';

definePageMeta({
    layout: 'websites'
});

const showAddDialog = ref(false);

const newNotification = ref({
    title: '',
    content: '',
    target: '',
    isImportant: false
});

// Mock data
const notifications = ref([
    {
        id: 1,
        title: 'Lịch thi cuối kỳ học kỳ 1',
        content: 'Thông báo lịch thi cuối kỳ học kỳ 1 năm học 2024-2025. Sinh viên vui lòng kiểm tra lịch thi và chuẩn bị tốt cho kỳ thi.',
        sender: 'Phòng Đào tạo',
        target: 'Tất cả sinh viên',
        createdAt: '2 giờ trước',
        isRead: false,
        isImportant: true
    },
    {
        id: 2,
        title: 'Đăng ký môn học tự chọn',
        content: 'Thời gian đăng ký môn học tự chọn học kỳ 2 từ ngày 15/12/2024 đến 20/12/2024.',
        sender: 'Phòng Đào tạo',
        target: 'Sinh viên CNTT',
        createdAt: '1 ngày trước',
        isRead: true,
        isImportant: false
    },
    {
        id: 3,
        title: 'Thông báo nghỉ lễ',
        content: 'Nhà trường thông báo nghỉ lễ Giáng sinh và Tết Dương lịch từ ngày 24/12/2024 đến 02/01/2025.',
        sender: 'Ban Giám hiệu',
        target: 'Tất cả sinh viên',
        createdAt: '3 ngày trước',
        isRead: true,
        isImportant: false
    }
]);

// Computed properties
const totalNotifications = computed(() => notifications.value.length);
const readNotifications = computed(() => notifications.value.filter(n => n.isRead).length);
const unreadNotifications = computed(() => notifications.value.filter(n => !n.isRead).length);
const importantNotifications = computed(() => notifications.value.filter(n => n.isImportant).length);

// Methods
const viewNotification = (notification: any) => {
    notification.isRead = true;
    ElMessage.info(`Đã đọc thông báo: ${notification.title}`);
};

const editNotification = (notification: any) => {
    ElMessage.info(`Chỉnh sửa thông báo: ${notification.title}`);
};

const deleteNotification = (notification: any) => {
    ElMessageBox.confirm(
        `Bạn có chắc chắn muốn xóa thông báo "${notification.title}"?`,
        'Xác nhận xóa',
        {
            confirmButtonText: 'Xóa',
            cancelButtonText: 'Hủy',
            type: 'warning',
        }
    ).then(() => {
        const index = notifications.value.findIndex(n => n.id === notification.id);
        if (index > -1) {
            notifications.value.splice(index, 1);
            ElMessage.success(`Đã xóa thông báo: ${notification.title}`);
        }
    }).catch(() => {
        ElMessage.info('Đã hủy xóa thông báo');
    });
};

const addNotification = () => {
    if (newNotification.value.title && newNotification.value.content) {
        notifications.value.unshift({
            id: notifications.value.length + 1,
            ...newNotification.value,
            sender: 'Quản trị viên',
            createdAt: 'Vừa xong',
            isRead: false
        });
        showAddDialog.value = false;
        newNotification.value = {
            title: '',
            content: '',
            target: '',
            isImportant: false
        };
        ElMessage.success('Gửi thông báo thành công');
    } else {
        ElMessage.error('Vui lòng điền đầy đủ thông tin');
    }
};
</script>

<style scoped>
.el-table {
    font-size: 14px;
}
</style>
