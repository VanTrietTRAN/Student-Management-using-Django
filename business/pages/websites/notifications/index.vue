<template>
    <div class="min-h-screen bg-gray-50 pt-20 px-4 md:px-6 pb-6">
        <!-- Header Section -->
        <div class="mb-8">
            <div class="flex justify-between items-center">
                <div>
                    <h1 class="text-3xl font-bold text-gray-900 mb-2">Quản lý thông báo</h1>
                    <p class="text-gray-600">Tạo và gửi thông báo, quản lý theo khoa/lớp</p>
                </div>
                <el-button type="primary" :icon="Plus" @click="showAddDialog = true">
                    Tạo thông báo mới
                </el-button>
            </div>
        </div>

        <!-- Search and Filter Section -->
        <div class="bg-white rounded-lg shadow-md p-6 mb-6">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <el-input
                    v-model="searchKeyword"
                    placeholder="Tìm kiếm theo tiêu đề..."
                    :prefix-icon="Search"
                    clearable
                />
                <el-select v-model="selectedTarget" placeholder="Chọn đối tượng" clearable>
                    <el-option label="Tất cả đối tượng" value="" />
                    <el-option label="Toàn trường" value="Toàn trường" />
                    <el-option label="Khoa CNTT" value="Khoa CNTT" />
                    <el-option label="Lớp CNTT21A" value="CNTT21A" />
                </el-select>
                <el-select v-model="selectedStatus" placeholder="Chọn trạng thái" clearable>
                    <el-option label="Tất cả trạng thái" value="" />
                    <el-option label="Đã đọc" value="Đã đọc" />
                    <el-option label="Chưa đọc" value="Chưa đọc" />
                </el-select>
                <el-button type="primary" :icon="Search" @click="handleSearch">
                    Tìm kiếm
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
                        <IconUsers class="w-8 h-8 text-purple-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Tỷ lệ đọc</p>
                        <p class="text-2xl font-bold text-gray-900">{{ readRate }}%</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Notifications Table -->
        <div class="bg-white rounded-lg shadow-md">
            <div class="p-6 border-b border-gray-200">
                <h3 class="text-lg font-semibold text-gray-900">Danh sách thông báo</h3>
            </div>
            <div class="overflow-x-auto">
                <el-table :data="filteredNotifications" stripe style="width: 100%">
                    <el-table-column prop="title" label="Tiêu đề" width="250" />
                    <el-table-column prop="targetRole" label="Đối tượng" width="150" />
                    <el-table-column prop="createdAt" label="Ngày tạo" width="120" />
                    <el-table-column prop="isRead" label="Trạng thái" width="120">
                        <template #default="scope">
                            <el-tag :type="scope.row.isRead ? 'success' : 'warning'">
                                {{ scope.row.isRead ? 'Đã đọc' : 'Chưa đọc' }}
                            </el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column label="Thao tác" width="200">
                        <template #default="scope">
                            <el-button size="small" @click="viewNotification(scope.row)">
                                Xem
                            </el-button>
                            <el-button size="small" type="primary" @click="editNotification(scope.row)">
                                Sửa
                            </el-button>
                            <el-button size="small" type="danger" @click="deleteNotification(scope.row)">
                                Xóa
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
            <div class="p-4 border-t border-gray-200">
                <el-pagination
                    v-model:current-page="currentPage"
                    v-model:page-size="pageSize"
                    :page-sizes="[10, 20, 50, 100]"
                    :total="totalNotifications"
                    layout="total, sizes, prev, pager, next, jumper"
                />
            </div>
        </div>

        <!-- Add Notification Dialog -->
        <el-dialog v-model="showAddDialog" title="Tạo thông báo mới" width="600px">
            <el-form :model="newNotification" label-width="120px">
                <el-form-item label="Tiêu đề">
                    <el-input v-model="newNotification.title" />
                </el-form-item>
                <el-form-item label="Nội dung">
                    <el-input v-model="newNotification.content" type="textarea" :rows="4" />
                </el-form-item>
                <el-form-item label="Đối tượng">
                    <el-select v-model="newNotification.targetRole" placeholder="Chọn đối tượng">
                        <el-option label="Toàn trường" value="Toàn trường" />
                        <el-option label="Khoa CNTT" value="Khoa CNTT" />
                        <el-option label="Lớp CNTT21A" value="CNTT21A" />
                        <el-option label="Lớp CNTT21B" value="CNTT21B" />
                    </el-select>
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button @click="showAddDialog = false">Hủy</el-button>
                <el-button type="primary" @click="addNotification">Tạo</el-button>
            </template>
        </el-dialog>

        <!-- View Notification Dialog -->
        <el-dialog v-model="showViewDialog" title="Chi tiết thông báo" width="800px">
            <div v-if="selectedNotification" class="space-y-4">
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Tiêu đề</label>
                        <p class="mt-1 text-sm text-gray-900 font-bold">{{ selectedNotification.title }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Đối tượng</label>
                        <p class="mt-1 text-sm text-gray-900">{{ selectedNotification.targetRole }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Ngày tạo</label>
                        <p class="mt-1 text-sm text-gray-900">{{ selectedNotification.createdAt }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Trạng thái</label>
                        <el-tag :type="selectedNotification.isRead ? 'success' : 'warning'">
                            {{ selectedNotification.isRead ? 'Đã đọc' : 'Chưa đọc' }}
                        </el-tag>
                    </div>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700">Nội dung</label>
                    <div class="mt-1 p-4 bg-gray-50 rounded-lg">
                        <p class="text-sm text-gray-900 whitespace-pre-wrap">{{ selectedNotification.content }}</p>
                    </div>
                </div>
            </div>
            <template #footer>
                <el-button @click="showViewDialog = false">Đóng</el-button>
                <el-button type="primary" @click="editNotificationFromView">Chỉnh sửa</el-button>
                <el-button v-if="!selectedNotification?.isRead" type="success" @click="markAsRead">
                    Đánh dấu đã đọc
                </el-button>
            </template>
        </el-dialog>

        <!-- Edit Notification Dialog -->
        <el-dialog v-model="showEditDialog" title="Chỉnh sửa thông báo" width="600px">
            <el-form :model="editingNotification" label-width="120px">
                <el-form-item label="Tiêu đề">
                    <el-input v-model="editingNotification.title" />
                </el-form-item>
                <el-form-item label="Nội dung">
                    <el-input v-model="editingNotification.content" type="textarea" :rows="4" />
                </el-form-item>
                <el-form-item label="Đối tượng">
                    <el-select v-model="editingNotification.targetRole" placeholder="Chọn đối tượng">
                        <el-option label="Toàn trường" value="Toàn trường" />
                        <el-option label="Khoa CNTT" value="Khoa CNTT" />
                        <el-option label="Lớp CNTT21A" value="CNTT21A" />
                        <el-option label="Lớp CNTT21B" value="CNTT21B" />
                    </el-select>
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button @click="showEditDialog = false">Hủy</el-button>
                <el-button type="primary" @click="updateNotification">Cập nhật</el-button>
            </template>
        </el-dialog>
    </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Plus, Search } from '@element-plus/icons-vue';
import IconBulb from '@/assets/icons/bulb.svg';
import IconUsers from '@/assets/icons/users.svg';

definePageMeta({
    layout: 'websites'
});

// Reactive data
const searchKeyword = ref('');
const selectedTarget = ref('');
const selectedStatus = ref('');
const currentPage = ref(1);
const pageSize = ref(20);
const showAddDialog = ref(false);
const showViewDialog = ref(false);
const showEditDialog = ref(false);
const selectedNotification = ref(null);
const editingNotification = ref({});

const newNotification = ref({
    title: '',
    content: '',
    targetRole: ''
});

// Mock data
const notifications = ref([
    {
        id: 1,
        title: 'Thông báo lịch thi cuối kỳ',
        content: 'Kỳ thi cuối kỳ sẽ diễn ra từ ngày 15/01/2024 đến 25/01/2024. Sinh viên vui lòng chuẩn bị đầy đủ giấy tờ và đến đúng giờ.',
        targetRole: 'Toàn trường',
        createdAt: '2024-01-10',
        isRead: true
    },
    {
        id: 2,
        title: 'Cập nhật học phí học kỳ mới',
        content: 'Học phí học kỳ 2 năm học 2023-2024 đã được cập nhật. Sinh viên vui lòng đóng học phí trước ngày 15/02/2024.',
        targetRole: 'Khoa CNTT',
        createdAt: '2024-01-08',
        isRead: false
    },
    {
        id: 3,
        title: 'Thông báo nghỉ lễ 30/4',
        content: 'Nhà trường thông báo nghỉ lễ 30/4 và 1/5. Các lớp học sẽ được điều chỉnh lịch học phù hợp.',
        targetRole: 'Toàn trường',
        createdAt: '2024-01-05',
        isRead: true
    }
]);

// Computed properties
const totalNotifications = computed(() => notifications.value.length);
const readNotifications = computed(() => notifications.value.filter(n => n.isRead).length);
const unreadNotifications = computed(() => notifications.value.filter(n => !n.isRead).length);
const readRate = computed(() => {
    if (totalNotifications.value === 0) return 0;
    return Math.round((readNotifications.value / totalNotifications.value) * 100);
});

const filteredNotifications = computed(() => {
    let filtered = notifications.value;
    
    if (searchKeyword.value) {
        filtered = filtered.filter(notification => 
            notification.title.toLowerCase().includes(searchKeyword.value.toLowerCase())
        );
    }
    
    if (selectedTarget.value) {
        filtered = filtered.filter(notification => notification.targetRole === selectedTarget.value);
    }
    
    if (selectedStatus.value) {
        const isRead = selectedStatus.value === 'Đã đọc';
        filtered = filtered.filter(notification => notification.isRead === isRead);
    }
    
    return filtered;
});

// Methods
const handleSearch = () => {
    ElMessage.success('Tìm kiếm hoàn tất');
};

const viewNotification = (notification: any) => {
    selectedNotification.value = notification;
    showViewDialog.value = true;
};

const editNotification = (notification: any) => {
    editingNotification.value = { ...notification };
    showEditDialog.value = true;
};

const editNotificationFromView = () => {
    showViewDialog.value = false;
    editingNotification.value = { ...selectedNotification.value };
    showEditDialog.value = true;
};

const updateNotification = () => {
    const index = notifications.value.findIndex(n => n.id === editingNotification.value.id);
    if (index > -1) {
        notifications.value[index] = { ...editingNotification.value };
        showEditDialog.value = false;
        ElMessage.success(`Cập nhật thông báo: ${editingNotification.value.title}`);
    }
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

const markAsRead = () => {
    if (selectedNotification.value) {
        const index = notifications.value.findIndex(n => n.id === selectedNotification.value.id);
        if (index > -1) {
            notifications.value[index].isRead = true;
            selectedNotification.value.isRead = true;
            ElMessage.success('Đã đánh dấu đã đọc');
        }
    }
};

const addNotification = () => {
    if (newNotification.value.title && newNotification.value.content) {
        notifications.value.push({
            id: notifications.value.length + 1,
            ...newNotification.value,
            createdAt: new Date().toISOString().split('T')[0],
            isRead: false
        });
        showAddDialog.value = false;
        newNotification.value = {
            title: '',
            content: '',
            targetRole: ''
        };
        ElMessage.success('Tạo thông báo thành công');
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