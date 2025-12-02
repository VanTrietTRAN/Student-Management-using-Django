# 🎓 Hệ Thống Quản Lý Sinh Viên (Student Management System)

[![Django](https://img.shields.io/badge/Django-3.2+-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Hệ thống quản lý sinh viên toàn diện được xây dựng bằng Django Framework, cung cấp giải pháp quản lý học vụ hiện đại với giao diện thân thiện và nhiều tính năng mạnh mẽ.

![System Preview](screenshots/preview.png)

## ✨ Tính năng chính

### 🔐 Hệ thống phân quyền 3 cấp

#### 👨‍💼 **Admin (Quản trị viên)**
- **Quản lý người dùng**
  - Thêm, sửa, xóa giảng viên và sinh viên
  - Quản lý thông tin cá nhân và phân quyền
- **Quản lý đào tạo**
  - Quản lý khóa học (Courses)
  - Quản lý môn học (Subjects)
  - Quản lý năm học (Session Years)
  - Quản lý thời khóa biểu
- **Quản lý học tập**
  - Xem điểm danh các lớp học
  - Quản lý và nhập điểm theo môn học
- **Báo cáo & thống kê**
  - Dashboard với biểu đồ trực quan
  - Xuất báo cáo học tập
- **Giao tiếp**
  - Gửi thông báo cho sinh viên và giảng viên
  - Xem phản hồi từ sinh viên và giảng viên
  - Quản lý đơn xin nghỉ phép

#### 👨‍🏫 **Lecturer (Giảng viên)**
- **Quản lý lớp học phần**
  - Xem danh sách môn học được phân công
  - Xem danh sách sinh viên theo từng môn
  - Nhập điểm cho sinh viên
  - Quản lý mô tả môn học và tài liệu PDF
- **Điểm danh**
  - Điểm danh sinh viên theo buổi học
- **Giao tiếp**
  - Gửi thông báo cho sinh viên
  - Nhận và phản hồi từ sinh viên

#### 🎓 **Student (Sinh viên)**
- **Đăng ký môn học**
  - Xem danh sách môn học có thể đăng ký
  - Đăng ký/Hủy đăng ký môn học
  - Xem mô tả và tài liệu môn học
- **Học tập**
  - Xem thời khóa biểu tuần
  - Xem kết quả học tập và điểm số
  - Xem lịch sử điểm danh
- **Học phí**
  - Xem học phí theo môn học
  - Xem tổng học phí phải đóng
- **Giao tiếp**
  - Gửi phản hồi cho admin
  - Xem thông báo từ giảng viên và admin
  - Gửi đơn xin nghỉ phép

### 🎨 Giao diện hiện đại
- Theme gradient màu tím chuyên nghiệp
- Responsive design - Tương thích mobile
- Hiệu ứng hover và animations mượt mà
- Contrast màu sắc tối ưu cho accessibility
- Card-based layout trực quan

### 🔔 Hệ thống thông báo
- Thông báo real-time
- Phân loại thông báo theo người nhận
- Lịch sử thông báo

### 📊 Dashboard & Báo cáo
- Biểu đồ thống kê sinh viên, giảng viên, môn học
- Xuất báo cáo Excel/PDF
- Visualization dữ liệu trực quan

## 🚀 Công nghệ sử dụng

- **Backend**: Django 3.2+
- **Database**: SQLite (development) / MySQL/PostgreSQL (production)
- **Frontend**: 
  - AdminLTE 3 - Bootstrap 4
  - Font Awesome Icons
  - Custom CSS với Gradient Design
  - jQuery & DataTables
- **Python Libraries**:
  - Django ORM
  - Pillow (Image processing)
  - Requests

## 📋 Yêu cầu hệ thống

- Python 3.8 trở lên
- pip (Python package manager)
- Git

## 🔧 Cài đặt và khởi chạy

### 1️⃣ Clone repository

```bash
git clone https://github.com/VanTrietTRAN/Student-Management-using-Django.git
cd Student-Management-using-Django
```

### 2️⃣ Tạo môi trường ảo (Virtual Environment)

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3️⃣ Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Cấu hình database

File `settings.py` mặc định sử dụng SQLite. Nếu muốn sử dụng MySQL/PostgreSQL:

```python
# student_management_system/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_database_name',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 5️⃣ Chạy migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6️⃣ Tạo superuser (Admin)

```bash
python manage.py createsuperuser
```

Nhập thông tin:
- Email: admin@example.com
- Password: (chọn mật khẩu mạnh)

### 7️⃣ Thu thập static files

```bash
python manage.py collectstatic --noinput
```

### 8️⃣ Chạy development server

```bash
python manage.py runserver
```

Truy cập: **http://127.0.0.1:8000/**

## 👤 Tài khoản mặc định

Sau khi tạo superuser, bạn có thể:
1. Đăng nhập với tài khoản superuser
2. Tạo tài khoản Admin, Lecturer, Student trong hệ thống

### Hoặc sử dụng tài khoản demo (nếu đã có dữ liệu mẫu):

**Admin:**
- Email: `admin@example.com`
- Password: `admin123`

**Lecturer:**
- Email: `lecturer@example.com`
- Password: `lecturer123`

**Student:**
- Email: `student@example.com`
- Password: `student123`

## 📁 Cấu trúc thư mục

```
Student-Management-using-Django/
│
├── 📂 student_management_system/     # Django Project Configuration
│   ├── settings.py                   # Cấu hình chính: Database, Apps, Middleware
│   ├── urls.py                       # URL routing chính
│   ├── wsgi.py                       # WSGI configuration cho deployment
│   └── __init__.py
│
├── 📂 student_management_app/        # Main Application
│   │
│   ├── 📄 Core Files
│   │   ├── models.py                 # Database Models (CustomUser, Students, Subjects, etc.)
│   │   ├── admin.py                  # Django Admin configuration
│   │   ├── apps.py                   # App configuration
│   │   └── __init__.py
│   │
│   ├── 📄 Authentication & Middleware
│   │   ├── EmailBackEnd.py           # Custom email authentication backend
│   │   ├── LoginCheckMiddleWare.py   # Middleware kiểm tra quyền truy cập
│   │   └── context_processors.py     # Custom context processors
│   │
│   ├── 📄 Views Layer (MVC Pattern)
│   │   ├── views.py                  # General views (Login, Signup, Logout)
│   │   ├── HodViews.py               # Admin/HOD views (Quản lý hệ thống)
│   │   ├── StaffViews.py             # Lecturer views (Giảng viên)
│   │   ├── StudentViews.py           # Student views (Sinh viên)
│   │   └── EditResultVIewClass.py    # Class-based view cho edit results
│   │
│   ├── 📄 Forms
│   │   └── forms.py                  # Django Forms (AddStudent, EditStudent, etc.)
│   │
│   ├── 📂 templates/                 # HTML Templates (Organized by role)
│   │   ├── hod_template/             # ✅ Admin Interface
│   │   │   ├── base_template.html    #    └─ Base layout
│   │   │   ├── sidebar_template.html #    └─ Sidebar navigation
│   │   │   ├── home_content.html     #    └─ Dashboard
│   │   │   ├── manage_student_template.html
│   │   │   ├── manage_staff_template.html
│   │   │   ├── manage_subject_template.html
│   │   │   ├── manage_course_template.html
│   │   │   ├── manage_session_template.html
│   │   │   ├── manage_schedule_template.html
│   │   │   ├── admin_view_attendance.html
│   │   │   ├── admin_grade_subjects.html
│   │   │   ├── admin_enter_grades.html
│   │   │   ├── admin_reports.html
│   │   │   ├── student_feedback_template.html
│   │   │   ├── staff_feedback_template.html
│   │   │   ├── student_leave_view.html
│   │   │   ├── staff_leave_view.html
│   │   │   └── admin_view_notifications.html
│   │   │
│   │   ├── staff_template/           # ✅ Lecturer Interface
│   │   │   ├── base_template.html    #    └─ Base layout
│   │   │   ├── sidebar_template.html #    └─ Sidebar navigation
│   │   │   ├── home_content.html     #    └─ Dashboard
│   │   │   ├── staff_my_subjects.html
│   │   │   ├── staff_view_class_students.html
│   │   │   ├── staff_enter_grades.html
│   │   │   ├── staff_manage_subject_description.html
│   │   │   ├── manage_subject_description.html
│   │   │   ├── staff_take_attendance.html
│   │   │   ├── staff_update_attendance.html
│   │   │   ├── staff_apply_leave.html
│   │   │   ├── staff_feedback.html
│   │   │   ├── staff_profile.html
│   │   │   └── staff_all_notification.html
│   │   │
│   │   ├── student_template/         # ✅ Student Interface
│   │   │   ├── base_template.html    #    └─ Base layout
│   │   │   ├── sidebar_template.html #    └─ Sidebar navigation
│   │   │   ├── student_home_template.html
│   │   │   ├── view_subjects_new.html      # Card-based subject view
│   │   │   ├── view_schedule.html          # Thời khóa biểu
│   │   │   ├── view_subject_description.html
│   │   │   ├── student_view_attendance.html
│   │   │   ├── student_result.html
│   │   │   ├── view_fees.html
│   │   │   ├── student_apply_leave.html
│   │   │   ├── student_feedback.html
│   │   │   ├── student_profile.html
│   │   │   └── all_notification.html
│   │   │
│   │   ├── login_page.html           # Login interface
│   │   ├── signup_admin_page.html
│   │   ├── signup_staff_page.html
│   │   └── signup_student_page.html
│   │
│   ├── 📂 static/                    # Static Files (CSS, JS, Images)
│   │   ├── custom/
│   │   │   └── modern-theme.css      # ⭐ Custom theme với gradient design
│   │   ├── dist/                     # AdminLTE distribution files
│   │   ├── plugins/                  # jQuery, DataTables, FontAwesome, etc.
│   │   └── bootstrap/
│   │
│   ├── 📂 migrations/                # Database migrations
│   │   └── 0001_initial.py           # Initial schema
│   │
│   └── 📄 tests.py                   # Unit tests
│
├── 📂 media/                         # User uploaded files
│   ├── profile_pics/                 # Profile pictures
│   └── subject_descriptions/         # Subject PDF materials
│
├── 📂 static/                        # Collected static files (Production)
│   └── (Generated by collectstatic)
│
├── 📂 screenshots/                   # Application screenshots
│
├── 📄 Configuration Files
│   ├── manage.py                     # Django management script
│   ├── requirements.txt              # Python dependencies
│   ├── runtime.txt                   # Python version for Heroku
│   ├── Procfile                      # Heroku deployment config
│   ├── .gitignore                    # Git ignore rules
│   └── db.sqlite3                    # SQLite database (development)
│
├── 📄 Documentation
│   ├── README.md                     # This file
│   ├── UPDATE_NOTES.md              # Recent changes log
│   ├── LICENSE                       # MIT License
│   └── database.sql                  # Database schema export
│
└── 📂 .venv/                         # Virtual environment (not in git)
```

### 🎯 Giải thích cấu trúc theo chức năng:

#### 1. **Core Application Layer** (`student_management_app/`)
- **Models** (`models.py`): Định nghĩa 15+ models cho toàn bộ hệ thống
  - User Management: `CustomUser`, `Admin`, `Staffs`, `Students`
  - Academic: `Courses`, `Subjects`, `SessionYearModel`, `Schedule`
  - Assessment: `StudentResult`, `Attendance`, `AttendanceReport`
  - Enrollment: `StudentEnrollment`, `SubjectDescriptionFile`
  - Communication: `FeedBackStudent`, `FeedBackStaffs`, `LeaveReportStudent`, `LeaveReportStaff`
  - Notifications: `NotificationStudent`, `NotificationStaffs`

#### 2. **Presentation Layer** (Views)
Tổ chức theo **Role-Based Access Control (RBAC)**:

- **`views.py`**: Authentication & Public views
  - Login/Logout
  - Signup (Admin, Staff, Student)
  - Password Reset
  
- **`HodViews.py`**: Admin/Head of Department (30+ functions)
  - Dashboard & Statistics
  - CRUD operations: Staff, Student, Course, Subject, Session
  - Schedule Management
  - Attendance Monitoring
  - Grade Management
  - Reports & Analytics
  - Notification Broadcasting
  - Leave Management
  
- **`StaffViews.py`**: Lecturer Interface (25+ functions)
  - Personal Dashboard
  - My Subjects Management
  - Student List by Subject
  - Attendance Taking & Updates
  - Grade Entry & Export
  - Subject Materials Upload (PDF)
  - Student Notifications
  - Leave Applications
  
- **`StudentViews.py`**: Student Interface (15+ functions)
  - Personal Dashboard
  - Subject Enrollment/Drop
  - Schedule Viewing
  - Attendance History
  - Grade Viewing
  - Fee Calculation
  - Material Downloads
  - Feedback & Leave

#### 3. **Template Organization** (Frontend)
Tổ chức theo **Module Pattern**:

- **Base Templates**: Layout chung cho mỗi role
- **Sidebar Templates**: Navigation riêng cho mỗi role
- **Feature Templates**: Mỗi chức năng có template riêng
- **Responsive Design**: Bootstrap 4 + Custom CSS

#### 4. **Static Assets** (Frontend Resources)
```
static/
├── custom/modern-theme.css     # Custom styling (500+ lines)
├── dist/                       # AdminLTE core
├── plugins/                    # Third-party libraries
│   ├── datatables/            # Table management
│   ├── chart.js/              # Charts & graphs
│   ├── fontawesome-free/      # Icons
│   ├── daterangepicker/       # Date selection
│   └── summernote/            # Rich text editor
└── bootstrap/                  # Bootstrap framework
```

#### 5. **Business Logic Layer**
- **Forms** (`forms.py`): Validation & data processing
- **Middleware** (`LoginCheckMiddleWare.py`): Request/Response processing
- **Authentication** (`EmailBackEnd.py`): Custom auth logic
- **Context Processors** (`context_processors.py`): Global template variables

#### 6. **Data Layer**
- **Models**: ORM definitions
- **Migrations**: Database schema versioning
- **Media**: User-generated content storage

### 📊 Design Patterns Used:

1. **MVC/MVT Pattern**: Django's Model-View-Template
2. **Role-Based Access Control (RBAC)**: Separated views by user role
3. **DRY Principle**: Reusable base templates
4. **Separation of Concerns**: Views, Models, Templates separated
5. **Repository Pattern**: Models as data repositories
6. **Factory Pattern**: Form factories for different user types

## 🎯 Workflow sử dụng

### Quy trình hoạt động cơ bản:

1. **Admin** tạo:
   - Khóa học (Courses)
   - Năm học (Session Years)
   - Môn học (Subjects) và phân công giảng viên
   - Tài khoản Giảng viên và Sinh viên
   - Thời khóa biểu (Schedules)

2. **Sinh viên**:
   - Đăng nhập và đăng ký môn học
   - Xem thời khóa biểu
   - Xem tài liệu môn học
   - Theo dõi điểm số

3. **Giảng viên**:
   - Xem danh sách sinh viên trong lớp
   - Điểm danh sinh viên
   - Nhập điểm cho sinh viên
   - Upload tài liệu môn học

4. **Admin**:
   - Theo dõi và quản lý toàn bộ hệ thống
   - Xem báo cáo và thống kê
   - Xử lý phản hồi và đơn xin nghỉ

## 🔒 Bảo mật

- Authentication và Authorization với Django Auth
- Password hashing với PBKDF2
- CSRF Protection
- XSS Protection
- SQL Injection Protection (Django ORM)
- Session management
- ~~reCAPTCHA~~ (Đã loại bỏ để tối ưu UX)

## 🌐 Deploy lên Production

### Heroku:

```bash
# Cài đặt Heroku CLI
heroku login
heroku create your-app-name

# Push code
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser

# Collect static files
heroku run python manage.py collectstatic --noinput
```

### Cấu hình cho production:

```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com']

# Sử dụng PostgreSQL
DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://user:password@localhost/dbname'
    )
}

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

