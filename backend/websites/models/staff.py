from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Staff(models.Model):
    """Model cho nhân viên"""
    staff_id = models.CharField(max_length=20, unique=True, verbose_name="Mã nhân viên")
    full_name = models.CharField(max_length=100, verbose_name="Họ và tên")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="Số điện thoại")
    department = models.CharField(max_length=100, verbose_name="Phòng ban")
    position = models.CharField(max_length=50, verbose_name="Chức vụ")
    role = models.CharField(
        max_length=30,
        choices=[
            ('Phòng đào tạo', 'Phòng đào tạo'),
            ('Phòng công tác sinh viên', 'Phòng công tác sinh viên'),
            ('Phòng hành chính', 'Phòng hành chính'),
            ('Phòng tài chính', 'Phòng tài chính'),
        ],
        verbose_name="Vai trò"
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('Đang làm việc', 'Đang làm việc'),
            ('Nghỉ việc', 'Nghỉ việc'),
        ],
        default='Đang làm việc',
        verbose_name="Trạng thái"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    
    class Meta:
        db_table = 'staff'
        verbose_name = "Nhân viên"
        verbose_name_plural = "Nhân viên"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.staff_id} - {self.full_name}"
