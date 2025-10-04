import json
import os
import django

from django.test import Client

# Use the project's base settings
# Make sure the backend package is discoverable on sys.path
import sys
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')
django.setup()

client = Client()

def run():
    accounts = [
        ('student@university.edu', 'student123'),
        ('lecture@university.edu', 'lecture123'),
        ('admin@university.edu', 'admin123'),
    ]

    for username, password in accounts:
        print('\n== Testing login for', username)
        login_url = '/api/v1/employees/login'
        data = {'username': username, 'password': password}
        # include HTTP_HOST to match ALLOWED_HOSTS and avoid DisallowedHost
        resp = client.post(login_url, data, HTTP_HOST='localhost')
        print('login status:', resp.status_code)
        try:
            body = resp.json()
            print(json.dumps(body, indent=2))
        except Exception:
            print('login response content:', resp.content)
            continue

        access_token = body.get('access_token')
        redirect_to = body.get('redirect_to')
        print('redirect_to:', redirect_to)

        if not access_token:
            print('No access token returned; skipping userinfo and token checks')
            continue

        # verify AccessToken exists in DB
        from oauth2_provider.models import get_access_token_model
        AccessToken = get_access_token_model()
        try:
            token_qs = AccessToken.objects.filter(token=access_token).order_by('-id')
            token_obj = token_qs.first() if token_qs.exists() else None
            if token_obj is not None:
                print('AccessToken found in DB: user=', getattr(token_obj.user, 'email', token_obj.user), 'application=', getattr(token_obj.application, 'name', token_obj.application))
            else:
                print('AccessToken not found in DB: no matching token')
        except Exception as e:
            print('AccessToken lookup error:', str(e))

        # call protected userinfo endpoint using DRF APIClient which handles Authorization header correctly
        from rest_framework.test import APIClient
        info_url = '/api/v1/employees/userinfo'
        api_client = APIClient()
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        info_resp = api_client.get(info_url, HTTP_HOST='localhost')
        print('userinfo status:', info_resp.status_code)
        try:
            print('userinfo body:', json.dumps(info_resp.json(), indent=2))
        except Exception:
            print('userinfo content:', info_resp.content)

if __name__ == '__main__':
    run()
