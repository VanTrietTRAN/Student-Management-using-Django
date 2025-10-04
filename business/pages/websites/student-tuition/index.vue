<template>
    <div class="min-h-screen bg-gray-50 pt-20 px-4 md:px-6 pb-6">
        <!-- Header Section -->
        <div class="mb-8">
            <h1 class="text-3xl font-bold text-gray-900 mb-2">Học phí của tôi</h1>
            <p class="text-gray-600">Xem và thanh toán học phí theo từng học kỳ</p>
        </div>

        <!-- Filter Section -->
        <div class="bg-white rounded-lg shadow-md p-6 mb-6">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <el-select v-model="selectedSemester" placeholder="Chọn học kỳ" clearable>
                    <el-option label="Tất cả học kỳ" value="" />
                    <el-option label="Học kỳ 1" value="1" />
                    <el-option label="Học kỳ 2" value="2" />
                    <el-option label="Học kỳ 3" value="3" />
                </el-select>
                <el-select v-model="selectedStatus" placeholder="Chọn trạng thái" clearable>
                    <el-option label="Tất cả trạng thái" value="" />
                    <el-option label="Đã đóng" value="Đã đóng" />
                    <el-option label="Chưa đóng" value="Chưa đóng" />
                    <el-option label="Quá hạn" value="Quá hạn" />
                </el-select>
                <el-button type="primary" :icon="Search" @click="handleFilter">
                    Lọc kết quả
                </el-button>
            </div>
        </div>

        <!-- Tuition Summary -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6 mb-8">
            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-blue-500">
                <div class="flex items-center">
                    <div class="p-3 bg-blue-100 rounded-full">
                        <IconFile class="w-8 h-8 text-blue-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Tổng học phí</p>
                        <p class="text-2xl font-bold text-gray-900">{{ formatCurrency(totalTuition) }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-green-500">
                <div class="flex items-center">
                    <div class="p-3 bg-green-100 rounded-full">
                        <IconFile class="w-8 h-8 text-green-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Đã đóng</p>
                        <p class="text-2xl font-bold text-gray-900">{{ formatCurrency(paidAmount) }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-red-500">
                <div class="flex items-center">
                    <div class="p-3 bg-red-100 rounded-full">
                        <IconFile class="w-8 h-8 text-red-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Chưa đóng</p>
                        <p class="text-2xl font-bold text-gray-900">{{ formatCurrency(unpaidAmount) }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-orange-500">
                <div class="flex items-center">
                    <div class="p-3 bg-orange-100 rounded-full">
                        <IconFile class="w-8 h-8 text-orange-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Quá hạn</p>
                        <p class="text-2xl font-bold text-gray-900">{{ overdueCount }}</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Tuition Table -->
        <div class="bg-white rounded-lg shadow-md">
            <div class="p-6 border-b border-gray-200">
                <h3 class="text-lg font-semibold text-gray-900">Chi tiết học phí</h3>
            </div>
            <div class="overflow-x-auto">
                <el-table :data="filteredTuition" stripe style="width: 100%">
                    <el-table-column prop="semester" label="Học kỳ" width="100" />
                    <el-table-column prop="amount" label="Số tiền" width="150">
                        <template #default="scope">
                            <span class="font-semibold">{{ formatCurrency(scope.row.amount) }}</span>
                        </template>
                    </el-table-column>
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
                            <el-button size="small" @click="viewTuitionDetail(scope.row)">
                                Xem chi tiết
                            </el-button>
                            <el-button 
                                v-if="scope.row.status !== 'Đã đóng'" 
                                size="small" 
                                type="primary" 
                                @click="payTuition(scope.row)"
                            >
                                Thanh toán
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
        </div>

        <!-- Tuition Detail Dialog -->
        <el-dialog v-model="showDetailDialog" title="Chi tiết học phí" width="600px">
            <div v-if="selectedTuition" class="space-y-4">
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Học kỳ</label>
                        <p class="mt-1 text-sm text-gray-900">{{ selectedTuition.semester }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Số tiền</label>
                        <p class="mt-1 text-sm text-gray-900 font-bold text-lg">{{ formatCurrency(selectedTuition.amount) }}</p>
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
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Phương thức</label>
                        <p class="mt-1 text-sm text-gray-900">{{ selectedTuition.paymentMethod || 'Chưa thanh toán' }}</p>
                    </div>
                </div>
            </div>
            <template #footer>
                <el-button @click="showDetailDialog = false">Đóng</el-button>
                <el-button v-if="selectedTuition?.status !== 'Đã đóng'" type="primary" @click="payTuition(selectedTuition)">
                    Thanh toán
                </el-button>
            </template>
        </el-dialog>

        <!-- Payment Dialog -->
        <el-dialog v-model="showPaymentDialog" title="Thanh toán học phí" width="500px">
            <div v-if="paymentTuition" class="space-y-4">
                <div class="text-center">
                    <h3 class="text-lg font-semibold text-gray-900 mb-2">Thông tin thanh toán</h3>
                    <p class="text-gray-600">Học kỳ: {{ paymentTuition.semester }}</p>
                    <p class="text-2xl font-bold text-blue-600">{{ formatCurrency(paymentTuition.amount) }}</p>
                </div>
                
                <el-form :model="paymentForm" label-width="120px">
                    <el-form-item label="Phương thức">
                        <el-select v-model="paymentForm.method" placeholder="Chọn phương thức">
                            <el-option label="Chuyển khoản" value="bank_transfer" />
                            <el-option label="Thẻ ATM" value="atm_card" />
                            <el-option label="Ví điện tử" value="e_wallet" />
                        </el-select>
                    </el-form-item>
                    <el-form-item label="Ghi chú">
                        <el-input v-model="paymentForm.note" type="textarea" :rows="3" />
                    </el-form-item>
                </el-form>
            </div>
            <template #footer>
                <el-button @click="showPaymentDialog = false">Hủy</el-button>
                <el-button type="primary" @click="processPayment">Xác nhận thanh toán</el-button>
            </template>
        </el-dialog>
    </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Search } from '@element-plus/icons-vue';
import IconFile from '@/assets/icons/file.svg';

definePageMeta({
    layout: 'student'
});

// Reactive data
const selectedSemester = ref('');
const selectedStatus = ref('');
const showDetailDialog = ref(false);
const showPaymentDialog = ref(false);
const selectedTuition = ref(null);
const paymentTuition = ref(null);

const paymentForm = ref({
    method: '',
    note: ''
});

// Mock data
const tuition = ref([
    {
        id: 1,
        semester: '1',
        amount: 5000000,
        dueDate: '2024-01-15',
        paymentDate: '2024-01-10',
        status: 'Đã đóng',
        paymentMethod: 'Chuyển khoản'
    },
    {
        id: 2,
        semester: '2',
        amount: 5000000,
        dueDate: '2024-02-15',
        paymentDate: null,
        status: 'Chưa đóng',
        paymentMethod: null
    },
    {
        id: 3,
        semester: '3',
        amount: 5000000,
        dueDate: '2024-03-15',
        paymentDate: null,
        status: 'Quá hạn',
        paymentMethod: null
    }
]);

// Computed properties
const totalTuition = computed(() => tuition.value.reduce((sum, t) => sum + t.amount, 0));
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
const overdueCount = computed(() => tuition.value.filter(t => t.status === 'Quá hạn').length);

const filteredTuition = computed(() => {
    let filtered = tuition.value;
    
    if (selectedSemester.value) {
        filtered = filtered.filter(t => t.semester === selectedSemester.value);
    }
    
    if (selectedStatus.value) {
        filtered = filtered.filter(t => t.status === selectedStatus.value);
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

const handleFilter = () => {
    ElMessage.success('Lọc kết quả hoàn tất');
};

const viewTuitionDetail = (tuitionItem: any) => {
    selectedTuition.value = tuitionItem;
    showDetailDialog.value = true;
};

const payTuition = (tuitionItem: any) => {
    paymentTuition.value = tuitionItem;
    showPaymentDialog.value = true;
    showDetailDialog.value = false;
};

const processPayment = () => {
    if (!paymentForm.value.method) {
        ElMessage.error('Vui lòng chọn phương thức thanh toán');
        return;
    }
    
    ElMessageBox.confirm(
        `Xác nhận thanh toán học phí học kỳ ${paymentTuition.value.semester}?`,
        'Xác nhận thanh toán',
        {
            confirmButtonText: 'Xác nhận',
            cancelButtonText: 'Hủy',
            type: 'success',
        }
    ).then(() => {
        // Update tuition status
        const index = tuition.value.findIndex(t => t.id === paymentTuition.value.id);
        if (index > -1) {
            tuition.value[index].status = 'Đã đóng';
            tuition.value[index].paymentDate = new Date().toISOString().split('T')[0];
            tuition.value[index].paymentMethod = paymentForm.value.method;
        }
        
        showPaymentDialog.value = false;
        paymentForm.value = { method: '', note: '' };
        ElMessage.success('Thanh toán thành công');
    }).catch(() => {
        ElMessage.info('Đã hủy thanh toán');
    });
};
</script>

<style scoped>
.el-table {
    font-size: 14px;
}
</style>
