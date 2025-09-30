from django.db import models
from oauth.models import User

class Teacher(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='teacher_profile',
        verbose_name="Tài khoản người dùng"
    )
    teacher_id = models.CharField(max_length=20, unique=True, verbose_name="Mã giảng viên")
    full_name = models.CharField(max_length=100, verbose_name="Họ và tên")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=15, verbose_name="Số điện thoại")
    department = models.CharField(
        max_length=50,
        choices=[
            ('CNTT', 'Khoa CNTT'),
            ('KTPM', 'Khoa KTPM'),
            ('ATTT', 'Khoa ATTT'),
        ],
        verbose_name="Khoa"
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('Đang làm việc', 'Đang làm việc'),
            ('Nghỉ hưu', 'Nghỉ hưu'),
            ('Tạm nghỉ', 'Tạm nghỉ'),
        ],
        default='Đang làm việc',
        verbose_name="Trạng thái"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Giảng viên"
        verbose_name_plural = "Giảng viên"
        ordering = ['teacher_id']

    def __str__(self):
        return f"{self.teacher_id} - {self.full_name}"