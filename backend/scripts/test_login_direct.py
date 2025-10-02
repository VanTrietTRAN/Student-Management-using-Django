import os
import sys
import django
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')
django.setup()

from django.test import Client
from rest_framework.test import APIRequestFactory, force_authenticate
from oauth2_provider.models import get_access_token_model
from businesses.views.employee import EmployeeViewSet

client = Client()

ACCOUNTS = [
    ('student@university.edu', 'student123'),
    ('lecture@university.edu', 'lecture123'),
    ('admin@university.edu', 'admin123'),
]

def run():
    AccessToken = get_access_token_model()
    factory = APIRequestFactory()

    for username, password in ACCOUNTS:
        print('\n== Direct test for', username)
        # login
        resp = client.post('/api/v1/employees/login', {'username': username, 'password': password}, HTTP_HOST='localhost')
        print('login status', resp.status_code)
        try:
            body = resp.json()
        except Exception:
            print('login failed, content:', resp.content)
            continue

        access_token = body.get('access_token')
        redirect_to = body.get('redirect_to')
        print('redirect_to', redirect_to)

        if not access_token:
            print('no token returned')
            continue

        token_qs = AccessToken.objects.filter(token=access_token).order_by('-id')
        token_obj = token_qs.first() if token_qs.exists() else None
        if not token_obj:
            print('token not found in DB')
            continue

        user = token_obj.user
        print('token->user', getattr(user, 'email', user))

        # build authenticated request to userinfo and attach the AccessToken as request.auth
        request = factory.get('/api/v1/employees/userinfo')
        force_authenticate(request, user=user, token=token_obj)
        view = EmployeeViewSet.as_view({'get':'userinfo'})
        response = view(request)
        print('userinfo direct status:', response.status_code)
        try:
            print('userinfo direct body:', json.dumps(response.data, indent=2))
        except Exception:
            print('userinfo direct content:', getattr(response, 'content', str(response)))

if __name__ == '__main__':
    run()
