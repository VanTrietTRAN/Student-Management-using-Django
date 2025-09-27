from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Student(models.Model):
    """Model cho sinh viên"""
    student_id = models.CharField(max_length=20, unique=True, verbose_name="Mã sinh viên")
    full_name = models.CharField(max_length=100, verbose_name="Họ và tên")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="Số điện thoại")
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Ngày sinh")
    address = models.TextField(blank=True, null=True, verbose_name="Địa chỉ")
    class_name = models.CharField(max_length=20, verbose_name="Lớp")
    major = models.CharField(max_length=50, verbose_name="Ngành")
    year = models.CharField(max_length=10, verbose_name="Khóa")
    status = models.CharField(
        max_length=20,
        choices=[
            ('Đang học', 'Đang học'),
            ('Tốt nghiệp', 'Tốt nghiệp'),
            ('Tạm nghỉ', 'Tạm nghỉ'),
            ('Bị đuổi', 'Bị đuổi'),
        ],
        default='Đang học',
        verbose_name="Trạng thái"
    )
    gpa = models.FloatField(default=0.0, verbose_name="Điểm TB")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    
    class Meta:
        db_table = 'students'
        verbose_name = "Sinh viên"
        verbose_name_plural = "Sinh viên"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student_id} - {self.full_name}"
