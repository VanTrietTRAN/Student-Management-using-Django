from django.db import models
from .student import Student

class Reward(models.Model):
    """Model cho khen thưởng và kỷ luật"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Sinh viên")
    type = models.CharField(
        max_length=20,
        choices=[
            ('Khen thưởng', 'Khen thưởng'),
            ('Kỷ luật', 'Kỷ luật'),
        ],
        verbose_name="Loại"
    )
    title = models.CharField(max_length=200, verbose_name="Tiêu đề")
    description = models.TextField(verbose_name="Mô tả")
    level = models.CharField(
        max_length=20,
        choices=[
            ('Cấp trường', 'Cấp trường'),
            ('Cấp khoa', 'Cấp khoa'),
            ('Cấp lớp', 'Cấp lớp'),
        ],
        verbose_name="Mức độ"
    )
    date = models.DateField(verbose_name="Ngày")
    status = models.CharField(
        max_length=20,
        choices=[
            ('Đã duyệt', 'Đã duyệt'),
            ('Chờ duyệt', 'Chờ duyệt'),
            ('Từ chối', 'Từ chối'),
        ],
        default='Chờ duyệt',
        verbose_name="Trạng thái"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    
    class Meta:
        db_table = 'rewards'
        verbose_name = "Khen thưởng & Kỷ luật"
        verbose_name_plural = "Khen thưởng & Kỷ luật"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student.full_name} - {self.title}"
