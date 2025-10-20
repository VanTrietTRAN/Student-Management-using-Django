# 📝 HƯỚNG DẪN ĐĂNG KÝ TÀI KHOẢN STUDENT

## 🎯 TỔNG QUAN

Hệ thống Student Management System hiện đã có **chức năng đăng ký tự động** cho sinh viên.
Sinh viên có thể tự đăng ký tài khoản và sau đó đăng nhập vào hệ thống.

## 📋 CÁC BƯỚC ĐĂNG KÝ

### Bước 1: Truy Cập Trang Đăng Ký

**Cách 1: Từ trang Login**
1. Mở trình duyệt và truy cập: `http://localhost:8000`
2. Click vào link **"Register as Student"** (có icon 👤)

**Cách 2: Truy cập trực tiếp**
- URL: `http://localhost:8000/signup_student`

### Bước 2: Điền Thông Tin

Điền đầy đủ các trường sau (TẤT CẢ đều bắt buộc):

| Trường | Mô Tả | Ví Dụ |
|--------|-------|-------|
| **Email** | Email của bạn (dùng để đăng nhập) | student@example.com |
| **First Name** | Tên | Nguyen |
| **Last Name** | Họ và tên đệm | Van A |
| **Username** | Tên đăng nhập (unique) | nguyenvana |
| **Password** | Mật khẩu (tối thiểu 8 ký tự) | mypassword123 |
| **Address** | Địa chỉ | 123 Nguyen Hue, TP.HCM |
| **Course** | Chọn khóa học từ dropdown | BCA, BBA, MBA, MCA |
| **Gender** | Giới tính | Male / Female / Other |
| **Profile Picture** | Ảnh đại diện (tùy chọn) | Chọn file .jpg/.png |
| **Session Year** | Năm học | 2020-2023 |

### Bước 3: Submit Form

1. Click nút **"Register as Student"** 
2. Hệ thống sẽ validate dữ liệu
3. Nếu thành công, bạn sẽ thấy thông báo: 
   > ✅ "Successfully Registered! You can now login with your credentials."
4. Tự động chuyển về trang Login

### Bước 4: Đăng Nhập

1. Tại trang login, nhập:
   - **Email**: Email bạn vừa đăng ký
   - **Password**: Password bạn vừa tạo
2. Click **"Sign In"**
3. Hệ thống sẽ đăng nhập và chuyển đến Student Dashboard

## ⚠️ LƯU Ý QUAN TRỌNG

### ✅ Validation

Hệ thống sẽ kiểm tra:
- ✔️ **Email unique**: Email chưa được sử dụng
- ✔️ **Username unique**: Username chưa tồn tại
- ✔️ **Password length**: Tối thiểu 8 ký tự
- ✔️ **Required fields**: Tất cả trường bắt buộc phải điền
- ✔️ **Course exists**: Khóa học phải tồn tại trong hệ thống
- ✔️ **Session year exists**: Năm học phải hợp lệ

### ❌ Lỗi Thường Gặp

**1. Username already exists**
- **Nguyên nhân**: Username đã có người dùng
- **Giải pháp**: Chọn username khác

**2. Email already exists**
- **Nguyên nhân**: Email đã được đăng ký
- **Giải pháp**: Sử dụng email khác hoặc đăng nhập nếu đã có tài khoản

**3. All fields are required**
- **Nguyên nhân**: Còn trường chưa điền
- **Giải pháp**: Kiểm tra lại và điền đầy đủ tất cả trường

**4. Password must be at least 8 characters long**
- **Nguyên nhân**: Password quá ngắn
- **Giải pháp**: Tạo password dài hơn 8 ký tự

**5. Selected course does not exist**
- **Nguyên nhân**: Khóa học không tồn tại
- **Giải pháp**: Chọn khóa học từ dropdown list

## 🔐 BẢO MẬT

### Password
- ✅ Password được hash tự động bởi Django (pbkdf2_sha256)
- ✅ KHÔNG BAO GIỜ lưu plain text password
- ✅ Sử dụng salt riêng cho mỗi user

