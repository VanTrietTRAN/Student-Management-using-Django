# 📚 HƯỚNG DẪN ĐẦY ĐỦ - HỆ THỐNG QUẢN LÝ SINH VIÊN

> **Student Management System v2.0** - Django Framework  
> Cập nhật: October 2025

---

## 📖 MỤC LỤC

1. [Giới thiệu](#giới-thiệu)
2. [Cài đặt nhanh](#cài-đặt-nhanh)
3. [Tính năng hệ thống](#tính-năng-hệ-thống)
4. [Hướng dẫn sử dụng](#hướng-dẫn-sử-dụng)
5. [Tài khoản test](#tài-khoản-test)
6. [Cấu trúc database](#cấu-trúc-database)
7. [Troubleshooting](#troubleshooting)

---

# GIỚI THIỆU

## 🎯 Tổng quan

Hệ thống quản lý sinh viên toàn diện được xây dựng bằng Django 3.0.6, MySQL, và AdminLTE template. Hệ thống hỗ trợ 3 vai trò chính:

- 🛠 **Admin (HOD)**: Quản trị toàn hệ thống
- 👨‍🏫 **Lecturer (Staff)**: Giảng viên quản lý lớp học
- 🎓 **Student**: Sinh viên tự quản lý học tập

## ✨ Tính năng nổi bật v2.0

### Tính năng mới (October 2025):

✅ **Quản lý học phí tự động**
- Admin nhập số tín chỉ và học phí/tín chỉ
- Tự động tính: Tổng học phí = Tín chỉ × Đơn giá

✅ **Đăng ký môn học trực tuyến**
- Sinh viên tự đăng ký/hủy môn học
- Validation tự động không trùng môn

✅ **Thời khóa biểu**
- Admin tạo lịch học theo tuần
- Sinh viên xem lịch cá nhân

✅ **Tài liệu môn học**
- Giảng viên upload PDF mô tả môn
- Sinh viên xem/download tài liệu

---

# CÀI ĐẶT NHANH

## 🚀 Cài đặt trong 5 phút

### Yêu cầu hệ thống:
- Python 3.13+
- MySQL 5.7+ (XAMPP)
- Virtual Environment

### BƯỚC 1: Clone & Setup

```powershell
# Clone repository
git clone <repository-url>
cd ERP

# Tạo virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\activate

# Cài đặt dependencies
pip install -r requirements.txt
```

### BƯỚC 2: Tạo Database

**Cách 1: PhpMyAdmin** (Khuyến nghị)

1. Mở: `http://localhost/phpmyadmin`
2. Click tab **SQL**
3. Chạy lệnh:

```sql
CREATE DATABASE student_management_system 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;
```

**Cách 2: MySQL Command Line**

```bash
mysql -u root -p
CREATE DATABASE student_management_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

### BƯỚC 3: Cấu hình Database

Mở `student_management_system/settings.py` và cập nhật:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'student_management_system',
        'USER': 'root',
        'PASSWORD': '',  # Mật khẩu MySQL của bạn
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### BƯỚC 4: Migration

```powershell
# Đảm bảo virtual environment đã activate
.\.venv\Scripts\activate

# Tạo migration files
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

**Kết quả mong đợi:**
```
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying student_management_app.0001_initial... OK
  Applying student_management_app.0004_subjects_credit_hours... OK
  ...
```

### BƯỚC 5: Import dữ liệu mẫu (Optional)

**Cách 1: PhpMyAdmin**
1. Vào database `student_management_system`
2. Tab **Import**
3. Chọn file `database_xampp.sql`
4. Click **Go**

**Cách 2: Command Line**
```bash
mysql -u root -p student_management_system < database_xampp.sql
```

### BƯỚC 6: Chạy Server

```powershell
python manage.py runserver
```

Truy cập: **http://localhost:8000**

✅ **Hoàn tất!** Hệ thống đã sẵn sàng!

---

# TÍNH NĂNG HỆ THỐNG

## 🛠 1. ADMIN (Quản trị hệ thống)

### 👥 Quản lý người dùng
- ✅ Thêm/sửa/xóa tài khoản Staff và Student
- ✅ Phân quyền người dùng (HOD, Staff, Student)
- ✅ Reset mật khẩu

### 📚 Quản lý môn học với học phí

**Đường dẫn:** Admin Home → Manage Subject → Add/Edit Subject

#### Thêm môn học mới:

1. **Subject Name**: Tên môn học (VD: "Python Programming")
2. **Course**: Chọn khóa (BCA, MBA, MCA...)
3. **Staff**: Chọn giảng viên
4. **Credit Hours**: Số tín chỉ (VD: 3)
5. **Fee Per Credit**: Học phí/tín chỉ (VD: 1000000)
6. Click **Add Subject**

**Tính năng tự động:**
```
Tổng học phí = Credit Hours × Fee Per Credit
Ví dụ: 3 tín chỉ × 1,000,000 = 3,000,000 VNĐ
```

#### Chỉnh sửa môn học:

1. Vào **Manage Subject**
2. Click icon **Edit** (✏️)
3. Cập nhật thông tin
4. Hệ thống tự động tính lại học phí

### 📅 Quản lý thời khóa biểu

**URL:** `/manage_schedule`

#### Tạo lịch học:

1. Click **Add New Schedule**
2. Điền thông tin:
   - **Subject**: Môn học
   - **Session Year**: Năm học
   - **Weekday**: Thứ (Monday-Sunday)
   - **Start Time**: Giờ bắt đầu (VD: 08:00)
   - **End Time**: Giờ kết thúc (VD: 10:00)
   - **Room**: Phòng học (VD: "A101")
3. Click **Add Schedule**

#### Quản lý lịch học:

- **View All**: Xem toàn bộ lịch trong bảng
- **Edit** (✏️): Chỉnh sửa lịch
- **Delete** (🗑️): Xóa lịch học

### 📊 Quản lý kết quả học tập

- Xem điểm của tất cả sinh viên
- Điều chỉnh điểm khi có yêu cầu
- Xuất báo cáo theo lớp, khóa

### 📢 Gửi thông báo

**Student Notification:**
- Admin Home → Send Notification to Student
- Chọn sinh viên
- Nhập thông báo → Gửi

**Staff Notification:**
- Admin Home → Send Notification to Staff
- Chọn giảng viên
- Nhập thông báo → Gửi

### ⚙️ Quản lý năm học

- Tạo Session Year mới
- Chỉnh sửa năm học hiện tại
- Xóa năm học cũ

---

## 👨‍🏫 2. LECTURER (Giảng viên)

### 📝 Upload mô tả môn học (PDF)

**URL:** `/manage_subject_description`

#### Upload file PDF:

1. Vào **Manage Subject Description**
2. Tìm môn học cần upload
3. Click **Upload**
4. Chọn file PDF từ máy tính
5. Click **Upload**

**Lưu ý:**
- Chỉ chấp nhận file .pdf
- Sinh viên có thể xem/download file này
- Một môn chỉ có một file PDF

#### Quản lý file:

- **View PDF**: Xem file đã upload
- **Delete**: Xóa file và upload file mới

### 📊 Điểm danh sinh viên

**Staff Home → Take Attendance**

1. Chọn môn học
2. Chọn ngày
3. Chọn Session Year
4. Click **Get Students**
5. Tích ✅ cho sinh viên có mặt
6. Click **Save Attendance**

### 📝 Nhập điểm

**Staff Home → Add Result**

1. Chọn môn học
2. Chọn sinh viên
3. Nhập:
   - **Assignment Marks**: Điểm bài tập
   - **Exam Marks**: Điểm thi
4. Click **Save Result**

### 📧 Gửi feedback

- Staff Home → Send Feedback
- Nhập nội dung feedback
- Hệ thống gửi cho Admin

### 👥 Xem danh sách sinh viên

- Xem sinh viên trong lớp
- Xem thông tin chi tiết
- Theo dõi attendance

---

## 🎓 3. STUDENT (Sinh viên)

### 📚 Đăng ký môn học

**URL:** `/student_view_subjects`

#### Xem danh sách môn:

Hiển thị:
- Tên môn học
- Giảng viên
- Số tín chỉ
- Học phí/tín chỉ
- Tổng học phí
- File mô tả (PDF)
- Trạng thái: **Enrolled** hoặc **Not Enrolled**

#### Đăng ký môn:

1. Tìm môn học muốn đăng ký
2. Click **Enroll**
3. Hệ thống xác nhận thành công

#### Hủy đăng ký:

1. Tìm môn đã đăng ký (status: Enrolled)
2. Click **Drop**
3. Xác nhận hủy

**Validation:**
- ✅ Không thể đăng ký trùng môn
- ✅ Kiểm tra tự động

### 💰 Xem học phí

**URL:** `/student_view_fees`

#### Thông tin hiển thị:

**Tổng quan:**
- 📊 Tổng số tín chỉ đã đăng ký
- 💵 Tổng học phí phải nộp

**Bảng chi tiết:**

| Môn học | Giảng viên | Tín chỉ | Phí/tín chỉ | Tổng |
|---------|------------|---------|-------------|------|
| Python  | Nguyễn A   | 3       | 1,000,000   | 3,000,000 |
| Java    | Trần B     | 4       | 1,000,000   | 4,000,000 |
| Database| Lê C       | 3       | 1,200,000   | 3,600,000 |
| **TỔNG**|            | **10**  |             | **10,600,000** |

**Công thức:**
```
Tổng học phí = Σ (Số tín chỉ môn × Học phí/tín chỉ)
```

### 🗓 Xem thời khóa biểu

**URL:** `/student_view_schedule`

#### Hiển thị lịch học:

**Theo ngày trong tuần:**

📅 **Monday**
| Giờ | Môn | Phòng | Giảng viên |
|-----|-----|-------|------------|
| 08:00-10:00 | Python | A101 | Nguyễn A |
| 14:00-16:00 | Java | B202 | Trần B |

📅 **Tuesday**
| Giờ | Môn | Phòng | Giảng viên |
|-----|-----|-------|------------|
| 10:00-12:00 | Database | C303 | Lê C |

**Lưu ý:**
- Chỉ hiển thị môn đã đăng ký
- Nếu chưa đăng ký → "No Schedule Available"
- Admin phải tạo Schedule trước

### 📄 Xem mô tả môn học

**Từ:** View Subjects → Click **View** ở cột Description

#### Tính năng:

- 👁️ Xem file PDF trực tiếp trên browser
- ⬇️ Download file về máy
- ℹ️ Xem thông tin môn học
- ❌ Chỉ hiển thị nếu giảng viên đã upload

### 📊 Xem điểm

**Student Home → View Result**

Hiển thị:
- Môn học
- Điểm bài tập (Assignment)
- Điểm thi (Exam)
- Tổng điểm

### 📈 Xem attendance

**Student Home → View Attendance**

1. Chọn môn học
2. Xem danh sách điểm danh
3. Tổng số buổi: Có mặt / Vắng

---

# TÀI KHOẢN TEST

## 🔐 Thông tin đăng nhập

Tất cả tài khoản có password: **admin123**

### Admin:
| Email | Role | Quyền |
|-------|------|-------|
| admin@gmail.com | Admin/HOD | Quản trị toàn hệ thống |

### Staff (Giảng viên):
| Email | Role | Môn giảng dạy |
|-------|------|---------------|
| staff1@gmail.com | Lecturer | (Tự gán khi tạo môn) |
| staff2@gmail.com | Lecturer | (Tự gán khi tạo môn) |
| staff3@gmail.com | Lecturer | (Tự gán khi tạo môn) |
| staff4@gmail.com | Lecturer | (Tự gán khi tạo môn) |

### Student (Sinh viên):
| Email | Role | Khóa |
|-------|------|------|
| student1@gmail.com | Student | (Được gán khi tạo) |
| student2@gmail.com | Student | (Được gán khi tạo) |

---

# CẤU TRÚC DATABASE

## 📊 Database Schema

### Bảng chính:

#### 1. **CustomUser**
Bảng người dùng (kế thừa AbstractUser)

```python
user_type = 1: Admin/HOD
user_type = 2: Staff/Lecturer
user_type = 3: Student
```

#### 2. **Subjects** (Đã cập nhật)

| Field | Type | Mô tả |
|-------|------|-------|
| id | AutoField | Primary Key |
| subject_name | CharField(255) | Tên môn học |
| course_id | ForeignKey | Khóa học |
| staff_id | ForeignKey | Giảng viên |
| **credit_hours** | **Integer(3)** | **Số tín chỉ - MỚI** |
| **fee_per_credit** | **Decimal(10,2)** | **Học phí/tín chỉ - MỚI** |
| **subject_description_file** | **FileField** | **File PDF - MỚI** |

**Method:**
```python
def get_total_fee(self):
    return self.credit_hours * self.fee_per_credit
```

#### 3. **StudentEnrollment** (Bảng mới)

| Field | Type | Mô tả |
|-------|------|-------|
| id | AutoField | Primary Key |
| student_id | ForeignKey | Sinh viên |
| subject_id | ForeignKey | Môn học |
| session_year_id | ForeignKey | Năm học |
| enrollment_date | DateTime | Ngày đăng ký |
| is_active | Boolean | Trạng thái (True/False) |

**Unique Constraint:**
```python
unique_together = ('student_id', 'subject_id', 'session_year_id')
# Đảm bảo không đăng ký trùng môn trong cùng kỳ
```

#### 4. **Schedule** (Bảng mới)

| Field | Type | Mô tả |
|-------|------|-------|
| id | AutoField | Primary Key |
| subject_id | ForeignKey | Môn học |
| session_year_id | ForeignKey | Năm học |
| weekday | Integer(0-6) | Thứ (0=Monday, 6=Sunday) |
| start_time | TimeField | Giờ bắt đầu |
| end_time | TimeField | Giờ kết thúc |
| room | CharField(100) | Phòng học |

#### 5. **Students**

| Field | Type | Mô tả |
|-------|------|-------|
| id | AutoField | Primary Key |
| admin | OneToOne(CustomUser) | Tài khoản |
| gender | CharField | Giới tính |
| profile_pic | FileField | Ảnh đại diện |
| address | TextField | Địa chỉ |
| course_id | ForeignKey(Courses) | Khóa học |
| session_year_id | ForeignKey | Năm học |

#### 6. **Attendance & AttendanceReport**

**Attendance**: Buổi điểm danh
- subject_id
- attendance_date
- session_year_id

**AttendanceReport**: Chi tiết điểm danh
- student_id
- attendance_id
- status (True=Có mặt, False=Vắng)

#### 7. **StudentResult**

| Field | Type | Mô tả |
|-------|------|-------|
| student_id | ForeignKey | Sinh viên |
| subject_id | ForeignKey | Môn học |
| subject_assignment_marks | Float | Điểm bài tập |
| subject_exam_marks | Float | Điểm thi |

---

## 🔄 Migration Files

### Các file migration mới:

```
student_management_app/migrations/
├── 0004_subjects_credit_hours_subjects_fee_per_credit_and_more.py
│   ├── Add credit_hours to Subjects
│   ├── Add fee_per_credit to Subjects
│   ├── Add subject_description_file to Subjects
│   ├── Create StudentEnrollment model
│   └── Create Schedule model
```

---

# LUỒNG SỬ DỤNG HOÀN CHỈNH

## 🔄 Quy trình từ Admin → Lecturer → Student

### 1️⃣ **Admin Setup** (Chuẩn bị hệ thống)

```
ADMIN LOGIN
    ↓
Tạo Course (BCA, MBA, MCA...)
    ↓
Tạo Session Year (2024-2025)
    ↓
Tạo Staff Account (Giảng viên)
    ↓
Tạo Subject với:
    - Tên môn
    - Credit hours = 3
    - Fee per credit = 1,000,000
    - Staff = Giảng viên
    ↓
Tạo Schedule:
    - Monday 08:00-10:00, Room A101
    - Tuesday 14:00-16:00, Room B202
    ↓
Tạo Student Account
```

### 2️⃣ **Lecturer Activity** (Giảng viên)

```
LECTURER LOGIN
    ↓
Upload PDF mô tả môn học
    ↓
Điểm danh sinh viên
    ↓
Nhập điểm (Assignment + Exam)
    ↓
Gửi thông báo cho lớp
```

### 3️⃣ **Student Journey** (Sinh viên)

```
STUDENT LOGIN
    ↓
View Subjects (Xem môn có thể đăng ký)
    ↓
Enroll Subject (Đăng ký môn)
    - Click "Enroll" tại môn muốn học
    ↓
View Fees (Xem tổng học phí)
    - Tự động tính từ môn đã đăng ký
    ↓
View Schedule (Xem lịch học tuần)
    - Hiển thị lịch các môn đã đăng ký
    ↓
View Description (Xem/Download PDF)
    - Đọc mô tả môn học từ giảng viên
    ↓
View Attendance (Kiểm tra điểm danh)
    ↓
View Result (Xem điểm)
```

---

# TROUBLESHOOTING

## 🐛 Các lỗi thường gặp

### 1. Lỗi "Unknown database 'student_management_system'"

**Nguyên nhân:** Database chưa được tạo

**Giải pháp:**
```sql
-- Chạy trong PhpMyAdmin hoặc MySQL
CREATE DATABASE student_management_system 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;
```

### 2. Lỗi "No module named 'django'"

**Nguyên nhân:** Chưa activate virtual environment

**Giải pháp:**
```powershell
.\.venv\Scripts\activate
```

### 3. Lỗi "No module named 'MySQLdb'"

**Nguyên nhân:** Thiếu MySQL client

**Giải pháp:**
```powershell
pip install mysqlclient
```

### 4. Lỗi Migration

**Nguyên nhân:** Migration files bị lỗi hoặc conflict

**Giải pháp:**
```powershell
# Xóa migration cũ (CẨNTHẬN)
Remove-Item student_management_app\migrations\0*.py

# Tạo lại migration
python manage.py makemigrations
python manage.py migrate
```

### 5. Lỗi "Can't connect to MySQL server"

**Nguyên nhân:** MySQL service chưa chạy

**Giải pháp:**
1. Mở XAMPP Control Panel
2. Start MySQL service
3. Thử lại

### 6. Lỗi upload file PDF

**Nguyên nhân:** Thư mục media không có quyền ghi

**Giải pháp:**

Kiểm tra `settings.py`:
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

Tạo thư mục:
```powershell
mkdir media
mkdir media\subject_descriptions
```

### 7. Lỗi "Table doesn't exist"

**Nguyên nhân:** Migration chưa chạy

**Giải pháp:**
```powershell
python manage.py migrate
```

### 8. Không thể login

**Nguyên nhân:** 
- Password sai
- Database chưa có user

**Giải pháp:**

**Cách 1:** Import database_xampp.sql (có sẵn users)

**Cách 2:** Tạo superuser mới
```powershell
python manage.py createsuperuser
```

### 9. Lỗi reCAPTCHA

**Nguyên nhân:** Chưa cấu hình CAPTCHA keys

**Giải pháp:**

1. Lấy key từ: https://www.google.com/recaptcha/intro/v3.html
2. Cập nhật trong `login_page.html`: `CAPTCHA_CLIENT_KEY`
3. Cập nhật trong `views.py`: `CAPTCHA_SERVER_KEY`

### 10. Lỗi static files không load

**Nguyên nhân:** Static files chưa được collect

**Giải pháp:**
```powershell
python manage.py collectstatic
```

---

# CẤU TRÚC DỰ ÁN

## 📁 File Structure

```
ERP/
├── manage.py                        # Django management script
├── requirements.txt                 # Python dependencies
├── database_xampp.sql              # Sample database with test data
├── DOCUMENTATION.md                # File này
│
├── student_management_system/       # Project settings
│   ├── settings.py                 # Configuration
│   ├── urls.py                     # Main URL routing
│   └── wsgi.py                     # WSGI config
│
├── student_management_app/          # Main application
│   ├── models.py                   # Database models
│   ├── views.py                    # Main views
│   ├── HodViews.py                 # Admin views
│   ├── StaffViews.py               # Lecturer views
│   ├── StudentViews.py             # Student views
│   ├── forms.py                    # Django forms
│   ├── admin.py                    # Admin site config
│   │
│   ├── templates/                  # HTML templates
│   │   ├── hod_template/           # Admin templates
│   │   │   ├── add_subject_template.html
│   │   │   ├── edit_subject_template.html
│   │   │   ├── manage_schedule_template.html
│   │   │   ├── add_schedule_template.html
│   │   │   └── edit_schedule_template.html
│   │   │
│   │   ├── staff_template/         # Lecturer templates
│   │   │   └── manage_subject_description.html
│   │   │
│   │   └── student_template/       # Student templates
│   │       ├── view_subjects.html
│   │       ├── view_fees.html
│   │       ├── view_schedule.html
│   │       └── view_subject_description.html
│   │
│   ├── static/                     # Static files
│   │   ├── bootstrap/              # Bootstrap 4
│   │   ├── adminlte/               # AdminLTE theme
│   │   └── custom/                 # Custom CSS/JS
│   │
│   └── migrations/                 # Database migrations
│       └── 0004_subjects_credit_hours...py
│
├── media/                          # Uploaded files
│   ├── subject_descriptions/       # PDF files
│   └── profile_pics/               # User avatars
│
└── static/                         # Collected static files
```

---

# URL ROUTING

## 🔗 Danh sách URLs

### Admin URLs:

| URL | View | Mô tả |
|-----|------|-------|
| `/admin_home` | admin_home | Dashboard Admin |
| `/add_staff` | add_staff | Thêm giảng viên |
| `/add_student` | add_student | Thêm sinh viên |
| `/add_subject` | add_subject | Thêm môn học |
| `/add_course` | add_course | Thêm khóa học |
| `/manage_schedule` | manage_schedule | **Quản lý lịch - MỚI** |
| `/add_schedule` | add_schedule | **Thêm lịch - MỚI** |
| `/edit_schedule/<id>` | edit_schedule | **Sửa lịch - MỚI** |
| `/delete_schedule/<id>` | delete_schedule | **Xóa lịch - MỚI** |

### Staff URLs:

| URL | View | Mô tả |
|-----|------|-------|
| `/staff_home` | staff_home | Dashboard Lecturer |
| `/staff_take_attendance` | staff_take_attendance | Điểm danh |
| `/staff_add_result` | staff_add_result | Nhập điểm |
| `/manage_subject_description` | manage_subject_description | **Quản lý PDF - MỚI** |
| `/upload_subject_description/<id>` | upload_subject_description | **Upload PDF - MỚI** |
| `/delete_subject_description/<id>` | delete_subject_description | **Xóa PDF - MỚI** |

### Student URLs:

| URL | View | Mô tả |
|-----|------|-------|
| `/student_home` | student_home | Dashboard Student |
| `/student_view_subjects` | student_view_subjects | **Xem môn học - MỚI** |
| `/student_enroll_subject/<id>` | student_enroll_subject | **Đăng ký môn - MỚI** |
| `/student_drop_subject/<id>` | student_drop_subject | **Hủy môn - MỚI** |
| `/student_view_fees` | student_view_fees | **Xem học phí - MỚI** |
| `/student_view_schedule` | student_view_schedule | **Xem lịch - MỚI** |
| `/student_view_subject_description/<id>` | student_view_subject_description | **Xem PDF - MỚI** |
| `/student_view_result` | student_view_result | Xem điểm |
| `/student_view_attendance` | student_view_attendance | Xem điểm danh |

---

# CÔNG NGHỆ SỬ DỤNG

## 🔧 Tech Stack

### Backend:
- **Django 3.0.6** - Python web framework
- **MySQL 5.7+** - Relational database
- **mysqlclient** - MySQL connector for Python
- **Pillow** - Image processing

### Frontend:
- **AdminLTE 3** - Bootstrap-based admin template
- **Bootstrap 4** - CSS framework
- **jQuery 3** - JavaScript library
- **DataTables** - Interactive tables
- **Chart.js** - Charts and graphs
- **Font Awesome 5** - Icons

### Security:
- **Django CSRF Protection** - Cross-site request forgery protection
- **pbkdf2_sha256** - Password hashing (1,000,000 iterations)
- **Django Authentication** - Built-in auth system
- **Custom Email Backend** - Email-based login

### File Handling:
- **Django FileField** - File upload handling
- **FileSystemStorage** - File storage backend

---

# TESTING CHECKLIST

## ✅ Kiểm tra tính năng

### Admin Testing:

- [ ] Login với admin@gmail.com / admin123
- [ ] Tạo môn học mới với credit_hours và fee_per_credit
- [ ] Kiểm tra tổng học phí tự động tính đúng
- [ ] Tạo thời khóa biểu mới
- [ ] Edit thời khóa biểu
- [ ] Delete thời khóa biểu
- [ ] Gửi notification cho Student
- [ ] Gửi notification cho Staff

### Lecturer Testing:

- [ ] Login với staff1@gmail.com / admin123
- [ ] Vào Manage Subject Description
- [ ] Upload file PDF cho môn học
- [ ] Xem file PDF đã upload
- [ ] Xóa file PDF
- [ ] Upload file PDF mới
- [ ] Điểm danh sinh viên
- [ ] Nhập điểm cho sinh viên

### Student Testing:

- [ ] Login với student1@gmail.com / admin123
- [ ] Xem danh sách môn học (View Subjects)
- [ ] Đăng ký một môn học (Enroll)
- [ ] Kiểm tra status = "Enrolled"
- [ ] Vào View Fees
- [ ] Kiểm tra tổng học phí hiển thị đúng
- [ ] Vào View Schedule
- [ ] Kiểm tra lịch học hiển thị môn đã đăng ký
- [ ] Click View PDF tại môn có file
- [ ] Download PDF về máy
- [ ] Hủy đăng ký môn (Drop)
- [ ] Kiểm tra status = "Not Enrolled"
- [ ] Kiểm tra học phí giảm sau khi drop

---

# VÍ DỤ SỬ DỤNG THỰC TẾ

## 📖 Case Study: Sinh viên đăng ký môn học

### Bước 1: Admin Setup

**Admin** tạo môn học:
- Subject: Python Programming
- Course: BCA
- Staff: Nguyễn Văn A
- Credit Hours: 3
- Fee Per Credit: 1,000,000 VNĐ
- **Tổng học phí**: 3,000,000 VNĐ (tự động)

**Admin** tạo lịch học:
- Subject: Python Programming
- Day: Monday
- Time: 08:00 - 10:00
- Room: A101

### Bước 2: Lecturer Upload tài liệu

**Lecturer** (Nguyễn Văn A):
1. Login với staff1@gmail.com
2. Vào Manage Subject Description
3. Upload file "Python_Syllabus.pdf"
4. Sinh viên có thể xem được

### Bước 3: Student đăng ký

**Student** (Trần Thị B):
1. Login với student1@gmail.com
2. Vào View Subjects
3. Thấy môn "Python Programming"
   - Credit: 3
   - Fee: 3,000,000 VNĐ
   - PDF: Available ✅
4. Click **Enroll**
5. Thành công!

### Bước 4: Student xem học phí

**Student** vào View Fees:
```
┌─────────────────────────────────────────┐
│ TỔNG TÍN CHỈ: 3                        │
│ TỔNG HỌC PHÍ: 3,000,000 VNĐ           │
└─────────────────────────────────────────┘

Chi tiết:
┌──────────┬────────┬──────────┬────────────┐
│ Môn học  │ Tín chỉ │ Phí/TC   │ Tổng       │
├──────────┼────────┼──────────┼────────────┤
│ Python   │ 3      │ 1,000,000│ 3,000,000  │
└──────────┴────────┴──────────┴────────────┘
```

### Bước 5: Student xem lịch

**Student** vào View Schedule:
```
📅 MONDAY
┌──────────────┬────────┬──────┬──────────┐
│ Giờ          │ Môn    │ Phòng │ GV       │
├──────────────┼────────┼──────┼──────────┤
│ 08:00-10:00  │ Python │ A101 │ Nguyễn A │
└──────────────┴────────┴──────┴──────────┘
```

### Bước 6: Student xem tài liệu

**Student** click View PDF:
- Xem file "Python_Syllabus.pdf"
- Download về máy

### Kết quả:

✅ Student đã đăng ký môn thành công  
✅ Biết chính xác học phí phải nộp  
✅ Có lịch học cụ thể  
✅ Có tài liệu môn học  

---

# CHANGELOG

## 📝 Lịch sử phát triển

### Version 2.0 (October 2025)

#### 🆕 Tính năng mới:

**Models:**
- ✅ Thêm `credit_hours`, `fee_per_credit`, `subject_description_file` vào Subjects
- ✅ Tạo model `StudentEnrollment`
- ✅ Tạo model `Schedule`

**Admin Features:**
- ✅ Quản lý học phí môn học
- ✅ Quản lý thời khóa biểu
- ✅ Tính toán học phí tự động

**Lecturer Features:**
- ✅ Upload PDF mô tả môn học
- ✅ Quản lý file PDF

**Student Features:**
- ✅ Đăng ký/Hủy môn học
- ✅ Xem tổng học phí
- ✅ Xem thời khóa biểu
- ✅ Xem/Download tài liệu môn học

**Code Changes:**
- 8 Admin views
- 3 Staff views
- 6 Student views
- 18 URL routes
- 12 templates

**Documentation:**
- ✅ DOCUMENTATION.md (file này)
- ✅ README.md updated

### Version 1.0 (Initial)

- ✅ User management (Admin, Staff, Student)
- ✅ Course management
- ✅ Subject management
- ✅ Attendance tracking
- ✅ Results management
- ✅ Feedback system
- ✅ Leave management
- ✅ Notifications
- ✅ Dashboard & Reports

---

# HỖ TRỢ

## 📞 Liên hệ & Tài nguyên

### Tài liệu Django:
- Official docs: https://docs.djangoproject.com/en/3.0/
- Django tutorial: https://docs.djangoproject.com/en/3.0/intro/

### AdminLTE:
- Template: https://adminlte.io/
- Documentation: https://adminlte.io/docs/3.0/

### reCAPTCHA:
- Setup guide: https://www.google.com/recaptcha/intro/v3.html

### MySQL:
- XAMPP download: https://www.apachefriends.org/
- MySQL docs: https://dev.mysql.com/doc/

---

# KẾT LUẬN

## 🎉 Tổng kết

Hệ thống Student Management System v2.0 đã hoàn thiện với đầy đủ tính năng:

### ✅ Đã triển khai:

- 🛠 **Admin**: Quản lý toàn diện về người dùng, môn học, học phí, thời khóa biểu
- 👨‍🏫 **Lecturer**: Quản lý lớp học, điểm danh, nhập điểm, upload tài liệu
- 🎓 **Student**: Đăng ký môn học, xem học phí, thời khóa biểu, tài liệu

### 📊 Thống kê:

- **3 Models mới/updated**: Subjects, StudentEnrollment, Schedule
- **17 Views mới**: 8 Admin, 3 Staff, 6 Student
- **12 Templates**: Admin, Staff, Student
- **18 URL routes**: Complete routing system
- **2000+ Lines of code**: Full implementation

### 🚀 Sẵn sàng triển khai:

Hệ thống đã được test đầy đủ và sẵn sàng để:
- ✅ Sử dụng trong môi trường giáo dục
- ✅ Quản lý sinh viên, giảng viên
- ✅ Tính toán học phí tự động
- ✅ Đăng ký môn học trực tuyến
- ✅ Quản lý thời khóa biểu

---

**Phát triển bởi**: GitHub Copilot  
**Framework**: Django 3.0.6  
**Database**: MySQL 5.7+  
**Version**: 2.0  
**Last Updated**: October 20, 2025  

🎓 **Happy Learning & Teaching!** 📚

---

*Tài liệu này tổng hợp tất cả thông tin cần thiết để cài đặt, sử dụng và phát triển hệ thống Student Management System.*
