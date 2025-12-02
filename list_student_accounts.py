"""
Script to list all student accounts with login credentials
Run this script with: python list_student_accounts.py
"""
import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from student_management_app.models import Students, CustomUser

def list_student_accounts():
    """List all student accounts"""
    try:
        # Get all students
        students = Students.objects.all().order_by('id')
        
        print(f"\n{'='*80}")
        print(f"DANH SÁCH TÀI KHOẢN SINH VIÊN")
        print(f"{'='*80}")
        print(f"\nTổng số sinh viên: {students.count()}")
        print(f"\n{'='*80}")
        
        # Default password for all accounts (usually set during creation)
        default_password = "admin"
        
        print(f"\n⚠️  LƯU Ý: Mật khẩu mặc định cho tất cả tài khoản là: '{default_password}'")
        print(f"          (Nếu đã thay đổi, vui lòng liên hệ admin)\n")
        print(f"{'='*80}\n")
        
        for idx, student in enumerate(students, 1):
            user = student.admin
            print(f"{idx}. {user.last_name} {user.first_name}")
            print(f"   📧 Email: {user.email}")
            print(f"   👤 Username: {user.username}")
            print(f"   🔑 Password: {default_password}")
            print(f"   🎓 Khóa học: {student.course_id.course_name}")
            print(f"   📅 Niên khóa: {student.session_year_id.session_start_year} - {student.session_year_id.session_end_year}")
            print(f"   {'─'*76}")
        
        print(f"\n{'='*80}")
        print("HƯỚNG DẪN ĐĂNG NHẬP:")
        print(f"{'='*80}")
        print("1. Truy cập: http://127.0.0.1:8000/")
        print("2. Nhập Username hoặc Email")
        print(f"3. Nhập Password: {default_password}")
        print("4. Click 'Đăng nhập'")
        print(f"{'='*80}\n")
        
        # Save to file
        with open('student_accounts.txt', 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("DANH SÁCH TÀI KHOẢN SINH VIÊN\n")
            f.write("="*80 + "\n\n")
            f.write(f"Mật khẩu mặc định: {default_password}\n\n")
            f.write("="*80 + "\n\n")
            
            for idx, student in enumerate(students, 1):
                user = student.admin
                f.write(f"{idx}. {user.last_name} {user.first_name}\n")
                f.write(f"   Email: {user.email}\n")
                f.write(f"   Username: {user.username}\n")
                f.write(f"   Password: {default_password}\n")
                f.write(f"   Khóa học: {student.course_id.course_name}\n")
                f.write(f"   Niên khóa: {student.session_year_id.session_start_year} - {student.session_year_id.session_end_year}\n")
                f.write("   " + "─"*76 + "\n")
        
        print(f"✅ Đã lưu danh sách vào file: student_accounts.txt\n")
            
    except Exception as e:
        print(f"\n❌ Error listing accounts: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    list_student_accounts()
