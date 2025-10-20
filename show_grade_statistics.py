import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from student_management_app.models import StudentResult, Students

print("=" * 80)
print("THONG KE DIEM SO THEO THANG DIEM CHU")
print("=" * 80)

# Thống kê theo điểm chữ
grade_counts = {
    'A+': 0,  # >= 95
    'A': 0,   # 85-94
    'B': 0,   # 70-84
    'C': 0,   # 55-69
    'D': 0,   # 40-54
    'F': 0    # < 40
}

results = StudentResult.objects.all()
total_results = results.count()

print(f"\nTong so ket qua: {total_results}")
print("\nPhan tich chi tiet:\n")

for result in results:
    total = result.subject_assignment_marks + result.subject_exam_marks
    
    if total >= 95:
        grade_counts['A+'] += 1
    elif total >= 85:
        grade_counts['A'] += 1
    elif total >= 70:
        grade_counts['B'] += 1
    elif total >= 55:
        grade_counts['C'] += 1
    elif total >= 40:
        grade_counts['D'] += 1
    else:
        grade_counts['F'] += 1

# Hiển thị thống kê
print("Thong ke theo diem chu:")
print("-" * 60)
for grade, count in grade_counts.items():
    percentage = (count / total_results * 100) if total_results > 0 else 0
    bar = '█' * int(percentage / 2)
    
    if grade == 'A+':
        grade_range = ">= 95 (Xuat sac)"
    elif grade == 'A':
        grade_range = "85-94 (Gioi)"
    elif grade == 'B':
        grade_range = "70-84 (Kha)"
    elif grade == 'C':
        grade_range = "55-69 (Trung binh)"
    elif grade == 'D':
        grade_range = "40-54 (Dat yeu cau)"
    else:
        grade_range = "< 40 (Chua dat)"
    
    print(f"{grade:3} ({grade_range:22}): {count:3} ({percentage:5.1f}%) {bar}")

# Tỷ lệ đạt/không đạt
passed = grade_counts['A+'] + grade_counts['A'] + grade_counts['B'] + grade_counts['C'] + grade_counts['D']
failed = grade_counts['F']

print("\n" + "=" * 60)
print(f"DAT      : {passed:3} ({passed/total_results*100:5.1f}%)")
print(f"CHUA DAT : {failed:3} ({failed/total_results*100:5.1f}%)")
print("=" * 60)

# Thống kê theo student
print("\n\nThong ke theo sinh vien:")
print("-" * 80)

students = Students.objects.all()

for student in students[:5]:  # Hiển thị 5 student đầu tiên
    student_results = StudentResult.objects.filter(student_id=student)
    
    if not student_results.exists():
        continue
    
    print(f"\n{student.admin.username}:")
    
    for result in student_results:
        total = result.subject_assignment_marks + result.subject_exam_marks
        
        if total >= 95:
            grade = 'A+'
        elif total >= 85:
            grade = 'A'
        elif total >= 70:
            grade = 'B'
        elif total >= 55:
            grade = 'C'
        elif total >= 40:
            grade = 'D'
        else:
            grade = 'F'
        
        status = "DAT" if total >= 40 else "CHUA DAT"
        
        print(f"  {result.subject_id.subject_name:30} : {total:5.1f} [{grade:2}] {status}")

print("\n" + "=" * 80)
