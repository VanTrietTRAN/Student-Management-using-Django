from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from main_app.models import CustomUser
import os

class Command(BaseCommand):
    help = 'Create sample users: admin, staff, student'

    def handle(self, *args, **options):
        created = []
        # ensure media placeholder exists
        placeholder_path = os.path.join(settings.BASE_DIR, 'media', 'profile_placeholder.png')
        if not os.path.exists(placeholder_path):
            self.stdout.write(self.style.WARNING('Placeholder image not found at %s' % placeholder_path))

        def make_user(email, password, first_name, last_name, user_type, gender='M'):
            try:
                user = CustomUser.objects.filter(email=email).first()
                if user:
                    self.stdout.write(self.style.NOTICE(f'User already exists: {email}'))
                    return False
                user = CustomUser(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    user_type=str(user_type),
                    gender=gender,
                    address='Auto-created user',
                )
                # set unusable username field behavior handled by model
                user.set_password(password)
                # attach placeholder image file if available
                if os.path.exists(placeholder_path):
                    with open(placeholder_path, 'rb') as f:
                        django_file = File(f)
                        user.profile_pic.save(os.path.basename(placeholder_path), django_file, save=False)
                user.save()
                created.append(email)
                self.stdout.write(self.style.SUCCESS(f'Created user: {email}'))
                return True
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to create {email}: {e}'))
                return False

        make_user('admin@admin.com', 'admin', 'Admin', 'User', 1)
        make_user('staff@staff.com', 'staff', 'Staff', 'User', 2)
        make_user('student@student.com', 'student', 'Student', 'User', 3)

        self.stdout.write(self.style.SUCCESS('Done.'))
