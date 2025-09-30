<template>
    <div class="min-h-screen bg-gray-50 pt-20 px-4 md:px-6 pb-6">
        <!-- Header Section -->
        <div class="mb-8">
            <div class="flex justify-between items-center">
                <div>
                    <h1 class="text-3xl font-bold text-gray-900 mb-2">Quản lý lớp học</h1>
                    <p class="text-gray-600">Quản lý danh sách lớp, sinh viên và giảng viên chủ nhiệm</p>
                </div>
                <el-button type="primary" :icon="Plus" @click="showAddDialog = true">
                    Thêm lớp mới
                </el-button>
            </div>
        </div>

        <!-- Search and Filter Section -->
        <div class="bg-white rounded-lg shadow-md p-6 mb-6">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <el-input
                    v-model="searchKeyword"
                    placeholder="Tìm kiếm theo tên lớp..."
                    :prefix-icon="Search"
                    clearable
                />
                <el-select v-model="selectedMajor" placeholder="Chọn ngành" clearable>
                    <el-option label="Tất cả ngành" value="" />
                    <el-option label="Công nghệ thông tin" value="CNTT" />
                    <el-option label="Kỹ thuật phần mềm" value="KTPM" />
                    <el-option label="An toàn thông tin" value="ATTT" />
                </el-select>
                <el-select v-model="selectedYear" placeholder="Chọn khóa" clearable>
                    <el-option label="Tất cả khóa" value="" />
                    <el-option label="Khóa 2021" value="2021" />
                    <el-option label="Khóa 2022" value="2022" />
                    <el-option label="Khóa 2023" value="2023" />
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
                        <p class="text-sm font-medium text-gray-600">Tổng số lớp</p>
                        <p class="text-2xl font-bold text-gray-900">{{ totalClasses }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-green-500">
                <div class="flex items-center">
                    <div class="p-3 bg-green-100 rounded-full">
                        <IconUsers class="w-8 h-8 text-green-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Tổng sinh viên</p>
                        <p class="text-2xl font-bold text-gray-900">{{ totalStudents }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-purple-500">
                <div class="flex items-center">
                    <div class="p-3 bg-purple-100 rounded-full">
                        <IconUsers class="w-8 h-8 text-purple-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Giảng viên chủ nhiệm</p>
                        <p class="text-2xl font-bold text-gray-900">{{ totalTeachers }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-orange-500">
                <div class="flex items-center">
                    <div class="p-3 bg-orange-100 rounded-full">
                        <IconCalendar class="w-8 h-8 text-orange-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Lớp đang hoạt động</p>
                        <p class="text-2xl font-bold text-gray-900">{{ activeClasses }}</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Classes Table -->
        <div class="bg-white rounded-lg shadow-md">
            <div class="p-6 border-b border-gray-200">
                <h3 class="text-lg font-semibold text-gray-900">Danh sách lớp học</h3>
            </div>
            <div class="overflow-x-auto">
                <el-table :data="filteredClasses" stripe style="width: 100%">
                    <el-table-column prop="className" label="Tên lớp" width="150" />
                    <el-table-column prop="major" label="Ngành" width="150" />
                    <el-table-column prop="year" label="Khóa" width="100" />
                    <el-table-column prop="studentCount" label="Số sinh viên" width="120" />
                    <el-table-column prop="teacherName" label="GV chủ nhiệm" width="200" />
                    <el-table-column prop="room" label="Phòng học" width="120" />
                    <el-table-column prop="status" label="Trạng thái" width="120">
                        <template #default="scope">
                            <el-tag :type="getStatusType(scope.row.status)">
                                {{ scope.row.status }}
                            </el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column label="Thao tác" width="200">
                        <template #default="scope">
                            <el-button size="small" @click="viewClass(scope.row)">
                                Xem
                            </el-button>
                            <el-button size="small" type="primary" @click="editClass(scope.row)">
                                Sửa
                            </el-button>
                            <el-button size="small" type="danger" @click="deleteClass(scope.row)">
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
                    :total="totalClasses"
                    layout="total, sizes, prev, pager, next, jumper"
                />
            </div>
        </div>

        <!-- Add Class Dialog -->
        <el-dialog v-model="showAddDialog" title="Thêm lớp mới" width="600px">
            <el-form :model="newClass" label-width="120px">
                <el-form-item label="Tên lớp">
                    <el-input v-model="newClass.className" />
                </el-form-item>
                <el-form-item label="Ngành">
                    <el-select v-model="newClass.major" placeholder="Chọn ngành">
                        <el-option label="Công nghệ thông tin" value="CNTT" />
                        <el-option label="Kỹ thuật phần mềm" value="KTPM" />
                        <el-option label="An toàn thông tin" value="ATTT" />
                    </el-select>
                </el-form-item>
                <el-form-item label="Khóa">
                    <el-select v-model="newClass.year" placeholder="Chọn khóa">
                        <el-option label="Khóa 2021" value="2021" />
                        <el-option label="Khóa 2022" value="2022" />
                        <el-option label="Khóa 2023" value="2023" />
                    </el-select>
                </el-form-item>
                <el-form-item label="Giảng viên chủ nhiệm">
                    <el-input v-model="newClass.teacherName" />
                </el-form-item>
                <el-form-item label="Phòng học">
                    <el-input v-model="newClass.room" />
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button @click="showAddDialog = false">Hủy</el-button>
                <el-button type="primary" @click="addClass">Thêm</el-button>
            </template>
        </el-dialog>

        <!-- View Class Dialog -->
        <el-dialog v-model="showViewDialog" title="Thông tin lớp học" width="800px">
            <div v-if="selectedClass" class="space-y-4">
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Tên lớp</label>
                        <p class="mt-1 text-sm text-gray-900">{{ selectedClass.className }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Ngành</label>
                        <p class="mt-1 text-sm text-gray-900">{{ selectedClass.major }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Khóa</label>
                        <p class="mt-1 text-sm text-gray-900">{{ selectedClass.year }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Số sinh viên</label>
                        <p class="mt-1 text-sm text-gray-900 font-bold">{{ selectedClass.studentCount }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Giảng viên chủ nhiệm</label>
                        <p class="mt-1 text-sm text-gray-900">{{ selectedClass.teacherName }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Phòng học</label>
                        <p class="mt-1 text-sm text-gray-900">{{ selectedClass.room }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Trạng thái</label>
                        <el-tag :type="getStatusType(selectedClass.status)">
                            {{ selectedClass.status }}
                        </el-tag>
                    </div>
                </div>
            </div>
            <template #footer>
                <el-button @click="showViewDialog = false">Đóng</el-button>
                <el-button type="primary" @click="editClassFromView">Chỉnh sửa</el-button>
            </template>
        </el-dialog>

        <!-- Edit Class Dialog -->
        <el-dialog v-model="showEditDialog" title="Chỉnh sửa lớp học" width="600px">
            <el-form :model="editingClass" label-width="120px">
                <el-form-item label="Tên lớp">
                    <el-input v-model="editingClass.className" disabled />
                </el-form-item>
                <el-form-item label="Ngành">
                    <el-select v-model="editingClass.major" placeholder="Chọn ngành">
                        <el-option label="Công nghệ thông tin" value="CNTT" />
                        <el-option label="Kỹ thuật phần mềm" value="KTPM" />
                        <el-option label="An toàn thông tin" value="ATTT" />
                    </el-select>
                </el-form-item>
                <el-form-item label="Khóa">
                    <el-select v-model="editingClass.year" placeholder="Chọn khóa">
                        <el-option label="Khóa 2021" value="2021" />
                        <el-option label="Khóa 2022" value="2022" />
                        <el-option label="Khóa 2023" value="2023" />
                    </el-select>
                </el-form-item>
                <el-form-item label="Giảng viên chủ nhiệm">
                    <el-input v-model="editingClass.teacherName" />
                </el-form-item>
                <el-form-item label="Phòng học">
                    <el-input v-model="editingClass.room" />
                </el-form-item>
                <el-form-item label="Trạng thái">
                    <el-select v-model="editingClass.status" placeholder="Chọn trạng thái">
                        <el-option label="Đang hoạt động" value="Đang hoạt động" />
                        <el-option label="Tạm dừng" value="Tạm dừng" />
                        <el-option label="Kết thúc" value="Kết thúc" />
                    </el-select>
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button @click="showEditDialog = false">Hủy</el-button>
                <el-button type="primary" @click="updateClass">Cập nhật</el-button>
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
const selectedMajor = ref('');
const selectedYear = ref('');
const currentPage = ref(1);
const pageSize = ref(20);
const showAddDialog = ref(false);
const showViewDialog = ref(false);
const showEditDialog = ref(false);
const selectedClass = ref(null);
const editingClass = ref({});

const newClass = ref({
    className: '',
    major: '',
    year: '',
    teacherName: '',
    room: ''
});

// Mock data
const classes = ref([
    {
        id: 1,
        className: 'CNTT21A',
        major: 'CNTT',
        year: '2021',
        studentCount: 45,
        teacherName: 'ThS. Nguyễn Văn A',
        room: 'A101',
        status: 'Đang hoạt động'
    },
    {
        id: 2,
        className: 'CNTT21B',
        major: 'CNTT',
        year: '2021',
        studentCount: 42,
        teacherName: 'TS. Trần Thị B',
        room: 'A102',
        status: 'Đang hoạt động'
    },
    {
        id: 3,
        className: 'KTPM22A',
        major: 'KTPM',
        year: '2022',
        studentCount: 38,
        teacherName: 'ThS. Lê Văn C',
        room: 'B201',
        status: 'Đang hoạt động'
    },
    {
        id: 4,
        className: 'ATTT23A',
        major: 'ATTT',
        year: '2023',
        studentCount: 35,
        teacherName: 'TS. Phạm Thị D',
        room: 'C301',
        status: 'Đang hoạt động'
    }
]);

// Computed properties
const totalClasses = computed(() => classes.value.length);
const totalStudents = computed(() => classes.value.reduce((sum, cls) => sum + cls.studentCount, 0));
const totalTeachers = computed(() => new Set(classes.value.map(cls => cls.teacherName)).size);
const activeClasses = computed(() => classes.value.filter(cls => cls.status === 'Đang hoạt động').length);

const filteredClasses = computed(() => {
    let filtered = classes.value;
    
    if (searchKeyword.value) {
        filtered = filtered.filter(cls => 
            cls.className.toLowerCase().includes(searchKeyword.value.toLowerCase())
        );
    }
    
    if (selectedMajor.value) {
        filtered = filtered.filter(cls => cls.major === selectedMajor.value);
    }
    
    if (selectedYear.value) {
        filtered = filtered.filter(cls => cls.year === selectedYear.value);
    }
    
    return filtered;
});

// Methods
const getStatusType = (status: string) => {
    switch (status) {
        case 'Đang hoạt động': return 'success';
        case 'Tạm dừng': return 'warning';
        case 'Kết thúc': return 'info';
        default: return 'danger';
    }
};

const handleSearch = () => {
    ElMessage.success('Tìm kiếm hoàn tất');
};

const viewClass = (cls: any) => {
    selectedClass.value = cls;
    showViewDialog.value = true;
};

const editClass = (cls: any) => {
    editingClass.value = { ...cls };
    showEditDialog.value = true;
};

const editClassFromView = () => {
    showViewDialog.value = false;
    editingClass.value = { ...selectedClass.value };
    showEditDialog.value = true;
};

const updateClass = () => {
    const index = classes.value.findIndex(c => c.id === editingClass.value.id);
    if (index > -1) {
        classes.value[index] = { ...editingClass.value };
        showEditDialog.value = false;
        ElMessage.success(`Cập nhật thông tin lớp: ${editingClass.value.className}`);
    }
};

const deleteClass = (cls: any) => {
    ElMessageBox.confirm(
        `Bạn có chắc chắn muốn xóa lớp "${cls.className}"?`,
        'Xác nhận xóa',
        {
            confirmButtonText: 'Xóa',
            cancelButtonText: 'Hủy',
            type: 'warning',
        }
    ).then(() => {
        const index = classes.value.findIndex(c => c.id === cls.id);
        if (index > -1) {
            classes.value.splice(index, 1);
            ElMessage.success(`Đã xóa lớp: ${cls.className}`);
        }
    }).catch(() => {
        ElMessage.info('Đã hủy xóa lớp');
    });
};

const addClass = () => {
    if (newClass.value.className && newClass.value.major && newClass.value.year) {
        classes.value.push({
            id: classes.value.length + 1,
            ...newClass.value,
            studentCount: 0,
            status: 'Đang hoạt động'
        });
        showAddDialog.value = false;
        newClass.value = {
            className: '',
            major: '',
            year: '',
            teacherName: '',
            room: ''
        };
        ElMessage.success('Thêm lớp thành công');
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

