import os
import sys
import requests

# Setup DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')

import django
django.setup()

from oauth2_provider.models import AccessToken

BASE = 'http://127.0.0.1:8008'
username = 'student@university.edu'
password = 'student123'

r = requests.post(f'{BASE}/api/v1/employees/login', data={'username': username, 'password': password}, timeout=5)
print('login status', r.status_code)
print(r.text[:400])
try:
    token = r.json().get('access_token')
except Exception:
    token = None

if not token:
    print('no token')
    sys.exit(1)

# Check DB for AccessToken
try:
    tok = AccessToken.objects.filter(token=token).first()
    if tok:
        print('Found AccessToken in DB: id=', tok.id, 'user=', tok.user.email, 'scope=', tok.scope)
    else:
        print('No AccessToken row matches token. Most recent tokens:')
        for t in AccessToken.objects.order_by('-id')[:5]:
            print('  ', t.id, t.token[:80], 'user=', getattr(t.user, 'email', None))
except Exception as e:
    print('DB query error:', e)
