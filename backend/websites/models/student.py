from django.db import models
from oauth.models import User

class Student(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile',
        verbose_name="Tài khoản người dùng"
    )
    student_id = models.CharField(max_length=20, unique=True, verbose_name="Mã sinh viên")
    full_name = models.CharField(max_length=100, verbose_name="Họ và tên")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=15, verbose_name="Số điện thoại")
    classroom = models.CharField(max_length=20, verbose_name="Lớp")
    major = models.CharField(max_length=50, verbose_name="Ngành")
    profile_picture = models.ImageField(
        upload_to='students/profile_pictures/',
        null=True,
        blank=True,
        verbose_name="Ảnh đại diện"
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('Đang học', 'Đang học'),
            ('Tốt nghiệp', 'Tốt nghiệp'),
            ('Tạm nghỉ', 'Tạm nghỉ'),
        ],
        default='Đang học',
        verbose_name="Trạng thái"
    )
    gpa = models.FloatField(default=0.0, verbose_name="Điểm TB")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sinh viên"
        verbose_name_plural = "Sinh viên"
        ordering = ['student_id']

    def __str__(self):
        return f"{self.student_id} - {self.full_name}"