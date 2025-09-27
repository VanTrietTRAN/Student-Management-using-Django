from django.db import models

class Subject(models.Model):
    """Model cho môn học"""
    subject_code = models.CharField(max_length=20, unique=True, verbose_name="Mã môn học")
    subject_name = models.CharField(max_length=100, verbose_name="Tên môn học")
    credits = models.PositiveIntegerField(verbose_name="Số tín chỉ")
    major = models.CharField(max_length=50, verbose_name="Ngành")
    type = models.CharField(
        max_length=20,
        choices=[
            ('Bắt buộc', 'Bắt buộc'),
            ('Tự chọn', 'Tự chọn'),
            ('Thực tập', 'Thực tập'),
        ],
        verbose_name="Loại môn học"
    )
    semester = models.PositiveIntegerField(verbose_name="Học kỳ")
    teacher_name = models.CharField(max_length=100, verbose_name="Giảng viên")
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả")
    status = models.CharField(
        max_length=20,
        choices=[
            ('Đang mở', 'Đang mở'),
            ('Đã đóng', 'Đã đóng'),
            ('Tạm dừng', 'Tạm dừng'),
        ],
        default='Đang mở',
        verbose_name="Trạng thái"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    
    class Meta:
        db_table = 'subjects'
        verbose_name = "Môn học"
        verbose_name_plural = "Môn học"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.subject_code} - {self.subject_name}"
