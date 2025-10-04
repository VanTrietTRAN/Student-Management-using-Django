# Hệ thống Quản lý Sinh viên (Django + Nuxt.js)

Hệ thống quản lý sinh viên toàn diện với 3 vai trò: Admin, Giảng viên và Sinh viên.

## Tính năng chính

### 1. Quản trị viên (Admin)
- Quản lý người dùng (thêm/sửa/xóa tài khoản)
- Quản lý môn học và phân công giảng viên
- Quản lý lớp học và thời khóa biểu
- Quản lý học phí và kết quả học tập
- Cấu hình hệ thống và gửi thông báo

### 2. Giảng viên
- Xem danh sách lớp và sinh viên
- Điểm danh và theo dõi chuyên cần
- Nhập điểm và đánh giá sinh viên
- Gửi thông báo đến lớp học
- Xuất báo cáo điểm

### 3. Sinh viên
- Quản lý thông tin cá nhân
- Đăng ký/hủy đăng ký môn học
- Xem thời khóa biểu và lịch thi
- Xem điểm và học phí
- Nhận thông báo

## Yêu cầu hệ thống

- Python 3.12+
- Node.js 18+
- MySQL 8.0+
- Git

## Cài đặt và Chạy

### 1. Clone dự án

```powershell
git clone https://github.com/VanTrietTRAN/Student-Management-using-Django.git
cd Student-Management-using-Django
```

### 2. Thiết lập Backend (Django)

```powershell
# Tạo và kích hoạt môi trường ảo
py -3 -m venv .venv
.venv\Scripts\Activate.ps1

# Cài đặt dependencies
cd backend

# Cài đặt Pillow trước
pip install Pillow==10.0.0

# Cài đặt các package cơ bản
pip install -r requirements/temp.txt

# Cài đặt các package còn lại
pip install -r requirements/base.txt --no-deps

# Nếu gặp lỗi khi cài đặt package nào đó, có thể cài riêng package đó với lệnh:
# pip install <tên-package>==<version>

# Tạo file cấu hình
Copy-Item config.env.template config.env
# Chỉnh sửa config.env với thông tin database và cấu hình khác

# Tạo RSA key cho OAuth
openssl genrsa -out oidc.key 4096

# Tạo migrations và apply
python manage.py makemigrations
python manage.py migrate

# Tạo tài khoản mặc định
python create_default_accounts.py

# Chạy server
python manage.py runserver
```

### 3. Thiết lập Frontend (Nuxt.js)

```powershell
# Di chuyển vào thư mục frontend
cd ../business

# Cài đặt dependencies
npm install

# Chạy ở chế độ development
npm run dev
```

## Tài khoản mặc định

Hệ thống được tạo sẵn với 3 tài khoản mặc định:

1. Admin:
   - Email: admin@university.edu
   - Mật khẩu: admin123

2. Giảng viên:
   - Email: lecture@university.edu
   - Mật khẩu: lecture123

3. Sinh viên:
   - Email: student@university.edu
   - Mật khẩu: student123

## Cấu trúc dự án

```
Student-Management-using-Django/
├── backend/                 # Django backend
│   ├── base/               # Core components
│   ├── businesses/         # Business logic
│   ├── contents/           # Content management
│   ├── websites/          # Main application
│   └── manage.py
├── business/              # Nuxt.js frontend
│   ├── components/
│   ├── pages/
│   ├── services/
│   └── nuxt.config.ts
└── requirements/         # Python dependencies
```

## Phát triển

### Backend Development

1. API Endpoints:
   - Admin API: `http://localhost:8000/websites/admin/`
   - Student API: `http://localhost:8000/websites/student/`
   - Teacher API: `http://localhost:8000/websites/teacher/`

2. Database Migrations:
```powershell
python manage.py makemigrations
python manage.py migrate
```

### Frontend Development

1. Cấu trúc thư mục:
   - `pages/`: Các trang chính
   - `components/`: Components có thể tái sử dụng
   - `services/`: Các service gọi API
   - `stores/`: Vuex stores

2. Biên dịch và chạy:
```powershell
# Development
npm run dev

# Production build
npm run build
npm run start
```

## Xử lý sự cố

### Backend

1. Lỗi Database:
   - Kiểm tra cấu hình trong `config.env`
   - Đảm bảo MySQL đang chạy
   - Thử xóa và tạo lại migrations

2. Lỗi Authentication:
   - Kiểm tra `oidc.key` đã được tạo
   - Đảm bảo các tài khoản mặc định đã được tạo
   - Xóa token và đăng nhập lại

### Frontend

1. Lỗi API:
   - Kiểm tra backend đang chạy
   - Xem console để debug
   - Kiểm tra cấu hình API trong `nuxt.config.ts`

2. Lỗi Build:
   - Xóa `.nuxt`, `node_modules`
   - Cài lại dependencies
   - Chạy lại với `npm run dev`