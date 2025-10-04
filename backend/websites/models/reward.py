from django.db import models
from .student import Student

class Reward(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Sinh viên")
    type = models.CharField(
        max_length=20,
        choices=[
            ('Khen thưởng', 'Khen thưởng'),
            ('Kỷ luật', 'Kỷ luật'),
        ],
        verbose_name="Loại"
    )
    description = models.TextField(verbose_name="Mô tả")
    date = models.DateField(verbose_name="Ngày")
    status = models.CharField(
        max_length=20,
        choices=[
            ('Đang xử lý', 'Đang xử lý'),
            ('Đã xử lý', 'Đã xử lý'),
        ],
        default='Đang xử lý',
        verbose_name="Trạng thái"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Khen thưởng & Kỷ luật"
        verbose_name_plural = "Khen thưởng & Kỷ luật"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.full_name} - {self.type} - {self.date}"