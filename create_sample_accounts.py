"""
Script để tạo tài khoản mẫu cho hệ thống Student Management
Chạy: python create_sample_accounts.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from student_management_app.models import CustomUser, SessionYearModel, Courses, Subjects, AdminHOD, Staffs, Students

def create_sample_accounts():
    print("\n" + "="*60)
    print("TẠO TÀI KHOẢN MẪU CHO HỆ THỐNG STUDENT MANAGEMENT")
    print("="*60 + "\n")
    
    # 1. Tạo Session Year
    print("📅 Tạo Session Year...")
    session_year, created = SessionYearModel.objects.get_or_create(
        session_start_year="2024-01-01",
        session_end_year="2024-12-31",
        defaults={"id": 1}
    )
    print(f"   ✓ Session Year: {session_year.session_start_year} - {session_year.session_end_year}")
    
    # 2. Tạo Course
    print("\n📚 Tạo Course...")
    course, created = Courses.objects.get_or_create(
        course_name="Computer Science",
        defaults={
            "created_at": "2024-01-01",
            "updated_at": "2024-01-01"
        }
    )
    print(f"   ✓ Course: {course.course_name}")
    
    # 3. Tạo Admin Account
    print("\n👨‍💼 Tạo ADMIN Account...")
    try:
        admin_user = CustomUser.objects.get(email="admin@example.com")
        print(f"   ⚠ Admin đã tồn tại: admin@example.com")
    except CustomUser.DoesNotExist:
        admin_user = CustomUser.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="admin123",
            user_type=1,
            first_name="Admin",
            last_name="System"
        )
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()
        
        AdminHOD.objects.create(
            admin=admin_user
        )
        print(f"   ✓ Admin được tạo: admin@example.com / admin123")
    
    # 4. Tạo Staff/Lecturer Account
    print("\n👨‍🏫 Tạo LECTURER Account...")
    try:
        staff_user = CustomUser.objects.get(email="lecturer@example.com")
        print(f"   ⚠ Lecturer đã tồn tại: lecturer@example.com")
    except CustomUser.DoesNotExist:
        staff_user = CustomUser.objects.create_user(
            username="lecturer1",
            email="lecturer@example.com",
            password="lecturer123",
            user_type=2,
            first_name="John",
            last_name="Doe"
        )
        staff_user.save()
        
        Staffs.objects.create(
            admin=staff_user,
            address="123 University Ave"
        )
        print(f"   ✓ Lecturer được tạo: lecturer@example.com / lecturer123")
    
    # 5. Tạo Student Accounts
    print("\n👨‍🎓 Tạo STUDENT Accounts...")
    
    students_data = [
        {
            "username": "student1",
            "email": "student1@example.com",
            "password": "student123",
            "first_name": "Alice",
            "last_name": "Johnson",
            "address": "456 Student St",
            "gender": "Female"
        },
        {
            "username": "student2",
            "email": "student2@example.com",
            "password": "student123",
            "first_name": "Bob",
            "last_name": "Smith",
            "address": "789 Campus Rd",
            "gender": "Male"
        }
    ]
    
    for student_data in students_data:
        try:
            student_user = CustomUser.objects.get(email=student_data["email"])
            print(f"   ⚠ Student đã tồn tại: {student_data['email']}")
        except CustomUser.DoesNotExist:
            student_user = CustomUser.objects.create_user(
                username=student_data["username"],
                email=student_data["email"],
                password=student_data["password"],
                user_type=3,
                first_name=student_data["first_name"],
                last_name=student_data["last_name"]
            )
            student_user.save()
            
            Students.objects.create(
                admin=student_user,
                gender=student_data["gender"],
                address=student_data["address"],
                course_id=course,
                session_year_id=session_year,
                profile_pic=""
            )
            print(f"   ✓ Student được tạo: {student_data['email']} / {student_data['password']}")
    
    # 6. Tạo Subject mẫu
    print("\n📖 Tạo Subject mẫu...")
    try:
        subject = Subjects.objects.get(subject_name="Python Programming")
    except Subjects.DoesNotExist:
        staff = Staffs.objects.first()
        if staff:
            subject = Subjects.objects.create(
                subject_name="Python Programming",
                course_id=course,
                staff_id=staff,
                credit_hours=3,
                fee_per_credit=100.00,
                created_at="2024-01-01",
                updated_at="2024-01-01"
            )
            print(f"   ✓ Subject: {subject.subject_name} (3 credits, $100/credit)")
        else:
            print(f"   ⚠ Chưa có Staff để gán Subject")
    
    # Hiển thị thông tin tài khoản
    print("\n" + "="*60)
    print("🎉 TẠO TÀI KHOẢN THÀNH CÔNG!")
    print("="*60)
    print("\n📋 DANH SÁCH TÀI KHOẢN ĐĂNG NHẬP:\n")
    
    print("1️⃣  ADMIN (Quản trị viên)")
    print("   • Email: admin@example.com")
    print("   • Password: admin123")
    print("   • Quyền: Quản lý toàn hệ thống\n")
    
    print("2️⃣  LECTURER (Giảng viên)")
    print("   • Email: lecturer@example.com")
    print("   • Password: lecturer123")
    print("   • Quyền: Quản lý môn học, điểm danh, nhập điểm\n")
    
    print("3️⃣  STUDENT 1 (Sinh viên)")
    print("   • Email: student1@example.com")
    print("   • Password: student123")
    print("   • Tên: Alice Johnson\n")
    
    print("4️⃣  STUDENT 2 (Sinh viên)")
    print("   • Email: student2@example.com")
    print("   • Password: student123")
    print("   • Tên: Bob Smith\n")
    
    print("="*60)
    print("🌐 Truy cập hệ thống tại: http://127.0.0.1:8000/")
    print("="*60 + "\n")

if __name__ == "__main__":
    create_sample_accounts()
