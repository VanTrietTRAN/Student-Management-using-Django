<template>
  <div class="p-6">
    <!-- Page Header -->
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-900">{{ $t('Học phí') }}</h1>
    </div>

    <!-- Tuition Overview -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
      <!-- Total Tuition -->
      <el-card shadow="hover" class="h-full">
        <div class="text-center">
          <h3 class="text-lg font-semibold mb-2">{{ $t('Tổng học phí') }}</h3>
          <p class="text-3xl font-bold text-primary-600">24,000,000 VNĐ</p>
          <p class="text-sm text-gray-500 mt-2">{{ $t('Học kỳ') }} 2 - 2023/2024</p>
        </div>
      </el-card>

      <!-- Paid Amount -->
      <el-card shadow="hover" class="h-full">
        <div class="text-center">
          <h3 class="text-lg font-semibold mb-2">{{ $t('Đã thanh toán') }}</h3>
          <p class="text-3xl font-bold text-success-600">12,000,000 VNĐ</p>
          <p class="text-sm text-gray-500 mt-2">{{ $t('Cập nhật') }}: 15/01/2024</p>
        </div>
      </el-card>

      <!-- Remaining Amount -->
      <el-card shadow="hover" class="h-full">
        <div class="text-center">
          <h3 class="text-lg font-semibold mb-2">{{ $t('Còn lại') }}</h3>
          <p class="text-3xl font-bold text-danger-600">12,000,000 VNĐ</p>
          <p class="text-sm text-gray-500 mt-2">{{ $t('Hạn nộp') }}: 30/01/2024</p>
        </div>
      </el-card>
    </div>

    <!-- Payment History -->
    <div class="bg-white rounded-lg shadow overflow-hidden mb-6">
      <div class="p-4 border-b border-gray-200">
        <h2 class="text-lg font-semibold">{{ $t('Lịch sử thanh toán') }}</h2>
      </div>
      <el-table :data="paymentHistory" stripe>
        <el-table-column prop="date" :label="$t('Ngày thanh toán')" width="150">
          <template #default="{ row }">
            {{ formatDate(row.date) }}
          </template>
        </el-table-column>
        <el-table-column prop="amount" :label="$t('Số tiền')" width="150">
          <template #default="{ row }">
            {{ formatCurrency(row.amount) }}
          </template>
        </el-table-column>
        <el-table-column prop="method" :label="$t('Phương thức')" width="150">
          <template #default="{ row }">
            <el-tag :type="getPaymentMethodTag(row.method)">
              {{ row.method }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" :label="$t('Trạng thái')" width="150">
          <template #default="{ row }">
            <el-tag :type="getStatusTag(row.status)">
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="reference" :label="$t('Mã giao dịch')" min-width="200" />
      </el-table>
    </div>

    <!-- Tuition Details -->
    <div class="bg-white rounded-lg shadow overflow-hidden">
      <div class="p-4 border-b border-gray-200">
        <h2 class="text-lg font-semibold">{{ $t('Chi tiết học phí') }}</h2>
      </div>
      <el-table :data="tuitionDetails" stripe>
        <el-table-column prop="courseCode" :label="$t('Mã học phần')" width="150" />
        <el-table-column prop="courseName" :label="$t('Tên học phần')" min-width="250" />
        <el-table-column prop="credits" :label="$t('Số tín chỉ')" width="120" align="center" />
        <el-table-column prop="amount" :label="$t('Học phí')" width="150">
          <template #default="{ row }">
            {{ formatCurrency(row.amount) }}
          </template>
        </el-table-column>
        <el-table-column prop="type" :label="$t('Loại học phí')" width="150">
          <template #default="{ row }">
            <el-tag :type="getTuitionTypeTag(row.type)">{{ row.type }}</el-tag>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import dayjs from 'dayjs'
import { useI18n } from 'vue-i18n'
import type { PaymentHistory, TuitionDetail } from '@/types/websites/tuition'

// Set page metadata
definePageMeta({
  layout: 'websites'
})

const { t: $t } = useI18n()

// Sample payment history data
const paymentHistory = ref<PaymentHistory[]>([
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
const tuitionDetails = ref<TuitionDetail[]>([
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
const formatDate = (date: string): string => {
  return dayjs(date).format('DD/MM/YYYY')
}

const formatCurrency = (amount: number): string => {
  return new Intl.NumberFormat('vi-VN', {
    style: 'currency',
    currency: 'VND',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(amount)
}

type TagType = 'primary' | 'success' | 'warning' | 'info' | 'danger'

const getPaymentMethodTag = (method: PaymentHistory['method']): TagType => {
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

const getStatusTag = (status: PaymentHistory['status']): TagType => {
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

const getTuitionTypeTag = (type: TuitionDetail['type']): TagType => {
  switch (type) {
    case 'Học phí':
      return 'primary'
    case 'Phí khác':
      return 'warning'
    default:
      return 'info'
  }
}
</script>

<style scoped>
.el-table {
  border-radius: 0.5rem;
}

.el-card {
  border-radius: 0.5rem;
}
</style>
