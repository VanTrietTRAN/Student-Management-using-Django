export interface PaymentHistory {
  date: string
  amount: number
  method: 'Chuyển khoản' | 'VNPay' | 'Tiền mặt'
  status: 'Thành công' | 'Đang xử lý' | 'Thất bại'
  reference: string
}

export interface TuitionDetail {
  courseCode: string
  courseName: string
  credits: number
  amount: number
  type: 'Học phí' | 'Phí khác'
}