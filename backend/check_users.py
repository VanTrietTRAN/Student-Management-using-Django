import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')
django.setup()

from oauth.models import User

users = User.objects.all()
print("\nUsers in database:")
for user in users:
    print(f"Email: {user.email}")
    print(f"Is active: {user.is_active}")
    print(f"Is staff: {user.is_staff}")
    print(f"Is superuser: {user.is_superuser}")
    print(f"User type: {user.user_type}")
    print("-" * 50)