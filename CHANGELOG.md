# 📝 CHANGELOG - Cập nhật hệ thống

## Version 2.0 - Tháng 10/2025

### ✨ Tính năng mới

#### 🎓 Admin Features:

1. **Quản lý Học phí**
   - Thêm trường `credit_hours` (Số tín chỉ) cho môn học
   - Thêm trường `fee_per_credit` (Học phí mỗi tín chỉ)
   - Tính toán tự động: `total_fee = credit_hours × fee_per_credit`
   - Hiển thị tổng học phí khi thêm/sửa môn học

2. **Quản lý Thời khóa biểu**
   - Model mới: `Schedule`
   - Tạo lịch học theo: Thứ, Giờ bắt đầu, Giờ kết thúc, Phòng học
   - Gán môn học và năm học cho lịch
   - Views: `/manage_schedule`, `/add_schedule`, `/edit_schedule`, `/delete_schedule`
   - Templates: Manage, Add, Edit schedule

#### 👨‍🏫 Lecturer Features:

1. **Upload Mô tả Môn học**
   - Thêm trường `subject_description_file` vào Subjects model
   - Upload file PDF mô tả môn học
   - Quản lý file: View, Delete
   - Views: `/manage_subject_description`, `/upload_subject_description`, `/delete_subject_description`
   - Template: manage_subject_description.html

#### 🎓 Student Features:

1. **Đăng ký Môn học**
   - Model mới: `StudentEnrollment`
   - Xem danh sách môn học có thể đăng ký
   - Đăng ký môn (Enroll)
   - Hủy đăng ký (Drop)
   - Validation: Không đăng ký trùng môn
   - Views: `/student_view_subjects`, `/student_enroll_subject`, `/student_drop_subject`
   - Template: view_subjects.html

2. **Xem Học phí**
   - Tính toán tự động tổng học phí từ các môn đã đăng ký
   - Hiển thị chi tiết: Môn, Tín chỉ, Học phí/tín chỉ, Tổng
   - Tổng tín chỉ và tổng học phí
   - View: `/student_view_fees`
   - Template: view_fees.html

3. **Xem Thời khóa biểu**
   - Hiển thị lịch học theo tuần
   - Nhóm theo ngày trong tuần
   - Chỉ hiển thị môn đã đăng ký
   - View: `/student_view_schedule`
   - Template: view_schedule.html

4. **Xem Mô tả Môn học**
   - View/Download file PDF mô tả môn
   - Xem thông tin môn học
   - View: `/student_view_subject_description/<subject_id>`
   - Template: view_subject_description.html

---

### 🗃 Database Changes

#### Models Updated:

**1. Subjects** (Updated)
```python
credit_hours = IntegerField(default=3)
fee_per_credit = DecimalField(max_digits=10, decimal_places=2, default=0)
subject_description_file = FileField(upload_to='subject_descriptions/', blank=True, null=True)
```

**2. StudentEnrollment** (New)
```python
student_id = ForeignKey(Students)
subject_id = ForeignKey(Subjects)
session_year_id = ForeignKey(SessionYearModel)
enrollment_date = DateTimeField(auto_now_add=True)
is_active = BooleanField(default=True)
unique_together = ('student_id', 'subject_id', 'session_year_id')
```

**3. Schedule** (New)
```python
subject_id = ForeignKey(Subjects)
session_year_id = ForeignKey(SessionYearModel)
weekday = IntegerField(choices=WEEKDAY_CHOICES)  # 0-6
start_time = TimeField()
end_time = TimeField()
room = CharField(max_length=100)
```

#### Migration Files:
- `0004_subjects_credit_hours_subjects_fee_per_credit_and_more.py`

---

### 📂 Files Changed

#### Views:
- `HodViews.py`: 
  - Updated: `add_subject_save()`, `edit_subject_save()`
  - Added: `manage_schedule()`, `add_schedule()`, `add_schedule_save()`, `edit_schedule()`, `edit_schedule_save()`, `delete_schedule()`

- `StaffViews.py`:
  - Added: `manage_subject_description()`, `upload_subject_description()`, `delete_subject_description()`

- `StudentViews.py`:
  - Added: `student_view_subjects()`, `student_enroll_subject()`, `student_drop_subject()`, `student_view_fees()`, `student_view_schedule()`, `student_view_subject_description()`

#### Templates:

**Admin (hod_template/):**
- `add_subject_template.html` - Updated with credit_hours, fee_per_credit fields
- `edit_subject_template.html` - Updated with credit_hours, fee_per_credit fields
- `manage_schedule_template.html` - New
- `add_schedule_template.html` - New
- `edit_schedule_template.html` - New

**Staff (staff_template/):**
- `manage_subject_description.html` - New

**Student (student_template/):**
- `view_subjects.html` - New
- `view_fees.html` - New
- `view_schedule.html` - New
- `view_subject_description.html` - New

#### URLs (urls.py):
```python
# Admin URLs
path('manage_schedule', HodViews.manage_schedule)
path('add_schedule', HodViews.add_schedule)
path('add_schedule_save', HodViews.add_schedule_save)
path('edit_schedule/<str:schedule_id>', HodViews.edit_schedule)
path('edit_schedule_save', HodViews.edit_schedule_save)
path('delete_schedule/<str:schedule_id>', HodViews.delete_schedule)

# Staff URLs
path('manage_subject_description', StaffViews.manage_subject_description)
path('upload_subject_description/<str:subject_id>', StaffViews.upload_subject_description)
path('delete_subject_description/<str:subject_id>', StaffViews.delete_subject_description)

# Student URLs
path('student_view_subjects', StudentViews.student_view_subjects)
path('student_enroll_subject/<str:subject_id>', StudentViews.student_enroll_subject)
path('student_drop_subject/<str:subject_id>', StudentViews.student_drop_subject)
path('student_view_fees', StudentViews.student_view_fees)
path('student_view_schedule', StudentViews.student_view_schedule)
path('student_view_subject_description/<str:subject_id>', StudentViews.student_view_subject_description)
```

---

### 📚 Documentation:
- `FEATURES_GUIDE.md` - Hướng dẫn chi tiết tất cả tính năng mới
- `QUICK_SETUP.md` - Hướng dẫn cài đặt nhanh
- `CHANGELOG.md` - File này

---

### 🔧 Technical Changes:

1. **Imports Updated**:
   - Added `StudentEnrollment`, `Schedule` to imports in views
   - Added `FileSystemStorage` for file uploads

2. **Methods Added**:
   - `Subjects.get_total_fee()` - Calculate total fee

3. **Validation**:
   - Unique constraint on StudentEnrollment
   - File type validation for PDF uploads

---

### 🐛 Bug Fixes:
- None (New features)

---

### 📌 TODO / Future Enhancements:

- [ ] Add email notifications for enrollment
- [ ] Add conflict detection for schedule (same time)
- [ ] Add payment gateway integration
- [ ] Add GPA calculation based on credits
- [ ] Add course prerequisites
- [ ] Add enrollment capacity limits
- [ ] Add waitlist functionality
- [ ] Export schedule to PDF/iCal
- [ ] Mobile responsive improvements

---

### 🔄 Migration Steps:

1. Create database:
```sql
CREATE DATABASE student_management_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

3. (Optional) Import sample data:
```bash
mysql -u root -p student_management_system < database_xampp.sql
```

---

### 👥 Credits:
- Developed by: GitHub Copilot
- Framework: Django 3.0.6
- Template: AdminLTE 3
- Database: MySQL

---

**Version**: 2.0  
**Release Date**: October 20, 2025  
**Status**: ✅ Completed
