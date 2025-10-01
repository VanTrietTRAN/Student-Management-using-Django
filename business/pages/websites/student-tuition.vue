&lt;template>
  &lt;div class="p-6">
    &lt;!-- Page Header -->
    &lt;div class="mb-6">
      &lt;h1 class="text-2xl font-bold text-gray-900">{{ $t('Học phí') }}&lt;/h1>
    &lt;/div>

    &lt;!-- Tuition Overview -->
    &lt;div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
      &lt;!-- Total Tuition -->
      &lt;el-card shadow="hover" class="h-full">
        &lt;div class="text-center">
          &lt;h3 class="text-lg font-semibold mb-2">{{ $t('Tổng học phí') }}&lt;/h3>
          &lt;p class="text-3xl font-bold text-primary-600">24,000,000 VNĐ&lt;/p>
          &lt;p class="text-sm text-gray-500 mt-2">{{ $t('Học kỳ') }} 2 - 2023/2024&lt;/p>
        &lt;/div>
      &lt;/el-card>

      &lt;!-- Paid Amount -->
      &lt;el-card shadow="hover" class="h-full">
        &lt;div class="text-center">
          &lt;h3 class="text-lg font-semibold mb-2">{{ $t('Đã thanh toán') }}&lt;/h3>
          &lt;p class="text-3xl font-bold text-success-600">12,000,000 VNĐ&lt;/p>
          &lt;p class="text-sm text-gray-500 mt-2">{{ $t('Cập nhật') }}: 15/01/2024&lt;/p>
        &lt;/div>
      &lt;/el-card>

      &lt;!-- Remaining Amount -->
      &lt;el-card shadow="hover" class="h-full">
        &lt;div class="text-center">
          &lt;h3 class="text-lg font-semibold mb-2">{{ $t('Còn lại') }}&lt;/h3>
          &lt;p class="text-3xl font-bold text-danger-600">12,000,000 VNĐ&lt;/p>
          &lt;p class="text-sm text-gray-500 mt-2">{{ $t('Hạn nộp') }}: 30/01/2024&lt;/p>
        &lt;/div>
      &lt;/el-card>
    &lt;/div>

    &lt;!-- Payment History -->
    &lt;div class="bg-white rounded-lg shadow overflow-hidden mb-6">
      &lt;div class="p-4 border-b border-gray-200">
        &lt;h2 class="text-lg font-semibold">{{ $t('Lịch sử thanh toán') }}&lt;/h2>
      &lt;/div>
      &lt;el-table :data="paymentHistory" stripe>
        &lt;el-table-column prop="date" :label="$t('Ngày thanh toán')" width="150">
          &lt;template #default="{ row }">
            {{ formatDate(row.date) }}
          &lt;/template>
        &lt;/el-table-column>
        &lt;el-table-column prop="amount" :label="$t('Số tiền')" width="150">
          &lt;template #default="{ row }">
            {{ formatCurrency(row.amount) }}
          &lt;/template>
        &lt;/el-table-column>
        &lt;el-table-column prop="method" :label="$t('Phương thức')" width="150">
          &lt;template #default="{ row }">
            &lt;el-tag :type="getPaymentMethodTag(row.method)">
              {{ row.method }}
            &lt;/el-tag>
          &lt;/template>
        &lt;/el-table-column>
        &lt;el-table-column prop="status" :label="$t('Trạng thái')" width="150">
          &lt;template #default="{ row }">
            &lt;el-tag :type="getStatusTag(row.status)">
              {{ row.status }}
            &lt;/el-tag>
          &lt;/template>
        &lt;/el-table-column>
        &lt;el-table-column prop="reference" :label="$t('Mã giao dịch')" min-width="200" />
      &lt;/el-table>
    &lt;/div>

    &lt;!-- Tuition Details -->
    &lt;div class="bg-white rounded-lg shadow overflow-hidden">
      &lt;div class="p-4 border-b border-gray-200">
        &lt;h2 class="text-lg font-semibold">{{ $t('Chi tiết học phí') }}&lt;/h2>
      &lt;/div>
      &lt;el-table :data="tuitionDetails" stripe>
        &lt;el-table-column prop="courseCode" :label="$t('Mã học phần')" width="150" />
        &lt;el-table-column prop="courseName" :label="$t('Tên học phần')" min-width="250" />
        &lt;el-table-column prop="credits" :label="$t('Số tín chỉ')" width="120" align="center" />
        &lt;el-table-column prop="amount" :label="$t('Học phí')" width="150">
          &lt;template #default="{ row }">
            {{ formatCurrency(row.amount) }}
          &lt;/template>
        &lt;/el-table-column>
        &lt;el-table-column prop="type" :label="$t('Loại học phí')" width="150">
          &lt;template #default="{ row }">
            &lt;el-tag :type="getTuitionTypeTag(row.type)">{{ row.type }}&lt;/el-tag>
          &lt;/template>
        &lt;/el-table-column>
      &lt;/el-table>
    &lt;/div>
  &lt;/div>
&lt;/template>

&lt;script setup lang="ts">
import { ref } from 'vue'
import dayjs from 'dayjs'

// Sample payment history data
const paymentHistory = ref([
  {
    date: '2024-01-15',
    amount: 12000000,
    method: 'Chuyển khoản',
    status: 'Thành công',
    reference: 'PAY-2024011501'
  },
  {
    date: '2023-12-20',
    amount: 12000000,
    method: 'VNPay',
    status: 'Thành công',
    reference: 'PAY-2023122001'
  }
])

// Sample tuition details data
const tuitionDetails = ref([
  {
    courseCode: 'INT3306',
    courseName: 'Web Programming',
    credits: 3,
    amount: 4800000,
    type: 'Học phí'
  },
  {
    courseCode: 'INT3307',
    courseName: 'Database Systems',
    credits: 3,
    amount: 4800000,
    type: 'Học phí'
  },
  {
    courseCode: 'INT3308',
    courseName: 'Software Engineering',
    credits: 3,
    amount: 4800000,
    type: 'Học phí'
  }
])

// Helper functions
const formatDate = (date: string) => {
  return dayjs(date).format('DD/MM/YYYY')
}

const formatCurrency = (amount: number) => {
  return new Intl.NumberFormat('vi-VN', {
    style: 'currency',
    currency: 'VND',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(amount)
}

const getPaymentMethodTag = (method: string) => {
  switch (method) {
    case 'Chuyển khoản':
      return 'primary'
    case 'VNPay':
      return 'success'
    case 'Tiền mặt':
      return 'warning'
    default:
      return 'info'
  }
}

const getStatusTag = (status: string) => {
  switch (status) {
    case 'Thành công':
      return 'success'
    case 'Đang xử lý':
      return 'warning'
    case 'Thất bại':
      return 'danger'
    default:
      return 'info'
  }
}

const getTuitionTypeTag = (type: string) => {
  switch (type) {
    case 'Học phí':
      return 'primary'
    case 'Phí khác':
      return 'warning'
    default:
      return 'info'
  }
}
&lt;/script>

&lt;style scoped>
.el-table {
  @apply rounded-lg;
}

.el-card {
  @apply rounded-lg;
}
&lt;/style>