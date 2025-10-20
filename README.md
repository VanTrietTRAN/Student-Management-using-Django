# 🎓 Student Management System - Django

A comprehensive Student Management System built with Django, MySQL, and AdminLTE template.

## ✨ Features (Updated October 2025)

### 🛠 Admin (HOD) Features:
- ✅ **User Management**: Add/Edit/Delete Staff and Students
- ✅ **Course Management**: Create and manage courses
- ✅ **Subject Management with Fees**: 
  - Add credit hours and fee per credit
  - Automatic calculation of total subject fee
- ✅ **Schedule Management**: Create weekly timetables with time slots
- ✅ **Results Management**: View and manage student results
- ✅ **Attendance Reports**: Monitor attendance across all classes
- ✅ **Notifications**: Send system-wide notifications to staff and students

### 👨‍🏫 Lecturer (Staff) Features:
- ✅ **Attendance Management**: Take and update attendance
- ✅ **Results Entry**: Add exam marks and assignment marks
- ✅ **Subject Description**: Upload PDF course descriptions
- ✅ **Student Monitoring**: View enrolled students
- ✅ **Live Classroom**: Start online classes
- ✅ **Leave Management**: Apply for leave

### 🎓 Student Features:
- ✅ **Course Enrollment**: Register/Drop subjects
- ✅ **Fee Calculation**: View tuition fees based on enrolled subjects
- ✅ **Schedule Viewing**: See weekly timetable
- ✅ **Course Materials**: View/Download subject descriptions (PDF)
- ✅ **Attendance Tracking**: View attendance reports
- ✅ **Results**: Check exam and assignment marks
- ✅ **Notifications**: Receive announcements
- ✅ **Profile Management**: Update personal information

---

## 🚀 Quick Start

### Prerequisites:
```bash
Python 3.13+
MySQL 5.7+ (XAMPP recommended)
Virtual Environment
```

### Installation:

1. **Clone the repository**
```bash
git clone <repository-url>
cd ERP
```

2. **Create and activate virtual environment**
```bash
python -m venv .venv
.\.venv\Scripts\activate  # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create MySQL database**
```sql
CREATE DATABASE student_management_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

5. **Update database settings in `settings.py`**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'student_management_system',
        'USER': 'root',
        'PASSWORD': '',  # Your MySQL password
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

6. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

7. **Import sample data (Optional)**
```bash
# Using MySQL command line
mysql -u root -p student_management_system < database_xampp.sql

# OR use PhpMyAdmin Import feature
```

8. **Run the server**
```bash
python manage.py runserver
```

9. **Access the application**
```
http://localhost:8000
```

---

## 🔐 Test Accounts

Staff:    dmdat@uni.com / admin
Student:  hhhoa@std.uni.com / admin
Admin:    admin01@uni.com / admin

## 📚 Documentation

### 📖 **[DOCUMENTATION.md](DOCUMENTATION.md)** - Complete Documentation

File tài liệu duy nhất chứa mọi thông tin bạn cần:
- ✅ Hướng dẫn cài đặt chi tiết
- ✅ Tất cả tính năng của hệ thống
- ✅ Hướng dẫn sử dụng cho Admin, Lecturer, Student
- ✅ Cấu trúc database và code
- ✅ Troubleshooting
- ✅ Testing checklist
- ✅ Ví dụ thực tế

**Đọc file này để hiểu đầy đủ về hệ thống!** 📘

---

## 🗂 Project Structure

```
ERP/
├── student_management_app/      # Main Django app
│   ├── models.py               # Database models
│   ├── views.py                # Main views
│   ├── HodViews.py             # Admin views
│   ├── StaffViews.py           # Lecturer views
│   ├── StudentViews.py         # Student views
│   ├── templates/              # HTML templates
│   │   ├── hod_template/       # Admin templates
│   │   ├── staff_template/     # Lecturer templates
│   │   └── student_template/   # Student templates
│   └── static/                 # Static files (CSS, JS)
├── student_management_system/   # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── media/                      # Uploaded files
├── static/                     # Static assets
├── requirements.txt            # Python dependencies
└── manage.py                   # Django management script
```

---

## 🔧 Key Technologies

- **Backend**: Django 3.0.6
- **Database**: MySQL 5.7+
- **Frontend**: AdminLTE 3, Bootstrap 4, jQuery
- **Authentication**: Django Custom User with Email Backend
- **Password Hashing**: pbkdf2_sha256 (1,000,000 iterations)

---

## 🌟 New Features in v2.0

### Fee Management System:
- Admin sets credit hours and fee per credit for each subject
- System automatically calculates: `Total Fee = Credit Hours × Fee Per Credit`
- Students can view total tuition based on enrolled subjects

### Course Enrollment:
- Students can browse available subjects
- Self-enrollment with validation
- View enrolled subjects status
- Drop subjects before deadline

### Schedule Management:
- Admin creates weekly timetables
- Assign time slots, rooms, and lecturers
- Students view personalized schedules
- Conflict detection for time slots

### Course Materials:
- Lecturers upload PDF course descriptions
- Students download course materials
- Version control for uploaded files

---

## ⚙️ Configuration

### reCAPTCHA Setup:
1. Get keys from: https://www.google.com/recaptcha/intro/v3.html
2. In `login_page.html` replace: `CAPTCHA_CLIENT_KEY`
3. In `views.py` replace: `CAPTCHA_SERVER_KEY`

### Media Files:
```python
# settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

---

## 🐛 Troubleshooting

### Database Connection Error:
- Ensure MySQL service is running
- Check database credentials in `settings.py`
- Verify database exists

### Migration Issues:
```bash
# Delete old migrations
Remove-Item student_management_app\migrations\0*.py

# Create fresh migrations
python manage.py makemigrations
python manage.py migrate
```

### Module Not Found:
```bash
pip install -r requirements.txt
```

---

## 📊 Database Schema

### Key Models:

**Subjects** - Enhanced with fees
- credit_hours: Integer (default: 3)
- fee_per_credit: Decimal (10,2)
- subject_description_file: FileField

**StudentEnrollment** - New model
- Links students to subjects
- Tracks enrollment status
- Unique constraint per session

**Schedule** - New model
- Weekly timetable entries
- Time slots and room assignments
- Links to subjects and sessions

---

## 🤝 Contributing

This is a student project. Feel free to fork and enhance!

---

## 📄 License

See [LICENSE](LICENSE) file for details.

---

## 🎉 Version History

- **v2.0** (October 2025) - Added fee management, enrollment, schedule features
- **v1.0** (Initial) - Basic student management system

---

**Happy Learning!** 🚀📚
