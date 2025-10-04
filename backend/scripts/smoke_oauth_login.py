import os
import sys
import json
import requests

# Add backend dir to path so settings can be found if needed
script_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(script_dir)
sys.path.insert(0, backend_dir)

# Config
BASE_URL = os.environ.get('SMOKE_BASE_URL', 'http://127.0.0.1:8000')
TOKEN_URL = BASE_URL + '/o/token/'
PROTECTED_URL = BASE_URL + '/api/v1/students/'

# Use one of the default accounts
USERNAME = os.environ.get('SMOKE_USERNAME', 'student@university.edu')
PASSWORD = os.environ.get('SMOKE_PASSWORD', 'student123')
CLIENT_ID = os.environ.get('SMOKE_CLIENT_ID', '')
CLIENT_SECRET = os.environ.get('SMOKE_CLIENT_SECRET', '')

print('Token URL:', TOKEN_URL)
print('Attempting Resource Owner Password Credentials grant...')

payload = {
    'grant_type': 'password',
    'username': USERNAME,
    'password': PASSWORD,
}

# If client credentials are provided, use HTTP Basic auth
auth = None
if CLIENT_ID and CLIENT_SECRET:
    from requests.auth import HTTPBasicAuth
    auth = HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)

try:
    r = requests.post(TOKEN_URL, data=payload, auth=auth, timeout=10)
except Exception as e:
    print('Request error:', e)
    sys.exit(2)

print('Status code:', r.status_code)
try:
    data = r.json()
except Exception:
    print('Response text:', r.text)
    sys.exit(3)

print('Response JSON:', json.dumps(data, indent=2))
if 'access_token' not in data:
    print('No access_token in response; cannot call protected endpoint.')
    sys.exit(4)

headers = {'Authorization': f"Bearer {data['access_token']}"}
print('\nCalling protected endpoint:', PROTECTED_URL)
try:
    r2 = requests.get(PROTECTED_URL, headers=headers, timeout=10)
    print('Protected endpoint status:', r2.status_code)
    try:
        print('Protected response sample:', r2.json() if r2.text else '<empty>')
    except Exception:
        print('Protected response text:', r2.text)
except Exception as e:
    print('Protected request error:', e)
    sys.exit(5)

sys.exit(0)
