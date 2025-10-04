<template>
  <div class="tuition">
    <el-card class="tuition-summary">
      <template #header>
        <div class="card-header">
          <span>{{ $t('Tổng quan học phí') }}</span>
          <el-select v-model="selectedSemester" class="semester-select">
            <el-option
              v-for="semester in semesters"
              :key="semester.value"
              :label="semester.label"
              :value="semester.value"
            />
          </el-select>
        </div>
      </template>

      <!-- Summary Section -->
      <el-descriptions :column="3" border>
        <el-descriptions-item :label="$t('Tổng học phí')">
          {{ formatCurrency(totalTuition) }}
        </el-descriptions-item>
        <el-descriptions-item :label="$t('Đã thanh toán')">
          {{ formatCurrency(paidAmount) }}
        </el-descriptions-item>
        <el-descriptions-item :label="$t('Còn lại')">
          <span :class="{ 'text-danger': remainingAmount > 0 }">
            {{ formatCurrency(remainingAmount) }}
          </span>
        </el-descriptions-item>
      </el-descriptions>

      <!-- Payment Status -->
      <div class="payment-status mt-4">
        <el-progress
          :percentage="paymentPercentage"
          :status="paymentStatus"
          :format="formatPercentage"
          :stroke-width="20"
        />
      </div>
    </el-card>

    <!-- Tuition Details -->
    <el-card class="tuition-details mt-4">
      <template #header>
        <div class="card-header">
          <span>{{ $t('Chi tiết học phí') }}</span>
        </div>
      </template>

      <el-table :data="tuitionDetails" style="width: 100%">
        <el-table-column :label="$t('Mã học phần')" prop="courseCode" width="120" />
        <el-table-column :label="$t('Tên học phần')" prop="courseName" />
        <el-table-column :label="$t('Số tín chỉ')" prop="credits" width="100" />
        <el-table-column :label="$t('Đơn giá')" width="150">
          <template #default="{ row }">
            {{ formatCurrency(row.pricePerCredit) }}
          </template>
        </el-table-column>
        <el-table-column :label="$t('Thành tiền')" width="150">
          <template #default="{ row }">
            {{ formatCurrency(row.credits * row.pricePerCredit) }}
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- Payment History -->
    <el-card class="payment-history mt-4">
      <template #header>
        <div class="card-header">
          <span>{{ $t('Lịch sử thanh toán') }}</span>
        </div>
      </template>

      <el-table :data="paymentHistory" style="width: 100%">
        <el-table-column :label="$t('Ngày')" prop="date" width="120">
          <template #default="{ row }">
            {{ formatDate(row.date) }}
          </template>
        </el-table-column>
        <el-table-column :label="$t('Số tiền')" width="150">
          <template #default="{ row }">
            {{ formatCurrency(row.amount) }}
          </template>
        </el-table-column>
        <el-table-column :label="$t('Phương thức')" prop="method" width="150" />
        <el-table-column :label="$t('Mã giao dịch')" prop="transactionId" width="200" />
        <el-table-column :label="$t('Trạng thái')" width="120">
          <template #default="{ row }">
            <el-tag :type="getPaymentStatusType(row.status)">
              {{ getPaymentStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column :label="$t('Thao tác')" width="120">
          <template #default="{ row }">
            <el-button 
              type="primary" 
              link
              @click="downloadInvoice(row)"
            >
              {{ $t('Hóa đơn') }}
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- Pay Tuition Button -->
    <div class="payment-actions mt-4">
      <el-button 
        type="primary"
        :disabled="remainingAmount <= 0"
        @click="showPaymentDialog"
      >
        {{ $t('Thanh toán học phí') }}
      </el-button>
    </div>

    <!-- Payment Dialog -->
    <el-dialog
      v-model="paymentDialogVisible"
      :title="$t('Thanh toán học phí')"
      width="500px"
    >
      <el-form :model="paymentForm" label-width="120px">
        <el-form-item :label="$t('Số tiền')">
          <el-input-number
            v-model="paymentForm.amount"
            :min="1000"
            :max="remainingAmount"
            :step="1000"
            :precision="0"
          />
        </el-form-item>
        <el-form-item :label="$t('Phương thức')">
          <el-select v-model="paymentForm.method">
            <el-option label="Chuyển khoản" value="bank_transfer" />
            <el-option label="Thẻ tín dụng" value="credit_card" />
            <el-option label="Tiền mặt" value="cash" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="paymentDialogVisible = false">
          {{ $t('Hủy') }}
        </el-button>
        <el-button type="primary" @click="processPayment">
          {{ $t('Xác nhận') }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { format } from 'date-fns'
import { vi } from 'date-fns/locale'

// Data
const selectedSemester = ref('2025-1')
const semesters = [
  { label: 'Học kỳ 1 năm 2025-2026', value: '2025-1' },
  { label: 'Học kỳ 2 năm 2024-2025', value: '2024-2' },
  { label: 'Học kỳ 1 năm 2024-2025', value: '2024-1' }
]

const tuitionDetails = ref([
  {
    courseCode: 'INT3001',
    courseName: 'Trí tuệ nhân tạo',
    credits: 3,
    pricePerCredit: 850000
  },
  {
    courseCode: 'INT3002',
    courseName: 'Phát triển ứng dụng di động',
    credits: 3,
    pricePerCredit: 850000
  },
  {
    courseCode: 'INT3003',
    courseName: 'Lập trình Web nâng cao',
    credits: 3,
    pricePerCredit: 850000
  }
])

const paymentHistory = ref([
  {
    date: '2025-09-15',
    amount: 2550000,
    method: 'Chuyển khoản',
    transactionId: 'TRX123456789',
    status: 'completed'
  },
  {
    date: '2025-09-01',
    amount: 2550000,
    method: 'Thẻ tín dụng',
    transactionId: 'TRX123456788',
    status: 'completed'
  }
])

// Computed
const totalTuition = computed(() => {
  return tuitionDetails.value.reduce((sum, item) => {
    return sum + (item.credits * item.pricePerCredit)
  }, 0)
})

const paidAmount = computed(() => {
  return paymentHistory.value.reduce((sum, payment) => {
    return payment.status === 'completed' ? sum + payment.amount : sum
  }, 0)
})

const remainingAmount = computed(() => {
  return totalTuition.value - paidAmount.value
})

const paymentPercentage = computed(() => {
  return Math.min(100, (paidAmount.value / totalTuition.value) * 100)
})

const paymentStatus = computed(() => {
  if (paymentPercentage.value >= 100) return 'success'
  if (paymentPercentage.value >= 50) return 'warning'
  return 'exception'
})

// Payment Dialog
const paymentDialogVisible = ref(false)
const paymentForm = ref({
  amount: 0,
  method: 'bank_transfer'
})

// Methods
const formatCurrency = (amount: number) => {
  return new Intl.NumberFormat('vi-VN', {
    style: 'currency',
    currency: 'VND'
  }).format(amount)
}

const formatDate = (dateString: string) => {
  return format(new Date(dateString), 'dd/MM/yyyy', { locale: vi })
}

const formatPercentage = (percentage: number) => {
  return percentage === 100 ? 'Đã hoàn thành' : `${percentage}%`
}

const getPaymentStatusType = (status: string) => {
  const types: Record<string, string> = {
    completed: 'success',
    pending: 'warning',
    failed: 'danger'
  }
  return types[status] || 'info'
}

const getPaymentStatusText = (status: string) => {
  const texts: Record<string, string> = {
    completed: 'Đã hoàn thành',
    pending: 'Đang xử lý',
    failed: 'Thất bại'
  }
  return texts[status] || status
}

const showPaymentDialog = () => {
  paymentForm.value.amount = remainingAmount.value
  paymentDialogVisible.value = true
}

const processPayment = async () => {
  try {
    // API call to process payment
    console.log('Processing payment:', paymentForm.value)
    paymentDialogVisible.value = false
  } catch (error) {
    console.error('Payment failed:', error)
  }
}

const downloadInvoice = (payment: any) => {
  // Implementation for downloading invoice
  console.log('Downloading invoice for payment:', payment)
}
</script>

<style scoped>
.tuition {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.semester-select {
  width: 200px;
}

.mt-4 {
  margin-top: 1rem;
}

.text-danger {
  color: var(--el-color-danger);
}

.payment-status {
  margin: 20px 0;
}

.payment-actions {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
</style>