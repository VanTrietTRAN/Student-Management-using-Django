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

from django.contrib.auth.models import User
from django.core.management import call_command

def create_default_accounts():
    """Create default user accounts based on config.env settings"""
    
    # Default accounts from config.env
    accounts = [
        {
            'username': 'student@university.edu',
            'email': 'student@university.edu',
            'password': 'student123',
            'first_name': 'Sinh viên',
            'last_name': 'Mẫu',
            'is_staff': False,
            'is_superuser': False
        },
        {
            'username': 'teacher@university.edu',
            'email': 'teacher@university.edu',
            'password': 'teacher123',
            'first_name': 'Giảng viên',
            'last_name': 'Mẫu',
            'is_staff': True,
            'is_superuser': False
        },
        {
            'username': 'training@university.edu',
            'email': 'training@university.edu',
            'password': 'training123',
            'first_name': 'Nhân viên',
            'last_name': 'Phòng đào tạo',
            'is_staff': True,
            'is_superuser': False
        },
        {
            'username': 'affairs@university.edu',
            'email': 'affairs@university.edu',
            'password': 'affairs123',
            'first_name': 'Nhân viên',
            'last_name': 'Phòng công tác sinh viên',
            'is_staff': True,
            'is_superuser': False
        },
        {
            'username': 'admin@university.edu',
            'email': 'admin@university.edu',
            'password': 'admin123',
            'first_name': 'Quản trị viên',
            'last_name': 'Hệ thống',
            'is_staff': True,
            'is_superuser': True
        }
    ]
    
    print("Creating default user accounts...")
    
    for account in accounts:
        username = account['username']
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            print(f"User {username} already exists, skipping...")
            continue
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=account['email'],
            password=account['password'],
            first_name=account['first_name'],
            last_name=account['last_name'],
            is_staff=account['is_staff'],
            is_superuser=account['is_superuser']
        )
        
        print(f"Created user: {username} ({account['first_name']} {account['last_name']})")
    
    print("\nDefault accounts created successfully!")
    print("\nLogin credentials:")
    print("Student: student@university.edu / student123")
    print("Teacher: teacher@university.edu / teacher123")
    print("Training Staff: training@university.edu / training123")
    print("Student Affairs: affairs@university.edu / affairs123")
    print("Admin: admin@university.edu / admin123")

if __name__ == '__main__':
    create_default_accounts()