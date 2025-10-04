<template>
    <div class="min-h-screen bg-gray-50 pt-20 px-4 md:px-6 pb-6">
        <!-- Header Section -->
        <div class="mb-8">
            <div class="flex justify-between items-center">
                <div>
                    <h1 class="text-3xl font-bold text-gray-900 mb-2">Lịch học & thi</h1>
                    <p class="text-gray-600">Quản lý lịch học, lịch thi và thời khóa biểu</p>
                </div>
                <el-button type="primary" :icon="Plus" @click="showAddDialog = true">
                    Thêm lịch mới
                </el-button>
            </div>
        </div>

        <!-- Search and Filter Section -->
        <div class="bg-white rounded-lg shadow-md p-6 mb-6">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <el-input
                    v-model="searchKeyword"
                    placeholder="Tìm kiếm theo tên lớp, môn học..."
                    :prefix-icon="Search"
                    clearable
                />
                <el-select v-model="selectedType" placeholder="Chọn loại" clearable>
                    <el-option label="Tất cả loại" value="" />
                    <el-option label="Lịch học" value="Lịch học" />
                    <el-option label="Lịch thi" value="Lịch thi" />
                </el-select>
                <el-select v-model="selectedClass" placeholder="Chọn lớp" clearable>
                    <el-option label="Tất cả lớp" value="" />
                    <el-option label="CNTT21A" value="CNTT21A" />
                    <el-option label="CNTT21B" value="CNTT21B" />
                    <el-option label="CNTT22A" value="CNTT22A" />
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
                        <IconCalendar class="w-8 h-8 text-blue-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Tổng lịch</p>
                        <p class="text-2xl font-bold text-gray-900">{{ totalSchedules }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-green-500">
                <div class="flex items-center">
                    <div class="p-3 bg-green-100 rounded-full">
                        <IconCalendar class="w-8 h-8 text-green-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Lịch học</p>
                        <p class="text-2xl font-bold text-gray-900">{{ studySchedules }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-red-500">
                <div class="flex items-center">
                    <div class="p-3 bg-red-100 rounded-full">
                        <IconCalendar class="w-8 h-8 text-red-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Lịch thi</p>
                        <p class="text-2xl font-bold text-gray-900">{{ examSchedules }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-orange-500">
                <div class="flex items-center">
                    <div class="p-3 bg-orange-100 rounded-full">
                        <IconUsers class="w-8 h-8 text-orange-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Lớp đang học</p>
                        <p class="text-2xl font-bold text-gray-900">{{ activeClasses }}</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Schedules Table -->
        <div class="bg-white rounded-lg shadow-md">
            <div class="p-6 border-b border-gray-200">
                <h3 class="text-lg font-semibold text-gray-900">Danh sách lịch học & thi</h3>
            </div>
            <div class="overflow-x-auto">
                <el-table :data="filteredSchedules" stripe style="width: 100%">
                    <el-table-column prop="className" label="Lớp" width="120" />
                    <el-table-column prop="subjectName" label="Môn học" width="180" />
                    <el-table-column prop="type" label="Loại" width="100">
                        <template #default="scope">
                            <el-tag :type="getTypeColor(scope.row.type)">
                                {{ scope.row.type }}
                            </el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column prop="date" label="Ngày" width="120" />
                    <el-table-column prop="time" label="Thời gian" width="120" />
                    <el-table-column prop="room" label="Phòng" width="100" />
                    <el-table-column prop="teacherName" label="Giảng viên" width="180" />
                    <el-table-column prop="status" label="Trạng thái" width="120">
                        <template #default="scope">
                            <el-tag :type="getStatusType(scope.row.status)">
                                {{ scope.row.status }}
                            </el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column label="Thao tác" width="200">
                        <template #default="scope">
                            <el-button size="small" @click="viewSchedule(scope.row)">
                                Xem
                            </el-button>
                            <el-button size="small" type="primary" @click="editSchedule(scope.row)">
                                Sửa
                            </el-button>
                            <el-button size="small" type="danger" @click="deleteSchedule(scope.row)">
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
                    :total="totalSchedules"
                    layout="total, sizes, prev, pager, next, jumper"
                />
            </div>
        </div>

        <!-- Add Schedule Dialog -->
        <el-dialog v-model="showAddDialog" title="Thêm lịch mới" width="600px">
            <el-form :model="newSchedule" label-width="120px">
                <el-form-item label="Lớp">
                    <el-select v-model="newSchedule.className" placeholder="Chọn lớp">
                        <el-option label="CNTT21A" value="CNTT21A" />
                        <el-option label="CNTT21B" value="CNTT21B" />
                        <el-option label="CNTT22A" value="CNTT22A" />
                    </el-select>
                </el-form-item>
                <el-form-item label="Môn học">
                    <el-select v-model="newSchedule.subjectName" placeholder="Chọn môn học">
                        <el-option label="Lập trình cơ bản" value="Lập trình cơ bản" />
                        <el-option label="Cấu trúc dữ liệu" value="Cấu trúc dữ liệu" />
                        <el-option label="Phát triển phần mềm" value="Phát triển phần mềm" />
                    </el-select>
                </el-form-item>
                <el-form-item label="Loại">
                    <el-select v-model="newSchedule.type" placeholder="Chọn loại">
                        <el-option label="Lịch học" value="Lịch học" />
                        <el-option label="Lịch thi" value="Lịch thi" />
                    </el-select>
                </el-form-item>
                <el-form-item label="Ngày">
                    <el-date-picker v-model="newSchedule.date" type="date" placeholder="Chọn ngày" />
                </el-form-item>
                <el-form-item label="Thời gian">
                    <el-time-picker v-model="newSchedule.time" placeholder="Chọn thời gian" />
                </el-form-item>
                <el-form-item label="Phòng">
                    <el-input v-model="newSchedule.room" />
                </el-form-item>
                <el-form-item label="Giảng viên">
                    <el-input v-model="newSchedule.teacherName" />
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button @click="showAddDialog = false">Hủy</el-button>
                <el-button type="primary" @click="addSchedule">Thêm</el-button>
            </template>
        </el-dialog>

        <!-- View Schedule Dialog -->
        <el-dialog v-model="showViewDialog" title="Chi tiết lịch" width="800px">
            <div v-if="selectedSchedule" class="space-y-4">
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Lớp</label>
                        <p class="mt-1 text-sm text-gray-900">{{ selectedSchedule.className }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Môn học</label>
                        <p class="mt-1 text-sm text-gray-900">{{ selectedSchedule.subjectName }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Loại</label>
                        <el-tag :type="getTypeColor(selectedSchedule.type)">
                            {{ selectedSchedule.type }}
                        </el-tag>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Ngày</label>
                        <p class="mt-1 text-sm text-gray-900">{{ selectedSchedule.date }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Thời gian</label>
                        <p class="mt-1 text-sm text-gray-900">{{ selectedSchedule.time }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Phòng</label>
                        <p class="mt-1 text-sm text-gray-900">{{ selectedSchedule.room }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Giảng viên</label>
                        <p class="mt-1 text-sm text-gray-900">{{ selectedSchedule.teacherName }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Trạng thái</label>
                        <el-tag :type="getStatusType(selectedSchedule.status)">
                            {{ selectedSchedule.status }}
                        </el-tag>
                    </div>
                </div>
            </div>
            <template #footer>
                <el-button @click="showViewDialog = false">Đóng</el-button>
                <el-button type="primary" @click="editScheduleFromView">Chỉnh sửa</el-button>
            </template>
        </el-dialog>

        <!-- Edit Schedule Dialog -->
        <el-dialog v-model="showEditDialog" title="Chỉnh sửa lịch" width="600px">
            <el-form :model="editingSchedule" label-width="120px">
                <el-form-item label="Lớp">
                    <el-input v-model="editingSchedule.className" disabled />
                </el-form-item>
                <el-form-item label="Môn học">
                    <el-input v-model="editingSchedule.subjectName" disabled />
                </el-form-item>
                <el-form-item label="Loại">
                    <el-select v-model="editingSchedule.type" placeholder="Chọn loại">
                        <el-option label="Lịch học" value="Lịch học" />
                        <el-option label="Lịch thi" value="Lịch thi" />
                    </el-select>
                </el-form-item>
                <el-form-item label="Ngày">
                    <el-date-picker v-model="editingSchedule.date" type="date" placeholder="Chọn ngày" />
                </el-form-item>
                <el-form-item label="Thời gian">
                    <el-time-picker v-model="editingSchedule.time" placeholder="Chọn thời gian" />
                </el-form-item>
                <el-form-item label="Phòng">
                    <el-input v-model="editingSchedule.room" />
                </el-form-item>
                <el-form-item label="Giảng viên">
                    <el-input v-model="editingSchedule.teacherName" />
                </el-form-item>
                <el-form-item label="Trạng thái">
                    <el-select v-model="editingSchedule.status" placeholder="Chọn trạng thái">
                        <el-option label="Đang diễn ra" value="Đang diễn ra" />
                        <el-option label="Đã kết thúc" value="Đã kết thúc" />
                        <el-option label="Tạm hoãn" value="Tạm hoãn" />
                    </el-select>
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button @click="showEditDialog = false">Hủy</el-button>
                <el-button type="primary" @click="updateSchedule">Cập nhật</el-button>
            </template>
        </el-dialog>
    </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Plus, Search } from '@element-plus/icons-vue';
import IconCalendar from '@/assets/icons/calendar.svg';
import IconUsers from '@/assets/icons/users.svg';

definePageMeta({
    layout: 'websites'
});

// Reactive data
const searchKeyword = ref('');
const selectedType = ref('');
const selectedClass = ref('');
const currentPage = ref(1);
const pageSize = ref(20);
const showAddDialog = ref(false);
const showViewDialog = ref(false);
const showEditDialog = ref(false);
const selectedSchedule = ref(null);
const editingSchedule = ref({});

const newSchedule = ref({
    className: '',
    subjectName: '',
    type: '',
    date: '',
    time: '',
    room: '',
    teacherName: ''
});

// Mock data
const schedules = ref([
    {
        id: 1,
        className: 'CNTT21A',
        subjectName: 'Lập trình cơ bản',
        type: 'Lịch học',
        date: '2024-01-15',
        time: '08:00-10:00',
        room: 'A101',
        teacherName: 'ThS. Nguyễn Văn A',
        status: 'Đang diễn ra'
    },
    {
        id: 2,
        className: 'CNTT21B',
        subjectName: 'Cấu trúc dữ liệu',
        type: 'Lịch thi',
        date: '2024-01-20',
        time: '14:00-16:00',
        room: 'A102',
        teacherName: 'TS. Trần Thị B',
        status: 'Đang diễn ra'
    },
    {
        id: 3,
        className: 'CNTT22A',
        subjectName: 'Phát triển phần mềm',
        type: 'Lịch học',
        date: '2024-01-18',
        time: '10:00-12:00',
        room: 'B201',
        teacherName: 'ThS. Lê Văn C',
        status: 'Đang diễn ra'
    }
]);

// Computed properties
const totalSchedules = computed(() => schedules.value.length);
const studySchedules = computed(() => schedules.value.filter(s => s.type === 'Lịch học').length);
const examSchedules = computed(() => schedules.value.filter(s => s.type === 'Lịch thi').length);
const activeClasses = computed(() => new Set(schedules.value.map(s => s.className)).size);

const filteredSchedules = computed(() => {
    let filtered = schedules.value;
    
    if (searchKeyword.value) {
        filtered = filtered.filter(schedule => 
            schedule.className.toLowerCase().includes(searchKeyword.value.toLowerCase()) ||
            schedule.subjectName.toLowerCase().includes(searchKeyword.value.toLowerCase())
        );
    }
    
    if (selectedType.value) {
        filtered = filtered.filter(schedule => schedule.type === selectedType.value);
    }
    
    if (selectedClass.value) {
        filtered = filtered.filter(schedule => schedule.className === selectedClass.value);
    }
    
    return filtered;
});

// Methods
const getStatusType = (status: string) => {
    switch (status) {
        case 'Đang diễn ra': return 'success';
        case 'Đã kết thúc': return 'info';
        case 'Tạm hoãn': return 'warning';
        default: return 'danger';
    }
};

const getTypeColor = (type: string) => {
    switch (type) {
        case 'Lịch học': return 'success';
        case 'Lịch thi': return 'danger';
        default: return 'info';
    }
};

const handleSearch = () => {
    ElMessage.success('Tìm kiếm hoàn tất');
};

const viewSchedule = (schedule: any) => {
    selectedSchedule.value = schedule;
    showViewDialog.value = true;
};

const editSchedule = (schedule: any) => {
    editingSchedule.value = { ...schedule };
    showEditDialog.value = true;
};

const editScheduleFromView = () => {
    showViewDialog.value = false;
    editingSchedule.value = { ...selectedSchedule.value };
    showEditDialog.value = true;
};

const updateSchedule = () => {
    const index = schedules.value.findIndex(s => s.id === editingSchedule.value.id);
    if (index > -1) {
        schedules.value[index] = { ...editingSchedule.value };
        showEditDialog.value = false;
        ElMessage.success(`Cập nhật lịch: ${editingSchedule.value.className}`);
    }
};

const deleteSchedule = (schedule: any) => {
    ElMessageBox.confirm(
        `Bạn có chắc chắn muốn xóa lịch "${schedule.className} - ${schedule.subjectName}"?`,
        'Xác nhận xóa',
        {
            confirmButtonText: 'Xóa',
            cancelButtonText: 'Hủy',
            type: 'warning',
        }
    ).then(() => {
        const index = schedules.value.findIndex(s => s.id === schedule.id);
        if (index > -1) {
            schedules.value.splice(index, 1);
            ElMessage.success(`Đã xóa lịch: ${schedule.className}`);
        }
    }).catch(() => {
        ElMessage.info('Đã hủy xóa lịch');
    });
};

const addSchedule = () => {
    if (newSchedule.value.className && newSchedule.value.subjectName) {
        schedules.value.push({
            id: schedules.value.length + 1,
            ...newSchedule.value,
            status: 'Đang diễn ra'
        });
        showAddDialog.value = false;
        newSchedule.value = {
            className: '',
            subjectName: '',
            type: '',
            date: '',
            time: '',
            room: '',
            teacherName: ''
        };
        ElMessage.success('Thêm lịch thành công');
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