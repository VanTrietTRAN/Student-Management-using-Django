# 📚 HƯỚNG DẪN SỬ DỤNG HỆ THỐNG QUẢN LÝ SINH VIÊN - CÁC TÍNH NĂNG MỚI

## 🎯 TỔNG QUAN CẬP NHẬT

Hệ thống đã được nâng cấp với các tính năng quan trọng:
- ✅ **Quản lý học phí** (Credit Hours & Fee Per Credit)
- ✅ **Đăng ký môn học** (Student Enrollment)
- ✅ **Thời khóa biểu** (Schedule Management)
- ✅ **Upload mô tả môn học** (PDF Description)

---

## 🔄 CÁC BƯỚC CẬP NHẬT DATABASE

### Bước 1: Chạy Migration

```powershell
# Activate virtual environment
.\.venv\Scripts\activate

# Tạo migration files
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate
```

### Bước 2: Tạo Database MySQL (Nếu chưa có)

```sql
CREATE DATABASE student_management_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Sau đó cập nhật `settings.py`:

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

---

## 🛠 1. ADMIN (QUẢN TRỊ HỆ THỐNG)

### 👥 Quản lý Môn học với Học phí

**Đường dẫn**: Admin Home → Manage Subject → Add Subject / Edit Subject

#### Thêm Môn học Mới:
1. **Subject Name**: Nhập tên môn học (VD: "Python Programming")
2. **Course**: Chọn khóa học (BCA, MBA, MCA, etc.)
3. **Staff**: Chọn giảng viên phụ trách
4. **Credit Hours**: Nhập số tín chỉ (VD: 3)
5. **Fee Per Credit**: Nhập học phí mỗi tín chỉ (VD: 1000000)
6. Click **"Add Subject"**

**Tính toán tự động**:
- Tổng học phí môn = Credit Hours × Fee Per Credit
- VD: 3 tín chỉ × 1,000,000 = 3,000,000 VNĐ

#### Chỉnh sửa Môn học:
1. Vào **Manage Subject**
2. Click icon Edit (✏️) tại môn muốn sửa
3. Cập nhật thông tin
4. Hệ thống tự động tính lại tổng học phí

---

### 📅 Quản lý Thời khóa biểu

**Đường dẫn**: `/manage_schedule`

#### Tạo lịch học:
1. Click **"Add New Schedule"**
2. **Subject**: Chọn môn học
3. **Session Year**: Chọn năm học
4. **Weekday**: Chọn thứ trong tuần (Monday - Sunday)
5. **Start Time**: Giờ bắt đầu (VD: 08:00)
6. **End Time**: Giờ kết thúc (VD: 10:00)
7. **Room**: Nhập phòng học (VD: "A101")
8. Click **"Add Schedule"**

#### Xem/Sửa/Xóa lịch:
- **Manage Schedule**: Xem tất cả lịch học
- Click Edit (✏️) để chỉnh sửa
- Click Delete (🗑️) để xóa

---

### 📢 Gửi Thông báo

**Student Notification**:
- Đường dẫn: Admin Home → Send Notification to Student
- Chọn sinh viên và gửi thông báo

**Staff Notification**:
- Đường dẫn: Admin Home → Send Notification to Staff
- Chọn giảng viên và gửi thông báo

---

## 👨‍🏫 2. LECTURER (GIẢNG VIÊN)

### 📝 Upload Mô tả Môn học (PDF)

**Đường dẫn**: `/manage_subject_description`

#### Upload PDF:
1. Vào **Manage Subject Description**
2. Tìm môn học muốn upload
3. Click **"Upload"**
4. Chọn file PDF từ máy tính
5. Click **"Upload"**

**Lưu ý**:
- Chỉ chấp nhận file PDF
- Sinh viên sẽ xem được file này khi đăng ký môn

#### Xóa file mô tả:
- Click **"Delete"** tại môn có file
- Xác nhận xóa

---

### 📊 Quản lý Điểm danh & Nhập điểm

**Điểm danh**: Staff Home → Take Attendance
**Nhập điểm**: Staff Home → Add Result

---

## 🎓 3. STUDENT (SINH VIÊN)

### 📚 Đăng ký Học phần

**Đường dẫn**: `/student_view_subjects`

#### Xem danh sách môn:
- Hiển thị tất cả môn của khóa học
- Thông tin: Tên môn, Giảng viên, Tín chỉ, Học phí
- Trạng thái: Enrolled / Not Enrolled

#### Đăng ký môn:
1. Tìm môn muốn đăng ký
2. Click **"Enroll"**
3. Hệ thống xác nhận đăng ký thành công

#### Hủy đăng ký:
1. Tìm môn đã đăng ký
2. Click **"Drop"**
3. Xác nhận hủy

**Validation**:
- Không thể đăng ký trùng môn
- Hệ thống kiểm tra tự động

---

### 💰 Xem Học phí

**Đường dẫn**: `/student_view_fees`

#### Thông tin hiển thị:
- **Tổng số tín chỉ**: Tổng tín chỉ đã đăng ký
- **Tổng học phí**: Tổng tiền phải nộp

**Bảng chi tiết**:
- Tên môn
- Giảng viên
- Số tín chỉ
- Học phí mỗi tín chỉ
- Tổng học phí môn

**Công thức tính**:
```
Tổng học phí = Σ (Số tín chỉ môn × Học phí/tín chỉ)
```

**Ví dụ**:
```
Môn 1: Python (3 tín chỉ × 1,000,000) = 3,000,000
Môn 2: Java (4 tín chỉ × 1,000,000)   = 4,000,000
Môn 3: Database (3 tín chỉ × 1,200,000) = 3,600,000
----------------------------------------------
TỔNG: 10 tín chỉ                      = 10,600,000 VNĐ
```

---

### 🗓 Xem Thời khóa biểu

**Đường dẫn**: `/student_view_schedule`

#### Hiển thị:
- Lịch học theo từng thứ trong tuần
- Thông tin: Giờ học, Môn học, Phòng, Giảng viên
- Chỉ hiển thị môn đã đăng ký

**Lưu ý**:
- Nếu chưa đăng ký môn nào → Thông báo "No Schedule Available"
- Admin phải tạo Schedule trước

---

### 📄 Xem Mô tả Môn học

**Đường dẫn**: Từ trang **View Subjects** → Click **"View"** tại cột Description

#### Tính năng:
- Xem file PDF mô tả môn học
- Download file về máy
- Chỉ hiển thị nếu giảng viên đã upload

---

### 📊 Xem Kết quả Học tập

**Đường dẫn**: Student Home → View Result

- Xem điểm quá trình
- Xem điểm thi
- Xem GPA

---

## 🔑 TÀI KHOẢN TEST

Tất cả tài khoản có password: **admin123**

### Admin:
- Email: `admin@gmail.com`
- User type: HOD

### Staff (Giảng viên):
- Email: `staff1@gmail.com` đến `staff4@gmail.com`
- User type: Staff

### Student (Sinh viên):
- Email: `student1@gmail.com`, `student2@gmail.com`
- User type: Student

---

## 🗂 CẤU TRÚC DATABASE MỚI

### Bảng: Subjects (Cập nhật)
```sql
- credit_hours INT DEFAULT 3
- fee_per_credit DECIMAL(10,2) DEFAULT 0
- subject_description_file VARCHAR(100) NULL
```

### Bảng: StudentEnrollment (Mới)
```sql
- id (PK)
- student_id (FK → Students)
- subject_id (FK → Subjects)
- session_year_id (FK → SessionYearModel)
- is_active BOOLEAN DEFAULT TRUE
- enrollment_date DATETIME
- UNIQUE(student_id, subject_id, session_year_id)
```

### Bảng: Schedule (Mới)
```sql
- id (PK)
- subject_id (FK → Subjects)
- session_year_id (FK → SessionYearModel)
- weekday INT (0-6: Monday-Sunday)
- start_time TIME
- end_time TIME
- room VARCHAR(100)
```

---

## 🚀 LUỒNG SỬ DỤNG HOÀN CHỈNH

### Quy trình từ Admin đến Student:

```
1. ADMIN
   ↓
   - Tạo Course (BCA, MBA, etc.)
   - Tạo Session Year (2024-2025)
   - Tạo Staff (Giảng viên)
   - Tạo Subject với credit_hours + fee_per_credit
   - Tạo Schedule (Thời khóa biểu)
   
