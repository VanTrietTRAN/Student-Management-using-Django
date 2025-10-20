import os
import django
import random
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from student_management_app.models import StudentResult

print("=" * 80)
print("CAP NHAT LAI DIEM SO - TAO DATA THUC TE HON")
print("=" * 80)

# Lấy tất cả kết quả
results = StudentResult.objects.all()
total = results.count()

print(f"\nTong so ket qua: {total}")
print("\nCap nhat diem so...")

updated = 0
failed_count = 0

for result in results:
    # Random 20% sinh viên sẽ có điểm kém hơn
    if random.random() < 0.20:
        # Điểm bài tập thấp: 15-35
        result.subject_assignment_marks = round(random.uniform(15, 35), 1)
        # Điểm thi thấp: 20-55
        result.subject_exam_marks = round(random.uniform(20, 55), 1)
    else:
        # Điểm bài tập: 25-40
        result.subject_assignment_marks = round(random.uniform(25, 40), 1)
        # Điểm thi: 35-60
        result.subject_exam_marks = round(random.uniform(35, 60), 1)
    
    result.save()
    updated += 1
    
    total_score = result.subject_assignment_marks + result.subject_exam_marks
    if total_score < 40:
        failed_count += 1

print(f"\nDa cap nhat: {updated} ket qua")
print(f"So ket qua chua dat (F): {failed_count} ({failed_count/total*100:.1f}%)")
print("\n" + "=" * 80)
