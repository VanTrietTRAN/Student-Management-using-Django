#!/usr/bin/env python
import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')
django.setup()

from django.contrib.auth import get_user_model
from websites.models import Student, Teacher, Staff

User = get_user_model()

def create_default_accounts():
    """Tạo các tài khoản mặc định"""
    
    # Tạo tài khoản sinh viên mẫu
    student_user, created = User.objects.get_or_create(
        email='student@university.edu',
        defaults={
            'username': 'student',
            'first_name': 'Sinh',
            'last_name': 'Viên',
            'is_active': True
        }
    )
    if created:
        student_user.set_password('123456')
        student_user.save()
        print("✅ Tạo tài khoản sinh viên thành công")
    
    # Tạo tài khoản giảng viên mẫu
    teacher_user, created = User.objects.get_or_create(
        email='teacher@university.edu',
        defaults={
            'username': 'teacher',
            'first_name': 'Giảng',
            'last_name': 'Viên',
            'is_active': True
        }
    )
    if created:
        teacher_user.set_password('123456')
        teacher_user.save()
        print("✅ Tạo tài khoản giảng viên thành công")
    
    # Tạo tài khoản phòng đào tạo
    training_user, created = User.objects.get_or_create(
        email='training@university.edu',
        defaults={
            'username': 'training',
            'first_name': 'Phòng',
            'last_name': 'Đào tạo',
            'is_active': True
        }
    )
    if created:
        training_user.set_password('123456')
        training_user.save()
        print("✅ Tạo tài khoản phòng đào tạo thành công")
    
    # Tạo tài khoản phòng công tác sinh viên
    affairs_user, created = User.objects.get_or_create(
        email='studentaffairs@university.edu',
        defaults={
            'username': 'studentaffairs',
            'first_name': 'Phòng',
            'last_name': 'Công tác sinh viên',
            'is_active': True
        }
    )
    if created:
        affairs_user.set_password('123456')
        affairs_user.save()
        print("✅ Tạo tài khoản phòng công tác sinh viên thành công")
    
    # Tạo dữ liệu mẫu
    create_sample_data()

def create_sample_data():
    """Tạo dữ liệu mẫu"""
    
    # Tạo sinh viên mẫu
    student, created = Student.objects.get_or_create(
        student_id='SV001',
        defaults={
            'full_name': 'Nguyễn Văn An',
            'email': 'an.nguyen@email.com',
            'phone': '0123456789',
            'class_name': 'CNTT21A',
            'major': 'CNTT',
            'year': '2021',
            'status': 'Đang học',
            'gpa': 8.5
        }
    )
    if created:
        print("✅ Tạo sinh viên mẫu thành công")
    
    # Tạo giảng viên mẫu
    teacher, created = Teacher.objects.get_or_create(
        teacher_id='GV001',
        defaults={
            'full_name': 'ThS. Trần Thị Bình',
            'email': 'binh.tran@email.com',
            'phone': '0987654321',
            'department': 'Khoa Công nghệ thông tin',
            'position': 'Giảng viên',
            'degree': 'Thạc sĩ',
            'status': 'Đang làm việc'
        }
    )
    if created:
        print("✅ Tạo giảng viên mẫu thành công")
    
    # Tạo nhân viên mẫu
    staff, created = Staff.objects.get_or_create(
        staff_id='NV001',
        defaults={
            'full_name': 'Nguyễn Văn Cường',
            'email': 'cuong.nguyen@email.com',
            'phone': '0369852147',
            'department': 'Phòng đào tạo',
            'position': 'Chuyên viên',
            'role': 'Phòng đào tạo',
            'status': 'Đang làm việc'
        }
    )
    if created:
        print("✅ Tạo nhân viên mẫu thành công")

if __name__ == '__main__':
    print("🚀 Bắt đầu tạo tài khoản mặc định...")
    create_default_accounts()
    print("✅ Hoàn thành!")