## 🛠️ Troubleshooting

### Lỗi: "No module named 'django'"
```bash
# Kích hoạt virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Cài đặt lại dependencies
pip install -r requirements.txt
```

### Lỗi: "Static files not found"
```bash
python manage.py collectstatic --noinput --clear
```

### Lỗi: Database connection
- Kiểm tra cấu hình DATABASES trong settings.py
- Đảm bảo database server đang chạy
- Kiểm tra credentials (username/password)

### CSS không load sau khi cập nhật
```bash
# Clear cache và collectstatic
python manage.py collectstatic --noinput --clear

# Clear browser cache: Ctrl + F5
```

## 📝 Changelog

### Version 2.0 (November 2025)
- ✅ Loại bỏ reCAPTCHA để cải thiện UX
- ✅ Tối ưu sidebar Admin với nhóm menu rõ ràng
- ✅ Tích hợp "Mô tả & File PDF" vào Quản lý lớp học phần (Lecturer)
- ✅ Tái thiết kế trang "Môn học" cho Student với Card Grid Layout
- ✅ Tách riêng "Thời khóa biểu" và "Môn học đã đăng ký"
- ✅ Theme mới với gradient màu tím (#5b21b6 → #7c3aed)
- ✅ Cải thiện tương phản màu sắc toàn bộ hệ thống
- ✅ Thêm animations và hover effects
- ✅ Responsive design cải tiến

## 🤝 Đóng góp

Contributions, issues và feature requests đều được hoan nghênh!

1. Fork repository
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## 📄 License

Dự án này được phân phối dưới [MIT License](LICENSE).

## 👨‍💻 Tác giả

**Van Triet TRAN**

- GitHub: [@VanTrietTRAN](https://github.com/VanTrietTRAN)
- Repository: [Student-Management-using-Django](https://github.com/VanTrietTRAN/Student-Management-using-Django)

## 🙏 Acknowledgments

- [Django Framework](https://www.djangoproject.com/)
- [AdminLTE](https://adminlte.io/)
- [Font Awesome](https://fontawesome.com/)
- [Bootstrap](https://getbootstrap.com/)

## 📞 Liên hệ & Hỗ trợ

Nếu bạn có bất kỳ câu hỏi hoặc cần hỗ trợ, vui lòng:
- Tạo [Issue](https://github.com/VanTrietTRAN/Student-Management-using-Django/issues)
- Email: your.email@example.com

---

⭐️ Nếu dự án hữu ích, hãy cho một star! ⭐️