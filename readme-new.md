# Hướng dẫn chạy dự án trên Windows (PowerShell)

Tệp này mô tả chi tiết cách thiết lập và chạy dự án "Student Management System" trên Windows sử dụng PowerShell.

## Tóm tắt
- Django version: 5.2.6 (theo `requirements.txt`).
- CSDL mặc định: SQLite (file `db.sqlite3` ở root) — không cần cài thêm DB để chạy local.
- Email: cấu hình SMTP Gmail, cần đặt biến môi trường `EMAIL_ADDRESS` và `EMAIL_PASSWORD` nếu muốn gửi email.
- ALLOWED_HOSTS trong `student_management_system/settings.py` đang là `['*']` (phù hợp cho dev nhưng không an toàn ở production).

---

## 1. Mở PowerShell và chuyển vào thư mục dự án

```powershell
cd 'D:\PERSONAL\The-Fifth-2025-2026\ERP\student-management-using-django-main\student-management-using-django-main'
```

## 2. Tạo và kích hoạt virtual environment (khuyến nghị)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Nếu PowerShell chặn script activation, chạy (với quyền admin nếu cần):

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.venv\Scripts\Activate.ps1
```

## 3. Cập nhật pip và cài dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Lưu ý: `requirements.txt` đã được cập nhật lên các phiên bản mới hơn. Nếu bạn gặp lỗi với một số package trên Windows (ví dụ `psycopg2`/các gói cần build), bạn có thể cài thủ công các gói chính. Ví dụ cài thủ công (phiên bản tương ứng):

```powershell
pip install Django==5.2.6 Pillow==11.3.0 requests==2.32.5 whitenoise==6.11.0 mysql-connector==2.2.9 dj-database-url==3.0.1 virtualenv==20.34.0 gunicorn==23.0.0
```

Phiên bản đầy đủ hiện có trong `requirements.txt`.

## 4. Cấu hình biến môi trường (tuỳ chọn)

- `EMAIL_ADDRESS` và `EMAIL_PASSWORD`: cần nếu bạn muốn gửi email qua Gmail.
- `asdfasvnvaksdnvlakwnv`: biến để `SECRET_KEY` trong `settings.py` (có thể đặt một chuỗi bí mật dev).

Đặt biến cho session hiện tại (PowerShell):

```powershell
$env:asdfasvnvaksdnvlakwnv = "dev_secret_key_123"
$env:EMAIL_ADDRESS = "youremail@gmail.com"
$env:EMAIL_PASSWORD = "your_app_password"
```

> Gợi ý: đối với Gmail, dùng App Password (Google Account -> Security -> App Passwords).

## 5. (Tùy chọn) Chỉnh `ALLOWED_HOSTS` cho an toàn

Mở `student_management_system/settings.py` và chỉnh:

```python
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
```

## 6. Áp dụng migrations và tạo superuser

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

Nếu bạn không muốn tạo superuser, README gốc liệt kê một số credentials mẫu (chỉ khi DB đã chứa các user đó):
- HOD / SuperAdmin: `admin@admin.com` / `admin`
- Staff: `staff@staff.com` / `staff`
- Student: `student@student.com` / `student`

## 7. Collect static files (tùy dùng)

```powershell
python manage.py collectstatic --noinput
```

Static sẽ được thu vào thư mục `static` theo cấu hình `STATIC_ROOT`.

## 8. Chạy server local

```powershell
python manage.py runserver 0.0.0.0:8000
```

Mở trình duyệt: `http://127.0.0.1:8000/`.

## 9. Các lỗi thường gặp và cách khắc phục

- "Couldn't import Django": chưa active venv hoặc chưa cài Django. Active venv và `pip install -r requirements.txt`.
- Lỗi cài `psycopg2` trên Windows: cài `psycopg2-binary` hoặc bỏ qua nếu không dùng Postgres.
- Email không gửi: dùng App Password, hoặc tạm đổi `EMAIL_BACKEND` thành console/file backend cho dev. Ví dụ trong `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# hoặc
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_mails")
```

- Lỗi liên quan collectstatic/permission: đảm bảo bạn chạy PowerShell từ thư mục project và có quyền ghi.

## 10. Ghi chú Production

- Tắt `DEBUG` và đặt `SECRET_KEY` qua biến môi trường.
- Thiết lập `ALLOWED_HOSTS` thích hợp.
- Dùng Postgres/MySQL và cấu hình `DATABASES` (sửa `settings.py` hoặc sử dụng biến môi trường + `dj_database_url`).
- Dùng Gunicorn + nginx/hosting hoặc dịch vụ Heroku, và cấu hình static/media thích hợp.

---