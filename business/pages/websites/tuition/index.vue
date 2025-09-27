<template>
    <div class="min-h-screen bg-gray-50 pt-20 px-4 md:px-6 pb-6">
        <!-- Header Section -->
        <div class="mb-8">
            <div class="flex justify-between items-center">
                <div>
                    <h1 class="text-3xl font-bold text-gray-900 mb-2">Quản lý học phí</h1>
                    <p class="text-gray-600">Tra cứu, đóng học phí và lịch sử giao dịch của sinh viên</p>
                </div>
                <el-button type="primary" :icon="Plus" @click="showAddDialog = true">
                    Thêm học phí mới
                </el-button>
            </div>
        </div>

        <!-- Search Section -->
        <div class="bg-white rounded-lg shadow-md p-6 mb-6">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <el-input
                    v-model="searchKeyword"
                    placeholder="Tìm kiếm theo mã sinh viên..."
                    :prefix-icon="Search"
                    clearable
                />
                <el-select v-model="selectedStatus" placeholder="Trạng thái thanh toán" clearable>
                    <el-option label="Tất cả" value="" />
                    <el-option label="Đã đóng" value="Đã đóng" />
                    <el-option label="Chưa đóng" value="Chưa đóng" />
                    <el-option label="Quá hạn" value="Quá hạn" />
                </el-select>
                <el-select v-model="selectedSemester" placeholder="Học kỳ" clearable>
                    <el-option label="Tất cả học kỳ" value="" />
                    <el-option label="Học kỳ 1" value="1" />
                    <el-option label="Học kỳ 2" value="2" />
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
                        <p class="text-2xl font-bold text-gray-900">{{ totalTuition.toLocaleString() }} VNĐ</p>
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
                        <p class="text-2xl font-bold text-gray-900">{{ paidAmount.toLocaleString() }} VNĐ</p>
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
                        <p class="text-2xl font-bold text-gray-900">{{ unpaidAmount.toLocaleString() }} VNĐ</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-orange-500">
                <div class="flex items-center">
                    <div class="p-3 bg-orange-100 rounded-full">
                        <IconFile class="w-8 h-8 text-orange-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Tỷ lệ thu</p>
                        <p class="text-2xl font-bold text-gray-900">{{ paymentRate }}%</p>
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
                <el-table :data="filteredTuitions" stripe style="width: 100%">
                    <el-table-column prop="studentId" label="Mã SV" width="100" />
                    <el-table-column prop="studentName" label="Tên sinh viên" width="200" />
                    <el-table-column prop="className" label="Lớp" width="100" />
                    <el-table-column prop="semester" label="Học kỳ" width="100" />
                    <el-table-column prop="amount" label="Số tiền" width="150">
                        <template #default="scope">
                            {{ scope.row.amount.toLocaleString() }} VNĐ
                        </template>
                    </el-table-column>
                    <el-table-column prop="dueDate" label="Hạn nộp" width="120" />
                    <el-table-column prop="status" label="Trạng thái" width="120">
                        <template #default="scope">
                            <el-tag :type="getStatusType(scope.row.status)">
                                {{ scope.row.status }}
                            </el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column prop="paymentDate" label="Ngày nộp" width="120" />
                    <el-table-column label="Thao tác" width="200">
                        <template #default="scope">
                            <el-button size="small" @click="viewTuition(scope.row)">
                                Xem
                            </el-button>
                            <el-button size="small" type="success" @click="markAsPaid(scope.row)">
                                Đánh dấu đã nộp
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
                    :total="totalTuitions"
                    layout="total, sizes, prev, pager, next, jumper"
                />
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Plus, Search } from '@element-plus/icons-vue';
import IconFile from '@/assets/icons/file.svg';

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

// Mock data
const tuitions = ref([
    {
        id: 1,
        studentId: 'SV001',
        studentName: 'Nguyễn Văn An',
        className: 'CNTT21A',
        semester: 1,
        amount: 15000000,
        dueDate: '15/09/2024',
        status: 'Đã đóng',
        paymentDate: '10/09/2024'
    },
    {
        id: 2,
        studentId: 'SV002',
        studentName: 'Trần Thị Bình',
        className: 'CNTT21B',
        semester: 1,
        amount: 15000000,
        dueDate: '15/09/2024',
        status: 'Chưa đóng',
        paymentDate: ''
    },
    {
        id: 3,
        studentId: 'SV003',
        studentName: 'Lê Văn Cường',
        className: 'CNTT22A',
        semester: 1,
        amount: 15000000,
        dueDate: '15/09/2024',
        status: 'Quá hạn',
        paymentDate: ''
    }
]);

// Computed properties
const totalTuitions = computed(() => tuitions.value.length);
const totalTuition = computed(() => tuitions.value.reduce((sum, t) => sum + t.amount, 0));
const paidAmount = computed(() => 
    tuitions.value.filter(t => t.status === 'Đã đóng').reduce((sum, t) => sum + t.amount, 0)
);
const unpaidAmount = computed(() => 
    tuitions.value.filter(t => t.status !== 'Đã đóng').reduce((sum, t) => sum + t.amount, 0)
);
const paymentRate = computed(() => 
    totalTuition.value > 0 ? Math.round((paidAmount.value / totalTuition.value) * 100) : 0
);

const filteredTuitions = computed(() => {
    let filtered = tuitions.value;
    
    if (searchKeyword.value) {
        filtered = filtered.filter(tuition => 
            tuition.studentId.toLowerCase().includes(searchKeyword.value.toLowerCase()) ||
            tuition.studentName.toLowerCase().includes(searchKeyword.value.toLowerCase())
        );
    }
    
    if (selectedStatus.value) {
        filtered = filtered.filter(tuition => tuition.status === selectedStatus.value);
    }
    
    if (selectedSemester.value) {
        filtered = filtered.filter(tuition => tuition.semester.toString() === selectedSemester.value);
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

const handleSearch = () => {
    ElMessage.success('Tìm kiếm hoàn tất');
};

const viewTuition = (tuition: any) => {
    selectedTuition.value = tuition;
    showViewDialog.value = true;
};

const markAsPaid = (tuition: any) => {
    ElMessageBox.confirm(
        `Bạn có chắc chắn muốn đánh dấu đã nộp học phí cho "${tuition.studentName}"?`,
        'Xác nhận',
        {
            confirmButtonText: 'Xác nhận',
            cancelButtonText: 'Hủy',
            type: 'success',
        }
    ).then(() => {
        tuition.status = 'Đã đóng';
        tuition.paymentDate = new Date().toLocaleDateString('vi-VN');
        ElMessage.success(`Đã đánh dấu nộp học phí: ${tuition.studentName}`);
    }).catch(() => {
        ElMessage.info('Đã hủy thao tác');
    });
};
</script>

<style scoped>
.el-table {
    font-size: 14px;
}
</style>