2. LECTURER
   ↓
   - Upload PDF mô tả môn học
   - Điểm danh sinh viên
   - Nhập điểm
   
3. STUDENT
   ↓
   - Đăng ký môn học (Enroll)
   - Xem học phí tổng
   - Xem thời khóa biểu
   - Xem mô tả môn học (PDF)
   - Xem điểm
```

---

## ⚙️ CÁC URL ROUTES MỚI

### Admin URLs:
```
/manage_schedule              - Quản lý thời khóa biểu
/add_schedule                 - Thêm lịch học
/edit_schedule/<id>           - Sửa lịch học
/delete_schedule/<id>         - Xóa lịch học
```

### Staff URLs:
```
/manage_subject_description              - Quản lý PDF mô tả
/upload_subject_description/<subject_id> - Upload PDF
/delete_subject_description/<subject_id> - Xóa PDF
```

### Student URLs:
```
/student_view_subjects                      - Xem môn học
/student_enroll_subject/<subject_id>        - Đăng ký môn
/student_drop_subject/<subject_id>          - Hủy đăng ký
/student_view_fees                          - Xem học phí
/student_view_schedule                      - Xem thời khóa biểu
/student_view_subject_description/<subject_id> - Xem PDF mô tả
```

---

## 🐛 TROUBLESHOOTING

### Lỗi khi migrate:
```powershell
# Xóa migration cũ
Remove-Item student_management_app\migrations\0*.py

# Tạo lại từ đầu
python manage.py makemigrations
python manage.py migrate
```

### Lỗi "Unknown database":
```sql
# Tạo database trong MySQL
CREATE DATABASE student_management_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Lỗi upload file PDF:
- Kiểm tra thư mục `media/` có quyền ghi
- Kiểm tra `settings.py` có cấu hình:
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

---

## 📝 TESTING CHECKLIST

### Admin:
- [ ] Tạo môn học với credit_hours và fee_per_credit
- [ ] Tính toán học phí tự động đúng
- [ ] Tạo thời khóa biểu
- [ ] Gửi thông báo cho Student/Staff

### Lecturer:
- [ ] Upload PDF mô tả môn học
- [ ] Xóa PDF
- [ ] Xem danh sách môn giảng dạy

### Student:
- [ ] Xem danh sách môn có thể đăng ký
- [ ] Đăng ký môn học
- [ ] Hủy đăng ký môn
- [ ] Xem tổng học phí chính xác
- [ ] Xem thời khóa biểu
- [ ] Xem/Download PDF mô tả môn

---

## 🎉 HOÀN TẤT!

Hệ thống đã sẵn sàng với đầy đủ tính năng:
✅ Quản lý học phí tự động
✅ Đăng ký môn học trực tuyến
✅ Thời khóa biểu
✅ Upload/xem mô tả môn học

**Happy Learning!** 🚀📚
