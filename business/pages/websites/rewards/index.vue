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

        <!-- Search and Filter Section -->
        <div class="bg-white rounded-lg shadow-md p-6 mb-6">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <el-input
                    v-model="searchKeyword"
                    placeholder="Tìm kiếm theo tên sinh viên..."
                    :prefix-icon="Search"
                    clearable
                />
                <el-select v-model="selectedType" placeholder="Chọn loại" clearable>
                    <el-option label="Tất cả loại" value="" />
                    <el-option label="Khen thưởng" value="Khen thưởng" />
                    <el-option label="Kỷ luật" value="Kỷ luật" />
                </el-select>
                <el-select v-model="selectedStatus" placeholder="Chọn trạng thái" clearable>
                    <el-option label="Tất cả trạng thái" value="" />
                    <el-option label="Đang xử lý" value="Đang xử lý" />
                    <el-option label="Đã xử lý" value="Đã xử lý" />
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
                        <IconAppraisal class="w-8 h-8 text-blue-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Tổng hồ sơ</p>
                        <p class="text-2xl font-bold text-gray-900">{{ totalRecords }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-green-500">
                <div class="flex items-center">
                    <div class="p-3 bg-green-100 rounded-full">
                        <IconAppraisal class="w-8 h-8 text-green-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Khen thưởng</p>
                        <p class="text-2xl font-bold text-gray-900">{{ rewardCount }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-red-500">
                <div class="flex items-center">
                    <div class="p-3 bg-red-100 rounded-full">
                        <IconAppraisal class="w-8 h-8 text-red-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Kỷ luật</p>
                        <p class="text-2xl font-bold text-gray-900">{{ disciplineCount }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-orange-500">
                <div class="flex items-center">
                    <div class="p-3 bg-orange-100 rounded-full">
                        <IconUsers class="w-8 h-8 text-orange-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Đang xử lý</p>
                        <p class="text-2xl font-bold text-gray-900">{{ pendingCount }}</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Rewards/Discipline Table -->
        <div class="bg-white rounded-lg shadow-md">
            <div class="p-6 border-b border-gray-200">
                <h3 class="text-lg font-semibold text-gray-900">Danh sách khen thưởng & kỷ luật</h3>
            </div>
            <div class="overflow-x-auto">
                <el-table :data="filteredRecords" stripe style="width: 100%">
                    <el-table-column prop="studentName" label="Sinh viên" width="180" />
                    <el-table-column prop="type" label="Loại" width="120">
                        <template #default="scope">
                            <el-tag :type="getTypeColor(scope.row.type)">
                                {{ scope.row.type }}
                            </el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column prop="description" label="Mô tả" width="250" />
                    <el-table-column prop="date" label="Ngày" width="120" />
                    <el-table-column prop="status" label="Trạng thái" width="120">
                        <template #default="scope">
                            <el-tag :type="getStatusType(scope.row.status)">
                                {{ scope.row.status }}
                            </el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column label="Thao tác" width="200">
                        <template #default="scope">
                            <el-button size="small" @click="viewRecord(scope.row)">
                                Xem
                            </el-button>
                            <el-button size="small" type="primary" @click="editRecord(scope.row)">
                                Sửa
                            </el-button>
                            <el-button size="small" type="danger" @click="deleteRecord(scope.row)">
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
                    :total="totalRecords"
                    layout="total, sizes, prev, pager, next, jumper"
                />
            </div>
        </div>

        <!-- Add Record Dialog -->
        <el-dialog v-model="showAddDialog" title="Thêm khen thưởng/kỷ luật" width="600px">
            <el-form :model="newRecord" label-width="120px">
                <el-form-item label="Sinh viên">
                    <el-select v-model="newRecord.studentName" placeholder="Chọn sinh viên">
                        <el-option label="Nguyễn Văn An" value="Nguyễn Văn An" />
                        <el-option label="Trần Thị Bình" value="Trần Thị Bình" />
                        <el-option label="Lê Văn Cường" value="Lê Văn Cường" />
                    </el-select>
                </el-form-item>
                <el-form-item label="Loại">
                    <el-select v-model="newRecord.type" placeholder="Chọn loại">
                        <el-option label="Khen thưởng" value="Khen thưởng" />
                        <el-option label="Kỷ luật" value="Kỷ luật" />
                    </el-select>
                </el-form-item>
                <el-form-item label="Mô tả">
                    <el-input v-model="newRecord.description" type="textarea" :rows="3" />
                </el-form-item>
                <el-form-item label="Ngày">
                    <el-date-picker v-model="newRecord.date" type="date" placeholder="Chọn ngày" />
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button @click="showAddDialog = false">Hủy</el-button>
                <el-button type="primary" @click="addRecord">Thêm</el-button>
            </template>
        </el-dialog>

        <!-- View Record Dialog -->
        <el-dialog v-model="showViewDialog" title="Chi tiết khen thưởng/kỷ luật" width="800px">
            <div v-if="selectedRecord" class="space-y-4">
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Sinh viên</label>
                        <p class="mt-1 text-sm text-gray-900">{{ selectedRecord.studentName }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Loại</label>
                        <el-tag :type="getTypeColor(selectedRecord.type)">
                            {{ selectedRecord.type }}
                        </el-tag>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Ngày</label>
                        <p class="mt-1 text-sm text-gray-900">{{ selectedRecord.date }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Trạng thái</label>
                        <el-tag :type="getStatusType(selectedRecord.status)">
                            {{ selectedRecord.status }}
                        </el-tag>
                    </div>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700">Mô tả</label>
                    <div class="mt-1 p-4 bg-gray-50 rounded-lg">
                        <p class="text-sm text-gray-900 whitespace-pre-wrap">{{ selectedRecord.description }}</p>
                    </div>
                </div>
            </div>
            <template #footer>
                <el-button @click="showViewDialog = false">Đóng</el-button>
                <el-button type="primary" @click="editRecordFromView">Chỉnh sửa</el-button>
            </template>
        </el-dialog>

        <!-- Edit Record Dialog -->
        <el-dialog v-model="showEditDialog" title="Chỉnh sửa khen thưởng/kỷ luật" width="600px">
            <el-form :model="editingRecord" label-width="120px">
                <el-form-item label="Sinh viên">
                    <el-input v-model="editingRecord.studentName" disabled />
                </el-form-item>
                <el-form-item label="Loại">
                    <el-select v-model="editingRecord.type" placeholder="Chọn loại">
                        <el-option label="Khen thưởng" value="Khen thưởng" />
                        <el-option label="Kỷ luật" value="Kỷ luật" />
                    </el-select>
                </el-form-item>
                <el-form-item label="Mô tả">
                    <el-input v-model="editingRecord.description" type="textarea" :rows="3" />
                </el-form-item>
                <el-form-item label="Ngày">
                    <el-date-picker v-model="editingRecord.date" type="date" placeholder="Chọn ngày" />
                </el-form-item>
                <el-form-item label="Trạng thái">
                    <el-select v-model="editingRecord.status" placeholder="Chọn trạng thái">
                        <el-option label="Đang xử lý" value="Đang xử lý" />
                        <el-option label="Đã xử lý" value="Đã xử lý" />
                    </el-select>
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button @click="showEditDialog = false">Hủy</el-button>
                <el-button type="primary" @click="updateRecord">Cập nhật</el-button>
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
const selectedStatus = ref('');
const currentPage = ref(1);
const pageSize = ref(20);
const showAddDialog = ref(false);
const showViewDialog = ref(false);
const showEditDialog = ref(false);
const selectedRecord = ref(null);
const editingRecord = ref({});

const newRecord = ref({
    studentName: '',
    type: '',
    description: '',
    date: ''
});

// Mock data
const records = ref([
    {
        id: 1,
        studentName: 'Nguyễn Văn An',
        type: 'Khen thưởng',
        description: 'Đạt giải nhất cuộc thi lập trình cấp trường',
        date: '2024-01-15',
        status: 'Đã xử lý'
    },
    {
        id: 2,
        studentName: 'Trần Thị Bình',
        type: 'Kỷ luật',
        description: 'Vi phạm nội quy thi cử - gian lận trong kỳ thi',
        date: '2024-01-10',
        status: 'Đang xử lý'
    },
    {
        id: 3,
        studentName: 'Lê Văn Cường',
        type: 'Khen thưởng',
        description: 'Thành tích học tập xuất sắc - GPA 9.0',
        date: '2024-01-08',
        status: 'Đã xử lý'
    }
]);

// Computed properties
const totalRecords = computed(() => records.value.length);
const rewardCount = computed(() => records.value.filter(r => r.type === 'Khen thưởng').length);
const disciplineCount = computed(() => records.value.filter(r => r.type === 'Kỷ luật').length);
const pendingCount = computed(() => records.value.filter(r => r.status === 'Đang xử lý').length);

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
    
    if (selectedStatus.value) {
        filtered = filtered.filter(record => record.status === selectedStatus.value);
    }
    
    return filtered;
});

// Methods
const getStatusType = (status: string) => {
    switch (status) {
        case 'Đã xử lý': return 'success';
        case 'Đang xử lý': return 'warning';
        default: return 'info';
    }
};

const getTypeColor = (type: string) => {
    switch (type) {
        case 'Khen thưởng': return 'success';
        case 'Kỷ luật': return 'danger';
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
        ElMessage.success(`Cập nhật: ${editingRecord.value.studentName}`);
    }
};

const deleteRecord = (record: any) => {
    ElMessageBox.confirm(
        `Bạn có chắc chắn muốn xóa hồ sơ "${record.studentName}"?`,
        'Xác nhận xóa',
        {
            confirmButtonText: 'Xóa',
            cancelButtonText: 'Hủy',
            type: 'warning',
        }
    ).then(() => {
        const index = records.value.findIndex(r => r.id === record.id);
        if (index > -1) {
            records.value.splice(index, 1);
            ElMessage.success(`Đã xóa: ${record.studentName}`);
        }
    }).catch(() => {
        ElMessage.info('Đã hủy xóa');
    });
};

const addRecord = () => {
    if (newRecord.value.studentName && newRecord.value.type && newRecord.value.description) {
        records.value.push({
            id: records.value.length + 1,
            ...newRecord.value,
            status: 'Đang xử lý'
        });
        showAddDialog.value = false;
        newRecord.value = {
            studentName: '',
            type: '',
            description: '',
            date: ''
        };
        ElMessage.success('Thêm thành công');
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