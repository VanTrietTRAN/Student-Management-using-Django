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
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')
django.setup()

from oauth.models import User
from businesses.models import Employee
from django.core.management import call_command

def create_default_accounts():
    """Create default user accounts based on config.env settings"""
    
    # Default accounts from config.env
    accounts = [
        {
            'email': 'student@university.edu',
            'password': 'student123',
            'first_name': 'Sinh viên',
            'last_name': '',
            'is_staff': False,
            'is_superuser': False,
            'user_type': 'student'
        },
        {
            'email': 'lecture@university.edu',
            'password': 'lecture123',
            'first_name': 'Giảng viên',
            'last_name': '',
            'is_staff': True,
            'is_superuser': False,
            'user_type': 'teacher'
        },
        {
            'email': 'admin@university.edu',
            'password': 'admin123',
            'first_name': 'Quản trị viên',
            'last_name': '',
            'is_staff': True,
            'is_superuser': True,
            'user_type': 'admin'
        }
    ]
    
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
            password=account['password'],
            first_name=account['first_name'],
            last_name=account['last_name'],
            is_staff=account['is_staff'],
            is_superuser=account['is_superuser']
        )
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

if __name__ == '__main__':
    create_default_accounts()