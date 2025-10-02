import json
import requests

BASE = 'http://127.0.0.1:8008'
ACCOUNTS = [
    ('student@university.edu', 'student123'),
    ('lecture@university.edu', 'lecture123'),
    ('admin@university.edu', 'admin123'),
]

def run():
    for username, password in ACCOUNTS:
        print('\n== HTTP test for', username)
        login_url = f'{BASE}/api/v1/employees/login'
        data = {'username': username, 'password': password}
        try:
            r = requests.post(login_url, data=data, timeout=5)
        except Exception as e:
            print('HTTP request failed:', e)
            continue
        print('login http status:', r.status_code)
        try:
            body = r.json()
            print(json.dumps(body, indent=2))
        except Exception:
            print('non-json login response:', r.text[:400])
            continue

        token = body.get('access_token')
        if not token:
            print('no token returned')
            continue

        headers = {'Authorization': f'Bearer {token}'}
        info_url = f'{BASE}/api/v1/employees/userinfo'
        try:
            ir = requests.get(info_url, headers=headers, timeout=5)
        except Exception as e:
            print('userinfo request failed:', e)
            continue
        print('userinfo http status:', ir.status_code)
        try:
            print(json.dumps(ir.json(), indent=2))
        except Exception:
            print('non-json userinfo response:', ir.text[:400])

if __name__ == '__main__':
    run()
