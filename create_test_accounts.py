"""
Script để tạo tài khoản mới với mật khẩu đơn giản
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from student_management_app.models import CustomUser, AdminHOD, Staffs, Students, Courses, SessionYearModel

print("\n" + "="*70)
print("🔑 TẠO TÀI KHOẢN MỚI VỚI MẬT KHẨU ĐƠN GIẢN")
print("="*70 + "\n")

# Tạo tài khoản Admin mới
print("1️⃣  Tạo Admin Account mới...")
try:
    admin_user = CustomUser.objects.get(username="admin_test")
    print("   ⚠️  Admin 'admin_test' đã tồn tại")
except CustomUser.DoesNotExist:
    admin_user = CustomUser.objects.create_user(
        username="admin_test",
        email="admin_test@gmail.com",
        password="123456",  # Mật khẩu đơn giản
        user_type='1',
        first_name="Admin",
        last_name="Test"
    )
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.save()
    
    AdminHOD.objects.create(admin=admin_user)
    print("   ✅ Admin được tạo thành công!")

# Tạo tài khoản Lecturer mới
print("\n2️⃣  Tạo Lecturer Account mới...")
try:
    lecturer_user = CustomUser.objects.get(username="lecturer_test")
    print("   ⚠️  Lecturer 'lecturer_test' đã tồn tại")
except CustomUser.DoesNotExist:
    lecturer_user = CustomUser.objects.create_user(
        username="lecturer_test",
        email="lecturer_test@gmail.com",
        password="123456",  # Mật khẩu đơn giản
        user_type='2',
        first_name="Lecturer",
        last_name="Test"
    )
    lecturer_user.save()
    
    Staffs.objects.create(
        admin=lecturer_user,
        address="Test Address"
    )
    print("   ✅ Lecturer được tạo thành công!")

# Tạo tài khoản Student mới
print("\n3️⃣  Tạo Student Account mới...")
try:
    student_user = CustomUser.objects.get(username="student_test")
    print("   ⚠️  Student 'student_test' đã tồn tại")
except CustomUser.DoesNotExist:
    # Lấy course và session year đầu tiên
    course = Courses.objects.first()
    session_year = SessionYearModel.object.first()
    
    student_user = CustomUser.objects.create_user(
        username="student_test",
        email="student_test@gmail.com",
        password="123456",  # Mật khẩu đơn giản
        user_type='3',
        first_name="Student",
        last_name="Test"
    )
    student_user.save()
    
    Students.objects.create(
        admin=student_user,
        gender="Male",
        address="Test Address",
        course_id=course,
        session_year_id=session_year,
        profile_pic=""
    )
    print("   ✅ Student được tạo thành công!")

# Đặt lại mật khẩu cho tài khoản admin hiện có
print("\n4️⃣  Đặt lại mật khẩu cho tài khoản 'admin' hiện có...")
try:
    admin_existing = CustomUser.objects.get(username="admin")
    admin_existing.set_password("123456")
    admin_existing.save()
    print("   ✅ Mật khẩu đã được đặt lại thành '123456'")
except:
    print("   ⚠️  Không tìm thấy tài khoản 'admin'")

# Hiển thị thông tin tài khoản
print("\n" + "="*70)
print("✅ TẠO/CẬP NHẬT TÀI KHOẢN THÀNH CÔNG!")
print("="*70)
print("\n📋 THÔNG TIN ĐĂNG NHẬP:\n")

print("1️⃣  ADMIN (Tài khoản hiện có - mật khẩu đã reset)")
print("   • Username: admin")
print("   • Password: 123456")
print("   • Email: admin@gmail.com\n")

print("2️⃣  ADMIN TEST (Tài khoản mới)")
print("   • Username: admin_test")
print("   • Password: 123456")
print("   • Email: admin_test@gmail.com\n")

print("3️⃣  LECTURER TEST (Tài khoản mới)")
print("   • Username: lecturer_test")
print("   • Password: 123456")
print("   • Email: lecturer_test@gmail.com\n")

print("4️⃣  STUDENT TEST (Tài khoản mới)")
print("   • Username: student_test")
print("   • Password: 123456")
print("   • Email: student_test@gmail.com\n")

print("="*70)
print("🌐 Truy cập: http://127.0.0.1:8000/")
print("💡 Đăng nhập bằng Username và Password ở trên")
print("="*70 + "\n")
