import os, sys
# Ensure the 'backend' package directory is on sys.path so top-level packages like
# `core` (which lives under backend/core) can be imported when running this script
script_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(script_dir)
sys.path.insert(0, backend_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')
import django
django.setup()
from oauth.models import User
emails = ['student@university.edu','lecture@university.edu','admin@university.edu']
for e in emails:
    qs = User.objects.filter(email=e)
    if not qs.exists():
        print(e, '-> NOT FOUND')
        continue
    u = qs.first()
    print(e, '-> found | is_superuser=', u.is_superuser, '| active=', u.active, '| check_pass_student123=', u.check_password('student123'), '| check_pass_lecture123=', u.check_password('lecture123'), '| check_pass_admin123=', u.check_password('admin123'))
