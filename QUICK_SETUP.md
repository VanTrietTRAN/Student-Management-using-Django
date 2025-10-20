# 🚀 QUICK START - Cập nhật hệ thống với tính năng mới

## ⚠️ CHÚ Ý QUAN TRỌNG

Hệ thống đã được nâng cấp với nhiều tính năng mới. Bạn cần cập nhật database.

---

## 📋 BƯỚC 1: TẠO DATABASE

### Cách 1: Sử dụng PhpMyAdmin (XAMPP)

1. Mở **PhpMyAdmin**: `http://localhost/phpmyadmin`
2. Click tab **"SQL"**
3. Paste câu lệnh sau và click **"Go"**:

```sql
CREATE DATABASE student_management_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Cách 2: Sử dụng MySQL Command Line

```bash
mysql -u root -p
CREATE DATABASE student_management_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

---

## 📋 BƯỚC 2: CHẠY MIGRATIONS

Mở PowerShell tại thư mục dự án và chạy:

```powershell
# Activate virtual environment
.\.venv\Scripts\activate

# Run migrations
python manage.py migrate
```

**Kết quả mong đợi:**
```
Running migrations:
  Applying student_management_app.0004_subjects_credit_hours... OK
  Applying student_management_app.0004_subjects_fee_per_credit... OK
  ... (nhiều migrations khác)
```

---

## 📋 BƯỚC 3: IMPORT DỮ LIỆU MẪU (Optional)

Nếu bạn muốn có dữ liệu test sẵn:

### Cách 1: PhpMyAdmin
1. Vào database **student_management_system**
2. Click tab **"Import"**
3. Chọn file **database_xampp.sql**
4. Click **"Go"**

### Cách 2: MySQL Command Line
```bash
mysql -u root -p student_management_system < database_xampp.sql
```

**Lưu ý**: File `database_xampp.sql` đã có sẵn password **admin123** cho tất cả users.

---

## 📋 BƯỚC 4: CHẠY SERVER

```powershell
python manage.py runserver
```

Truy cập: `http://localhost:8000`

---

## 🔐 TÀI KHOẢN TEST

Tất cả password: **admin123**

| Email | Role |
|-------|------|
| admin@gmail.com | Admin/HOD |
| staff1@gmail.com | Lecturer |
| staff2@gmail.com | Lecturer |
| student1@gmail.com | Student |
| student2@gmail.com | Student |

---

## ✨ CÁC TÍNH NĂNG MỚI

### 🎓 Admin:
- ✅ **Quản lý học phí**: Thêm credit hours và fee per credit cho môn học
- ✅ **Thời khóa biểu**: Tạo lịch học theo thứ, giờ, phòng học
- ✅ **Tính toán tự động**: Tổng học phí = credit hours × fee per credit

### 👨‍🏫 Lecturer:
- ✅ **Upload PDF**: Upload file mô tả môn học (.pdf)
- ✅ **Quản lý file**: Xem, xóa file mô tả môn học

### 🎓 Student:
- ✅ **Đăng ký môn học**: Enroll/Drop subjects
- ✅ **Xem học phí**: Tổng học phí tự động từ môn đã đăng ký
- ✅ **Thời khóa biểu**: Xem lịch học theo tuần
- ✅ **Xem mô tả môn**: Download PDF mô tả môn học

---

## 📚 TÀI LIỆU CHI TIẾT

Xem file **FEATURES_GUIDE.md** để biết hướng dẫn chi tiết về từng tính năng.

---

## 🐛 TROUBLESHOOTING

### Lỗi "Unknown database"
→ Bạn chưa tạo database. Quay lại BƯỚC 1.

### Lỗi "No module named 'MySQLdb'"
→ Cài đặt: `pip install mysqlclient`

### Lỗi migration
→ Xóa file migration cũ và tạo lại:
```powershell
Remove-Item student_management_app\migrations\0*.py
python manage.py makemigrations
python manage.py migrate
```

### Lỗi "No such table"
→ Chạy lại: `python manage.py migrate`

---

## 📞 HỖ TRỢ

Nếu gặp vấn đề, kiểm tra:
1. ✅ XAMPP MySQL đã chạy chưa?
2. ✅ Database đã được tạo chưa?
3. ✅ Virtual environment đã activate chưa?
4. ✅ Migration đã chạy thành công chưa?

---

**Happy Coding!** 🚀
