<template>
    <div class="min-h-screen bg-gray-50 pt-20 px-4 md:px-6 pb-6">
        <!-- Header Section -->
        <div class="mb-8">
            <div class="flex justify-between items-center">
                <div>
                    <h1 class="text-3xl font-bold text-gray-900 mb-2">Quản lý học phí</h1>
                    <p class="text-gray-600">Theo dõi tình hình đóng học phí và tạo báo cáo thu chi</p>
                </div>
                <el-button type="primary" :icon="Plus" @click="showAddDialog = true">
                    Thêm học phí mới
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
                <el-select v-model="selectedStatus" placeholder="Chọn trạng thái" clearable>
                    <el-option label="Tất cả trạng thái" value="" />
                    <el-option label="Đã đóng" value="Đã đóng" />
                    <el-option label="Chưa đóng" value="Chưa đóng" />
                    <el-option label="Quá hạn" value="Quá hạn" />
                </el-select>
                <el-select v-model="selectedSemester" placeholder="Chọn học kỳ" clearable>
                    <el-option label="Tất cả học kỳ" value="" />
                    <el-option label="Học kỳ 1" value="1" />
                    <el-option label="Học kỳ 2" value="2" />
                    <el-option label="Học kỳ 3" value="3" />
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
                        <IconFile class="w-8 h-8 text-blue-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Tổng học phí</p>
                        <p class="text-2xl font-bold text-gray-900">{{ totalTuition }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-green-500">
                <div class="flex items-center">
                    <div class="p-3 bg-green-100 rounded-full">
                        <IconFile class="w-8 h-8 text-green-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Đã thu</p>
                        <p class="text-2xl font-bold text-gray-900">{{ paidAmount }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-red-500">
                <div class="flex items-center">
                    <div class="p-3 bg-red-100 rounded-full">
                        <IconFile class="w-8 h-8 text-red-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Chưa thu</p>
                        <p class="text-2xl font-bold text-gray-900">{{ unpaidAmount }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-orange-500">
                <div class="flex items-center">
                    <div class="p-3 bg-orange-100 rounded-full">
                        <IconUsers class="w-8 h-8 text-orange-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Sinh viên chưa đóng</p>
                        <p class="text-2xl font-bold text-gray-900">{{ unpaidStudents }}</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Tuition Table -->
        <div class="bg-white rounded-lg shadow-md">
            <div class="p-6 border-b border-gray-200">
                <h3 class="text-lg font-semibold text-gray-900">Danh sách học phí</h3>
            </div>
            <div class="overflow-x-auto">
                <el-table :data="filteredTuition" stripe style="width: 100%">
                    <el-table-column prop="studentName" label="Sinh viên" width="180" />
                    <el-table-column prop="amount" label="Số tiền" width="120">
                        <template #default="scope">
                            <span class="font-semibold">{{ formatCurrency(scope.row.amount) }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="semester" label="Học kỳ" width="100" />
                    <el-table-column prop="dueDate" label="Hạn đóng" width="120" />
                    <el-table-column prop="paymentDate" label="Ngày đóng" width="120" />
                    <el-table-column prop="status" label="Trạng thái" width="120">
                        <template #default="scope">
                            <el-tag :type="getStatusType(scope.row.status)">
                                {{ scope.row.status }}
                            </el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column label="Thao tác" width="200">
                        <template #default="scope">
                            <el-button size="small" @click="viewTuition(scope.row)">
                                Xem
                            </el-button>
                            <el-button size="small" type="primary" @click="editTuition(scope.row)">
                                Sửa
                            </el-button>
                            <el-button 
                                v-if="scope.row.status !== 'Đã đóng'" 
                                size="small" 
                                type="success" 
                                @click="markAsPaid(scope.row)"
                            >
                                Đánh dấu đã đóng
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
                    :total="totalTuition"
                    layout="total, sizes, prev, pager, next, jumper"
                />
            </div>
        </div>

        <!-- Add Tuition Dialog -->
        <el-dialog v-model="showAddDialog" title="Thêm học phí mới" width="600px">
            <el-form :model="newTuition" label-width="120px">
                <el-form-item label="Sinh viên">
                    <el-select v-model="newTuition.studentName" placeholder="Chọn sinh viên">
                        <el-option label="Nguyễn Văn An" value="Nguyễn Văn An" />
                        <el-option label="Trần Thị Bình" value="Trần Thị Bình" />
                        <el-option label="Lê Văn Cường" value="Lê Văn Cường" />
                    </el-select>
                </el-form-item>
                <el-form-item label="Số tiền">
                    <el-input-number v-model="newTuition.amount" :min="0" :step="100000" />
                </el-form-item>
                <el-form-item label="Học kỳ">
                    <el-select v-model="newTuition.semester" placeholder="Chọn học kỳ">
                        <el-option label="Học kỳ 1" value="1" />
                        <el-option label="Học kỳ 2" value="2" />
                        <el-option label="Học kỳ 3" value="3" />
                    </el-select>
                </el-form-item>
                <el-form-item label="Hạn đóng">
                    <el-date-picker v-model="newTuition.dueDate" type="date" placeholder="Chọn ngày hạn" />
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button @click="showAddDialog = false">Hủy</el-button>
                <el-button type="primary" @click="addTuition">Thêm</el-button>
            </template>
        </el-dialog>

        <!-- View Tuition Dialog -->
        <el-dialog v-model="showViewDialog" title="Chi tiết học phí" width="800px">
            <div v-if="selectedTuition" class="space-y-4">
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Sinh viên</label>
                        <p class="mt-1 text-sm text-gray-900">{{ selectedTuition.studentName }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Số tiền</label>
                        <p class="mt-1 text-sm text-gray-900 font-bold text-lg">{{ formatCurrency(selectedTuition.amount) }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Học kỳ</label>
                        <p class="mt-1 text-sm text-gray-900">{{ selectedTuition.semester }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Hạn đóng</label>
                        <p class="mt-1 text-sm text-gray-900">{{ selectedTuition.dueDate }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Ngày đóng</label>
                        <p class="mt-1 text-sm text-gray-900">{{ selectedTuition.paymentDate || 'Chưa đóng' }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Trạng thái</label>
                        <el-tag :type="getStatusType(selectedTuition.status)">
                            {{ selectedTuition.status }}
                        </el-tag>
                    </div>
                </div>
            </div>
            <template #footer>
                <el-button @click="showViewDialog = false">Đóng</el-button>
                <el-button type="primary" @click="editTuitionFromView">Chỉnh sửa</el-button>
            </template>
        </el-dialog>

        <!-- Edit Tuition Dialog -->
        <el-dialog v-model="showEditDialog" title="Chỉnh sửa học phí" width="600px">
            <el-form :model="editingTuition" label-width="120px">
                <el-form-item label="Sinh viên">
                    <el-input v-model="editingTuition.studentName" disabled />
                </el-form-item>
                <el-form-item label="Số tiền">
                    <el-input-number v-model="editingTuition.amount" :min="0" :step="100000" />
                </el-form-item>
                <el-form-item label="Học kỳ">
                    <el-input v-model="editingTuition.semester" disabled />
                </el-form-item>
                <el-form-item label="Hạn đóng">
                    <el-date-picker v-model="editingTuition.dueDate" type="date" placeholder="Chọn ngày hạn" />
                </el-form-item>
                <el-form-item label="Ngày đóng">
                    <el-date-picker v-model="editingTuition.paymentDate" type="date" placeholder="Chọn ngày đóng" />
                </el-form-item>
                <el-form-item label="Trạng thái">
                    <el-select v-model="editingTuition.status" placeholder="Chọn trạng thái">
                        <el-option label="Chưa đóng" value="Chưa đóng" />
                        <el-option label="Đã đóng" value="Đã đóng" />
                        <el-option label="Quá hạn" value="Quá hạn" />
                    </el-select>
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button @click="showEditDialog = false">Hủy</el-button>
                <el-button type="primary" @click="updateTuition">Cập nhật</el-button>
            </template>
        </el-dialog>
    </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Plus, Search } from '@element-plus/icons-vue';
import IconFile from '@/assets/icons/file.svg';
import IconUsers from '@/assets/icons/users.svg';

definePageMeta({
    layout: 'websites'
});

// Reactive data
const searchKeyword = ref('');
const selectedStatus = ref('');
const selectedSemester = ref('');
const currentPage = ref(1);
const pageSize = ref(20);
const showAddDialog = ref(false);
const showViewDialog = ref(false);
const showEditDialog = ref(false);
const selectedTuition = ref(null);
const editingTuition = ref({});

const newTuition = ref({
    studentName: '',
    amount: 0,
    semester: '',
    dueDate: ''
});

// Mock data
const tuition = ref([
    {
        id: 1,
        studentName: 'Nguyễn Văn An',
        amount: 5000000,
        semester: '1',
        dueDate: '2024-01-15',
        paymentDate: '2024-01-10',
        status: 'Đã đóng'
    },
    {
        id: 2,
        studentName: 'Trần Thị Bình',
        amount: 5000000,
        semester: '1',
        dueDate: '2024-01-15',
        paymentDate: null,
        status: 'Chưa đóng'
    },
    {
        id: 3,
        studentName: 'Lê Văn Cường',
        amount: 5000000,
        semester: '2',
        dueDate: '2024-02-15',
        paymentDate: null,
        status: 'Quá hạn'
    }
]);

// Computed properties
const totalTuition = computed(() => tuition.value.length);
const paidAmount = computed(() => 
    tuition.value
        .filter(t => t.status === 'Đã đóng')
        .reduce((sum, t) => sum + t.amount, 0)
);
const unpaidAmount = computed(() => 
    tuition.value
        .filter(t => t.status !== 'Đã đóng')
        .reduce((sum, t) => sum + t.amount, 0)
);
const unpaidStudents = computed(() => tuition.value.filter(t => t.status !== 'Đã đóng').length);

const filteredTuition = computed(() => {
    let filtered = tuition.value;
    
    if (searchKeyword.value) {
        filtered = filtered.filter(t => 
            t.studentName.toLowerCase().includes(searchKeyword.value.toLowerCase())
        );
    }
    
    if (selectedStatus.value) {
        filtered = filtered.filter(t => t.status === selectedStatus.value);
    }
    
    if (selectedSemester.value) {
        filtered = filtered.filter(t => t.semester === selectedSemester.value);
    }
    
    return filtered;
});

// Methods
const getStatusType = (status: string) => {
    switch (status) {
        case 'Đã đóng': return 'success';
        case 'Chưa đóng': return 'warning';
        case 'Quá hạn': return 'danger';
        default: return 'info';
    }
};

const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('vi-VN', {
        style: 'currency',
        currency: 'VND'
    }).format(amount);
};

const handleSearch = () => {
    ElMessage.success('Tìm kiếm hoàn tất');
};

const viewTuition = (tuitionItem: any) => {
    selectedTuition.value = tuitionItem;
    showViewDialog.value = true;
};

const editTuition = (tuitionItem: any) => {
    editingTuition.value = { ...tuitionItem };
    showEditDialog.value = true;
};

const editTuitionFromView = () => {
    showViewDialog.value = false;
    editingTuition.value = { ...selectedTuition.value };
    showEditDialog.value = true;
};

const updateTuition = () => {
    const index = tuition.value.findIndex(t => t.id === editingTuition.value.id);
    if (index > -1) {
        tuition.value[index] = { ...editingTuition.value };
        showEditDialog.value = false;
        ElMessage.success(`Cập nhật học phí: ${editingTuition.value.studentName}`);
    }
};

const markAsPaid = (tuitionItem: any) => {
    ElMessageBox.confirm(
        `Đánh dấu học phí của "${tuitionItem.studentName}" là đã đóng?`,
        'Xác nhận',
        {
            confirmButtonText: 'Xác nhận',
            cancelButtonText: 'Hủy',
            type: 'success',
        }
    ).then(() => {
        const index = tuition.value.findIndex(t => t.id === tuitionItem.id);
        if (index > -1) {
            tuition.value[index].status = 'Đã đóng';
            tuition.value[index].paymentDate = new Date().toISOString().split('T')[0];
            ElMessage.success(`Đã đánh dấu học phí: ${tuitionItem.studentName}`);
        }
    }).catch(() => {
        ElMessage.info('Đã hủy');
    });
};

const addTuition = () => {
    if (newTuition.value.studentName && newTuition.value.amount > 0) {
        tuition.value.push({
            id: tuition.value.length + 1,
            ...newTuition.value,
            paymentDate: null,
            status: 'Chưa đóng'
        });
        showAddDialog.value = false;
        newTuition.value = {
            studentName: '',
            amount: 0,
            semester: '',
            dueDate: ''
        };
        ElMessage.success('Thêm học phí thành công');
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