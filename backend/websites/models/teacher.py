from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Teacher(models.Model):
    """Model cho giảng viên"""
    teacher_id = models.CharField(max_length=20, unique=True, verbose_name="Mã giảng viên")
    full_name = models.CharField(max_length=100, verbose_name="Họ và tên")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="Số điện thoại")
    department = models.CharField(max_length=100, verbose_name="Khoa/Bộ môn")
    position = models.CharField(max_length=50, verbose_name="Chức vụ")
    degree = models.CharField(max_length=50, blank=True, null=True, verbose_name="Học vị")
    status = models.CharField(
        max_length=20,
        choices=[
            ('Đang làm việc', 'Đang làm việc'),
            ('Nghỉ hưu', 'Nghỉ hưu'),
            ('Nghỉ việc', 'Nghỉ việc'),
        ],
        default='Đang làm việc',
        verbose_name="Trạng thái"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    
    class Meta:
        db_table = 'teachers'
        verbose_name = "Giảng viên"
        verbose_name_plural = "Giảng viên"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.teacher_id} - {self.full_name}"
