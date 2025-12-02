"""
Script to update student names and emails to meaningful Vietnamese names
Run this script with: python update_student_info.py
"""
import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from student_management_app.models import Students, CustomUser

# Vietnamese student names
VIETNAMESE_NAMES = [
    ("Nguyễn Văn An", "nguyenvanan", "Male"),
    ("Trần Thị Bình", "tranthibinh", "Female"),
    ("Lê Hoàng Cường", "lehoangcuong", "Male"),
    ("Phạm Thị Dung", "phamthidung", "Female"),
    ("Hoàng Minh Đức", "hoangminhduc", "Male"),
    ("Vũ Thị Hà", "vuthiha", "Female"),
    ("Đặng Quốc Hùng", "dangquochung", "Male"),
    ("Ngô Thị Lan", "ngothilan", "Female"),
    ("Bùi Văn Long", "buivanlong", "Male"),
    ("Đỗ Thị Mai", "dothimai", "Female"),
    ("Lương Anh Nam", "luonganhnam", "Male"),
    ("Phan Thị Nga", "phanthinga", "Female"),
    ("Trịnh Văn Phong", "trinhvanphong", "Male"),
    ("Võ Thị Quỳnh", "vothiquynh", "Female"),
    ("Đinh Minh Sơn", "dinhminhson", "Male"),
    ("Lý Thị Trang", "lythitrang", "Female"),
    ("Mai Văn Tuấn", "maivantuan", "Male"),
    ("Hồ Thị Uyên", "hothiuyen", "Female"),
    ("Dương Văn Vinh", "duongvanvinh", "Male"),
    ("Chu Thị Xuân", "chuthixuan", "Female"),
]

def update_student_names():
    """Update all student names and emails to meaningful Vietnamese names"""
    try:
        # Get all students
        students = Students.objects.all()
        
        print(f"Found {students.count()} student(s) in database")
        
        if students.count() == 0:
            print("\n✅ No students found. Nothing to update.")
            return
        
        print("\nCurrent student information:")
        for student in students:
            print(f"  ID {student.id}: {student.admin.first_name} {student.admin.last_name} ({student.admin.email})")
        
        print("\n🔄 Updating student names and emails...")
        updated_count = 0
        
        for idx, student in enumerate(students):
            if idx < len(VIETNAMESE_NAMES):
                full_name, username, gender = VIETNAMESE_NAMES[idx]
                name_parts = full_name.split(" ", 2)
                
                if len(name_parts) >= 3:
                    last_name = name_parts[0]
                    first_name = " ".join(name_parts[1:])
                else:
                    last_name = name_parts[0]
                    first_name = name_parts[1] if len(name_parts) > 1 else ""
                
                # Update CustomUser
                user = student.admin
                old_name = f"{user.first_name} {user.last_name}"
                old_email = user.email
                
                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                user.email = f"{username}@student.edu.vn"
                user.save()
                
                # Update Student gender
                student.gender = gender
                student.save()
                
                print(f"  ✅ Updated ID {student.id}:")
                print(f"     Name: {old_name} → {full_name}")
                print(f"     Email: {old_email} → {user.email}")
                print(f"     Username: → {username}")
                print(f"     Gender: → {gender}")
                
                updated_count += 1
            else:
                # If we have more students than names, use a pattern
                user = student.admin
                student_num = idx + 1
                
                user.first_name = f"Sinh Viên"
                user.last_name = f"Số {student_num}"
                user.username = f"student{student_num}"
                user.email = f"student{student_num}@student.edu.vn"
                user.save()
                
                student.gender = "Male" if student_num % 2 == 0 else "Female"
                student.save()
                
                print(f"  ✅ Updated ID {student.id}: Sinh Viên Số {student_num}")
                updated_count += 1
        
        print(f"\n✅ Successfully updated {updated_count} student(s)!")
        
        # Show updated information
        print(f"\n📋 Updated student list:")
        students = Students.objects.all()
        for student in students:
            print(f"  • {student.admin.last_name} {student.admin.first_name}")
            print(f"    Email: {student.admin.email} | Username: {student.admin.username} | Gender: {student.gender}")
            
    except Exception as e:
        print(f"\n❌ Error updating student information: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("=" * 70)
    print("STUDENT INFORMATION UPDATE TOOL - Vietnamese Names")
    print("=" * 70)
    update_student_names()
    print("=" * 70)
