"""
Script để liệt kê tất cả tài khoản trong hệ thống
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from student_management_app.models import CustomUser, AdminHOD, Staffs, Students

print("\n" + "="*70)
print("📋 DANH SÁCH TÀI KHOẢN TRONG HỆ THỐNG")
print("="*70 + "\n")

# Lấy tất cả users
all_users = CustomUser.objects.all()

if not all_users:
    print("⚠️  Không có tài khoản nào trong hệ thống!")
    print("\n💡 Hãy tạo tài khoản bằng lệnh:")
    print("   python manage.py createsuperuser")
else:
    # Admin/HOD accounts
    admins = CustomUser.objects.filter(user_type='1')
    if admins:
        print("👨‍💼 ADMIN/HOD ACCOUNTS:")
        print("-" * 70)
        for idx, admin in enumerate(admins, 1):
            print(f"\n{idx}️⃣  Admin Account:")
            print(f"   • Username: {admin.username}")
            print(f"   • Email: {admin.email}")
            print(f"   • Tên: {admin.first_name} {admin.last_name}")
            print(f"   • Is Superuser: {admin.is_superuser}")
            print(f"   • Is Staff: {admin.is_staff}")
            print(f"   • Password: [Đã mã hóa - không thể xem]")
            print(f"   • Gợi ý: Nếu bạn quên password, hãy chạy: python manage.py changepassword {admin.username}")
    
    # Staff/Lecturer accounts  
    staffs = CustomUser.objects.filter(user_type='2')
    if staffs:
        print("\n\n👨‍🏫 LECTURER/STAFF ACCOUNTS:")
        print("-" * 70)
        for idx, staff in enumerate(staffs, 1):
            print(f"\n{idx}️⃣  Lecturer Account:")
            print(f"   • Username: {staff.username}")
            print(f"   • Email: {staff.email}")
            print(f"   • Tên: {staff.first_name} {staff.last_name}")
            print(f"   • Password: [Đã mã hóa - không thể xem]")
            
            try:
                staff_info = Staffs.objects.get(admin=staff)
                print(f"   • Địa chỉ: {staff_info.address}")
            except:
                pass
    
    # Student accounts
    students = CustomUser.objects.filter(user_type='3')
    if students:
        print("\n\n👨‍🎓 STUDENT ACCOUNTS:")
        print("-" * 70)
        for idx, student in enumerate(students, 1):
            print(f"\n{idx}️⃣  Student Account:")
            print(f"   • Username: {student.username}")
            print(f"   • Email: {student.email}")
            print(f"   • Tên: {student.first_name} {student.last_name}")
            print(f"   • Password: [Đã mã hóa - không thể xem]")
            
            try:
                student_info = Students.objects.get(admin=student)
                print(f"   • Giới tính: {student_info.gender}")
                print(f"   • Địa chỉ: {student_info.address}")
                print(f"   • Khóa học: {student_info.course_id.course_name if student_info.course_id else 'N/A'}")
            except:
                pass

print("\n" + "="*70)
print("📝 GHI CHÚ:")
print("="*70)
print("• Mật khẩu đã được mã hóa trong database")
print("• Để đặt lại mật khẩu cho user, chạy:")
print("  python manage.py changepassword <username>")
print("\n• Để tạo admin mới, chạy:")
print("  python manage.py createsuperuser")
print("\n• Để đăng nhập, truy cập: http://127.0.0.1:8000/")
print("="*70 + "\n")
