<template>
    <div class="min-h-screen bg-gray-50 pt-20 px-4 md:px-6 pb-6">
        <!-- Header Section -->
        <div class="mb-8">
            <div class="flex justify-between items-center">
                <div>
                    <h1 class="text-3xl font-bold text-gray-900 mb-2">Khen thưởng & Kỷ luật</h1>
                    <p class="text-gray-600">Quản lý quá trình rèn luyện, khen thưởng và kỷ luật sinh viên</p>
                </div>
                <el-button type="primary" :icon="Plus" @click="showAddDialog = true">
                    Thêm mới
                </el-button>
            </div>
        </div>

        <!-- Search Section -->
        <div class="bg-white rounded-lg shadow-md p-6 mb-6">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <el-input
                    v-model="searchKeyword"
                    placeholder="Tìm kiếm theo tên sinh viên..."
                    :prefix-icon="Search"
                    clearable
                />
                <el-select v-model="selectedType" placeholder="Loại" clearable>
                    <el-option label="Tất cả" value="" />
                    <el-option label="Khen thưởng" value="Khen thưởng" />
                    <el-option label="Kỷ luật" value="Kỷ luật" />
                </el-select>
                <el-select v-model="selectedLevel" placeholder="Mức độ" clearable>
                    <el-option label="Tất cả" value="" />
                    <el-option label="Cấp trường" value="Cấp trường" />
                    <el-option label="Cấp khoa" value="Cấp khoa" />
                    <el-option label="Cấp lớp" value="Cấp lớp" />
                </el-select>
                <el-button type="primary" :icon="Search" @click="handleSearch">
                    Tìm kiếm
                </el-button>
            </div>
        </div>

        <!-- Statistics Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6 mb-6">
            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-green-500">
                <div class="flex items-center">
                    <div class="p-3 bg-green-100 rounded-full">
                        <IconAppraisal class="w-8 h-8 text-green-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Tổng khen thưởng</p>
                        <p class="text-2xl font-bold text-gray-900">{{ totalRewards }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-red-500">
                <div class="flex items-center">
                    <div class="p-3 bg-red-100 rounded-full">
                        <IconAppraisal class="w-8 h-8 text-red-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Tổng kỷ luật</p>
                        <p class="text-2xl font-bold text-gray-900">{{ totalDisciplines }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-blue-500">
                <div class="flex items-center">
                    <div class="p-3 bg-blue-100 rounded-full">
                        <IconUsers class="w-8 h-8 text-blue-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Sinh viên được khen</p>
                        <p class="text-2xl font-bold text-gray-900">{{ rewardedStudents }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-orange-500">
                <div class="flex items-center">
                    <div class="p-3 bg-orange-100 rounded-full">
                        <IconUsers class="w-8 h-8 text-orange-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Sinh viên bị kỷ luật</p>
                        <p class="text-2xl font-bold text-gray-900">{{ disciplinedStudents }}</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Rewards and Disciplines Table -->
        <div class="bg-white rounded-lg shadow-md">
            <div class="p-6 border-b border-gray-200">
                <h3 class="text-lg font-semibold text-gray-900">Danh sách khen thưởng & kỷ luật</h3>
            </div>
            <div class="overflow-x-auto">
                <el-table :data="filteredRecords" stripe style="width: 100%">
                    <el-table-column prop="studentId" label="Mã SV" width="100" />
                    <el-table-column prop="studentName" label="Tên sinh viên" width="200" />
                    <el-table-column prop="className" label="Lớp" width="120" />
                    <el-table-column prop="type" label="Loại" width="120">
                        <template #default="scope">
                            <el-tag :type="getTypeColor(scope.row.type)">
                                {{ scope.row.type }}
                            </el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column prop="title" label="Tiêu đề" width="250" />
                    <el-table-column prop="level" label="Mức độ" width="120" />
                    <el-table-column prop="date" label="Ngày" width="120" />
                    <el-table-column prop="status" label="Trạng thái" width="120">
                        <template #default="scope">
                            <el-tag :type="getStatusType(scope.row.status)">
                                {{ scope.row.status }}
                            </el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column label="Thao tác" width="150">
                        <template #default="scope">
                            <el-button size="small" @click="viewRecord(scope.row)">
                                Xem
                            </el-button>
                            <el-button size="small" type="primary" @click="editRecord(scope.row)">
                                Sửa
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
                    :total="totalRecords"
                    layout="total, sizes, prev, pager, next, jumper"
                />
            </div>
        </div>

        <!-- Add Record Dialog -->
        <el-dialog v-model="showAddDialog" title="Thêm khen thưởng/kỷ luật" width="600px">
            <el-form :model="newRecord" label-width="120px">
                <el-form-item label="Sinh viên">
                    <el-select v-model="newRecord.studentId" placeholder="Chọn sinh viên" filterable>
                        <el-option 
                            v-for="student in students" 
                            :key="student.id" 
                            :label="`${student.studentId} - ${student.fullName}`" 
                            :value="student.studentId" 
                        />
                    </el-select>
                </el-form-item>
                <el-form-item label="Loại">
                    <el-select v-model="newRecord.type" placeholder="Chọn loại">
                        <el-option label="Khen thưởng" value="Khen thưởng" />
                        <el-option label="Kỷ luật" value="Kỷ luật" />
                    </el-select>
                </el-form-item>
                <el-form-item label="Tiêu đề">
                    <el-input v-model="newRecord.title" />
                </el-form-item>
                <el-form-item label="Mô tả">
                    <el-input v-model="newRecord.description" type="textarea" :rows="3" />
                </el-form-item>
                <el-form-item label="Mức độ">
                    <el-select v-model="newRecord.level" placeholder="Chọn mức độ">
                        <el-option label="Cấp trường" value="Cấp trường" />
                        <el-option label="Cấp khoa" value="Cấp khoa" />
                        <el-option label="Cấp lớp" value="Cấp lớp" />
                    </el-select>
                </el-form-item>
                <el-form-item label="Ngày">
                    <el-date-picker v-model="newRecord.date" type="date" />
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button @click="showAddDialog = false">Hủy</el-button>
                <el-button type="primary" @click="addRecord">Thêm</el-button>
            </template>
        </el-dialog>
    </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Plus, Search } from '@element-plus/icons-vue';
import IconAppraisal from '@/assets/icons/appraisal.svg';
import IconUsers from '@/assets/icons/users.svg';

definePageMeta({
    layout: 'websites'
});

// Reactive data
const searchKeyword = ref('');
const selectedType = ref('');
const selectedLevel = ref('');
const currentPage = ref(1);
const pageSize = ref(20);
const showAddDialog = ref(false);
const showViewDialog = ref(false);
const showEditDialog = ref(false);
const selectedRecord = ref(null);
const editingRecord = ref({});

const newRecord = ref({
    studentId: '',
    type: '',
    title: '',
    description: '',
    level: '',
    date: ''
});

// Mock data
const students = ref([
    { id: 1, studentId: 'SV001', fullName: 'Nguyễn Văn An' },
    { id: 2, studentId: 'SV002', fullName: 'Trần Thị Bình' },
    { id: 3, studentId: 'SV003', fullName: 'Lê Văn Cường' }
]);

const records = ref([
    {
        id: 1,
        studentId: 'SV001',
        studentName: 'Nguyễn Văn An',
        className: 'CNTT21A',
        type: 'Khen thưởng',
        title: 'Học sinh giỏi học kỳ 1',
        description: 'Đạt điểm trung bình trên 8.5 trong học kỳ 1',
        level: 'Cấp trường',
        date: '15/12/2024',
        status: 'Đã duyệt'
    },
    {
        id: 2,
        studentId: 'SV002',
        studentName: 'Trần Thị Bình',
        className: 'CNTT21B',
        type: 'Kỷ luật',
        title: 'Vi phạm nội quy lớp học',
        description: 'Đi muộn nhiều lần và không có lý do chính đáng',
        level: 'Cấp lớp',
        date: '10/12/2024',
        status: 'Đã duyệt'
    },
    {
        id: 3,
        studentId: 'SV003',
        studentName: 'Lê Văn Cường',
        className: 'CNTT22A',
        type: 'Khen thưởng',
        title: 'Thành tích xuất sắc trong nghiên cứu',
        description: 'Có công trình nghiên cứu được đăng trên tạp chí khoa học',
        level: 'Cấp khoa',
        date: '20/12/2024',
        status: 'Chờ duyệt'
    }
]);

// Computed properties
const totalRecords = computed(() => records.value.length);
const totalRewards = computed(() => records.value.filter(r => r.type === 'Khen thưởng').length);
const totalDisciplines = computed(() => records.value.filter(r => r.type === 'Kỷ luật').length);
const rewardedStudents = computed(() => 
    new Set(records.value.filter(r => r.type === 'Khen thưởng').map(r => r.studentId)).size
);
const disciplinedStudents = computed(() => 
    new Set(records.value.filter(r => r.type === 'Kỷ luật').map(r => r.studentId)).size
);

const filteredRecords = computed(() => {
    let filtered = records.value;
    
    if (searchKeyword.value) {
        filtered = filtered.filter(record => 
            record.studentName.toLowerCase().includes(searchKeyword.value.toLowerCase())
        );
    }
    
    if (selectedType.value) {
        filtered = filtered.filter(record => record.type === selectedType.value);
    }
    
    if (selectedLevel.value) {
        filtered = filtered.filter(record => record.level === selectedLevel.value);
    }
    
    return filtered;
});

// Methods
const getTypeColor = (type: string) => {
    return type === 'Khen thưởng' ? 'success' : 'danger';
};

const getStatusType = (status: string) => {
    switch (status) {
        case 'Đã duyệt': return 'success';
        case 'Chờ duyệt': return 'warning';
        case 'Từ chối': return 'danger';
        default: return 'info';
    }
};

const handleSearch = () => {
    ElMessage.success('Tìm kiếm hoàn tất');
};

const viewRecord = (record: any) => {
    selectedRecord.value = record;
    showViewDialog.value = true;
};

const editRecord = (record: any) => {
    editingRecord.value = { ...record };
    showEditDialog.value = true;
};

const editRecordFromView = () => {
    showViewDialog.value = false;
    editingRecord.value = { ...selectedRecord.value };
    showEditDialog.value = true;
};

const updateRecord = () => {
    const index = records.value.findIndex(r => r.id === editingRecord.value.id);
    if (index > -1) {
        records.value[index] = { ...editingRecord.value };
        showEditDialog.value = false;
        ElMessage.success(`Cập nhật: ${editingRecord.value.title}`);
    }
};

const addRecord = () => {
    if (newRecord.value.studentId && newRecord.value.type && newRecord.value.title) {
        const student = students.value.find(s => s.studentId === newRecord.value.studentId);
        
        if (student) {
            records.value.push({
                id: records.value.length + 1,
                studentId: newRecord.value.studentId,
                studentName: student.fullName,
                className: 'CNTT21A', // Default class
                type: newRecord.value.type,
                title: newRecord.value.title,
                description: newRecord.value.description,
                level: newRecord.value.level,
                date: newRecord.value.date || new Date().toLocaleDateString('vi-VN'),
                status: 'Chờ duyệt'
            });
            
            showAddDialog.value = false;
            newRecord.value = {
                studentId: '',
                type: '',
                title: '',
                description: '',
                level: '',
                date: ''
            };
            ElMessage.success('Thêm thành công');
        }
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
