from django.db import models

class Staff(models.Model):
    staff_id = models.CharField(max_length=20, unique=True, verbose_name="Mã nhân viên")
    full_name = models.CharField(max_length=100, verbose_name="Họ và tên")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=15, verbose_name="Số điện thoại")
    department = models.CharField(
        max_length=50,
        choices=[
            ('Phòng đào tạo', 'Phòng đào tạo'),
            ('Phòng công tác sinh viên', 'Phòng công tác sinh viên'),
        ],
        verbose_name="Phòng ban"
    )
    role = models.CharField(
        max_length=50,
        choices=[
            ('Training Staff', 'Nhân viên phòng đào tạo'),
            ('Student Affairs Staff', 'Nhân viên phòng công tác sinh viên'),
        ],
        verbose_name="Vai trò"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Nhân viên"
        verbose_name_plural = "Nhân viên"
        ordering = ['staff_id']

    def __str__(self):
        return f"{self.staff_id} - {self.full_name}"