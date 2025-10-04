import os
import sys
from pathlib import Path

# Ensure backend package is on sys.path so `core` settings module can be imported
BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')
import django
django.setup()

from oauth.models.oauth2 import AccessToken

for t in AccessToken.objects.order_by('-id')[:10]:
    print(t.id, getattr(t.user, 'email', None), (t.token[:120] + ('...' if len(t.token)>120 else '')))
