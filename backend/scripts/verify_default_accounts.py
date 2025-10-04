#!/usr/bin/env python
"""Verify default user accounts exist and their passwords are valid."""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')
django.setup()

from oauth.models import User

def check_account(email, password):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        print(f"MISSING: {email}")
        return False
    ok = user.check_password(password)
    print(f"{email}: exists=True, password_match={ok}, is_active={user.is_active}, is_staff={user.is_staff}, is_superuser={user.is_superuser}")
    return ok

def main():
    accounts = [
        ('student@university.edu', 'student123'),
        ('lecture@university.edu', 'lecture123'),
        ('admin@university.edu', 'admin123'),
    ]
    results = {email: check_account(email, pwd) for email, pwd in accounts}
    print('\nSummary:')
    for email, ok in results.items():
        print(f"{email}: {'OK' if ok else 'FAILED'}")

if __name__ == '__main__':
    main()
