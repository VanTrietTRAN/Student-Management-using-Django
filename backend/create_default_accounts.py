#!/usr/bin/env python
"""
Script to create default user accounts for the student information system.
Run this script after setting up the database.
"""

import os
import sys
import django
from django.conf import settings

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.temp')
django.setup()

from oauth.models import User
<<<<<<< HEAD
from businesses.models import Employee
=======
>>>>>>> 3b3381a6d34ff10ab244e9176bf5c5305c89c0c0
from django.core.management import call_command

def create_default_accounts():
    """Create default user accounts based on config.env settings"""

    # Default accounts
    accounts = [
        {
<<<<<<< HEAD
            'email': 'student@university.edu',
            'password': 'student123',
            'first_name': 'Sinh viên',
            'last_name': '',
=======
            'email': 'student@gmail.com',
            'password': '123456',
            'first_name': 'Sinh viên',
            'last_name': 'Nguyễn Văn An',
>>>>>>> 3b3381a6d34ff10ab244e9176bf5c5305c89c0c0
            'is_staff': False,
            'is_superuser': False,
            'user_type': 'student'
        },
        {
<<<<<<< HEAD
            'email': 'lecture@university.edu',
            'password': 'lecture123',
            'first_name': 'Giảng viên',
            'last_name': '',
=======
            'email': 'teacher@gmail.com',
            'password': '123456',
            'first_name': 'Giảng viên',
            'last_name': 'teacher',
>>>>>>> 3b3381a6d34ff10ab244e9176bf5c5305c89c0c0
            'is_staff': True,
            'is_superuser': False,
            'user_type': 'teacher'
        },
        {
<<<<<<< HEAD
            'email': 'admin@university.edu',
            'password': 'admin123',
=======
            'email': 'training@gmail.com',
            'password': '123456',
            'first_name': 'Nhân viên',
            'last_name': 'Phòng đào tạo',
            'is_staff': True,
            'is_superuser': False
        },
        {
            'email': 'studentaffairs@gmail.com',
            'password': '123456',
            'first_name': 'Nhân viên',
            'last_name': 'Phòng công tác sinh viên',
            'is_staff': True,
            'is_superuser': False
        },
        {
            'email': 'quynhtruong272@gmail.com',
            'password': '295239272',
>>>>>>> 3b3381a6d34ff10ab244e9176bf5c5305c89c0c0
            'first_name': 'Quản trị viên',
            'last_name': '',
            'is_staff': True,
            'is_superuser': True,
            'user_type': 'admin'
        }
    ]
<<<<<<< HEAD
    
    print("Creating default user accounts...")

    # Ensure OAuth client applications exist (business/ecommerce)
    try:
        call_command('init_oauth_clients')
        print('OAuth client applications initialized')
    except Exception as e:
        print('Failed to initialize OAuth clients:', e)
    
    for account in accounts:
        email = account['email']
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            print(f"User {email} already exists, skipping...")
            continue
        # Create user
        user = User.objects.create_user(
            email=account['email'],
=======

    print("🔧 Creating default user accounts...\n")

    for account in accounts:
        email = account['email']
        if User.objects.filter(email=email).exists():
            print(f"⚠️ User {email} already exists, skipping...")
            continue

        user = User.objects.create_user(
            email=email,
>>>>>>> 3b3381a6d34ff10ab244e9176bf5c5305c89c0c0
            password=account['password'],
            first_name=account['first_name'],
            last_name=account['last_name'],
            is_staff=account['is_staff'],
            is_superuser=account['is_superuser']
        )
<<<<<<< HEAD
        user.user_type = account['user_type']
        user.save()
        # Tạo employee liên kết nếu chưa có
        if not Employee.objects.filter(user=user).exists():
            emp = Employee.objects.create(
                user=user,
                first_name=account['first_name'],
                last_name=account['last_name'],
                work_mail=account['email'],
                status=1  # Active
            )
            print(f"Created employee for: {email}")
        else:
            print(f"Employee already exists for: {email}")
        print(f"Created user: {email} ({account['first_name']})")
    
    print("\nDefault accounts created successfully!")
    print("\nLogin credentials:")
    print("Student: student@university.edu / student123")
    print("Lecture: lecture@university.edu / lecture123")
    print("Admin: admin@university.edu / admin123")
=======

        print(f"✅ Created user: {email} ({account['first_name']} {account['last_name']})")

    print("\n🎉 Default accounts created successfully!")
    print("\n🔐 Login credentials:")
    print("👩‍🎓 Student: student@gmail.com / 123456")
    print("👨‍🏫 Teacher: teacher@gmail.com / 123456")
    print("🏢 Training Staff: training@gmail.com / 123456")
    print("📋 Student Affairs: studentaffairs@gmail.com / 123456")
    print("🛠 Admin: quynhtruong272@gmail.com / 295239272")
>>>>>>> 3b3381a6d34ff10ab244e9176bf5c5305c89c0c0

if __name__ == '__main__':
    create_default_accounts()