### Email
- ✅ Sử dụng email để đăng nhập (thay vì username)
- ✅ Email phải unique trong hệ thống

## 📊 LUỒNG HOẠT ĐỘNG

```
[Trang Login] 
    ↓
[Click "Register as Student"]
    ↓
[Form Đăng Ký]
    ↓
[Điền thông tin]
    ↓
[Click "Register"]
    ↓
[Validation]
    ↓
┌─────────────────┐
│ Validation OK?  │
└─────────────────┘
    ↓ YES              ↓ NO
[Tạo CustomUser]    [Hiển thị lỗi]
    ↓                   ↓
[Tạo Student]       [Ở lại form]
    ↓
[Lưu vào DB]
    ↓
[Thông báo thành công]
    ↓
[Redirect to Login]
    ↓
[Đăng nhập]
    ↓
[Student Dashboard]
```

## 🗄️ CẤU TRÚC DATABASE

### Bảng: CustomUser
```sql
- id (PK)
- username (unique)
- email (unique)
- password (hashed)
- first_name
- last_name
- user_type = 3 (Student)
- is_active = True
- is_staff = False
```

### Bảng: Students
```sql
- id (PK)
- admin_id (FK → CustomUser)
- gender
- profile_pic
- address
- course_id (FK → Courses)
- session_year_id (FK → SessionYearModel)
- created_at
- updated_at
```

## 🎓 VÍ DỤ ĐĂNG KÝ

### Thông Tin Mẫu

```
Email: john.doe@example.com
First Name: John
Last Name: Doe
Username: johndoe2024
Password: SecurePass123
Address: 123 Main Street, City
Course: BCA (Bachelor of Computer Applications)
Gender: Male
Profile Picture: john_photo.jpg
Session Year: 2020 - 2023
```

### Kết Quả

Sau khi đăng ký thành công:
- ✅ 1 record trong bảng `CustomUser` (user_type=3)
- ✅ 1 record trong bảng `Students` (liên kết với CustomUser)
- ✅ Có thể đăng nhập ngay với email và password

## 🔧 CHO DEVELOPER

### URL Routes

```python
# views.py
path('signup_student', views.signup_student, name="signup_student")
path('do_signup_student', views.do_signup_student, name="do_signup_student")
```

### Views Functions

**signup_student(request)**
- Hiển thị form đăng ký
- Load danh sách Courses và SessionYear

**do_signup_student(request)**
- Xử lý POST request
- Validate dữ liệu
- Tạo CustomUser với user_type=3
- Tạo Student profile
- Redirect về login page

### Template

- **signup_student_page.html**: Form đăng ký student
- **login_page.html**: Có link đến trang đăng ký

## 📞 HỖ TRỢ

Nếu gặp vấn đề:
1. Kiểm tra console log (F12 trong browser)
2. Xem Django server logs
3. Đảm bảo database có dữ liệu Courses và SessionYear

## 🚀 TESTING

### Test Case 1: Đăng Ký Thành Công
```
1. Điền đầy đủ thông tin hợp lệ
2. Click Register
→ Kết quả: Thông báo success, redirect to login
```

### Test Case 2: Email Đã Tồn Tại
```
1. Điền email đã đăng ký
2. Click Register
→ Kết quả: Lỗi "Email already exists"
```

### Test Case 3: Password Ngắn
```
1. Điền password < 8 ký tự
2. Click Register
→ Kết quả: Alert "Password must be at least 8 characters long"
```

## ✨ TÍNH NĂNG

- ✅ **Tự đăng ký**: Không cần admin tạo tài khoản
- ✅ **Validation**: Kiểm tra dữ liệu đầu vào
- ✅ **Security**: Password hash tự động
- ✅ **User-friendly**: Giao diện rõ ràng, dễ sử dụng
- ✅ **Error handling**: Thông báo lỗi chi tiết
- ✅ **Auto login redirect**: Sau đăng ký → login → dashboard

---

**Happy Learning!** 🎓
