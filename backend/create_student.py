import os
import django

# Thiết lập môi trường Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from oauth.models import User

def create_student():
    try:
        # Tạo tài khoản sinh viên
        student = User.objects.create_user(
            email='student@gmail.com',
            password='123456789',
            first_name='Sinh',
            last_name='Viên',
            user_type='student',
            is_active=True
        )
        
        print("Tạo tài khoản sinh viên thành công!")
        print("Email: student@gmail.com")
        print("Password: 123456789")
        
    except Exception as e:
        print(f"Lỗi khi tạo tài khoản: {str(e)}")

if __name__ == '__main__':
    create_student()