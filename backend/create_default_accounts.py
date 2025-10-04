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
from django.core.management import call_command

def create_default_accounts():
    """Create default user accounts based on config.env settings"""

    # Default accounts
    accounts = [
        {
            'email': 'student@gmail.com',
            'password': '123456',
            'first_name': 'Sinh viên',
            'last_name': 'Nguyễn Văn An',
            'is_staff': False,
            'is_superuser': False
        },
        {
            'email': 'teacher@gmail.com',
            'password': '123456',
            'first_name': 'Giảng viên',
            'last_name': 'teacher',
            'is_staff': True,
            'is_superuser': False
        },
        {
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
            'first_name': 'Quản trị viên',
            'last_name': 'Hệ thống',
            'is_staff': True,
            'is_superuser': True
        }
    ]

    print("🔧 Creating default user accounts...\n")

    for account in accounts:
        email = account['email']
        if User.objects.filter(email=email).exists():
            print(f"⚠️ User {email} already exists, skipping...")
            continue

        user = User.objects.create_user(
            email=email,
            password=account['password'],
            first_name=account['first_name'],
            last_name=account['last_name'],
            is_staff=account['is_staff'],
            is_superuser=account['is_superuser']
        )

        print(f"✅ Created user: {email} ({account['first_name']} {account['last_name']})")

    print("\n🎉 Default accounts created successfully!")
    print("\n🔐 Login credentials:")
    print("👩‍🎓 Student: student@gmail.com / 123456")
    print("👨‍🏫 Teacher: teacher@gmail.com / 123456")
    print("🏢 Training Staff: training@gmail.com / 123456")
    print("📋 Student Affairs: studentaffairs@gmail.com / 123456")
    print("🛠 Admin: quynhtruong272@gmail.com / 295239272")

if __name__ == '__main__':
    create_default_accounts()