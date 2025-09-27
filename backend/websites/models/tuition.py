from django.db import models
from .student import Student

class Tuition(models.Model):
    """Model cho học phí"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Sinh viên")
    semester = models.PositiveIntegerField(verbose_name="Học kỳ")
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Số tiền")
    due_date = models.DateField(verbose_name="Hạn nộp")
    payment_date = models.DateField(blank=True, null=True, verbose_name="Ngày nộp")
    status = models.CharField(
        max_length=20,
        choices=[
            ('Đã đóng', 'Đã đóng'),
            ('Chưa đóng', 'Chưa đóng'),
            ('Quá hạn', 'Quá hạn'),
        ],
        default='Chưa đóng',
        verbose_name="Trạng thái"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    
    class Meta:
        db_table = 'tuitions'
        verbose_name = "Học phí"
        verbose_name_plural = "Học phí"
        unique_together = ['student', 'semester']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student.full_name} - Học kỳ {self.semester} - {self.amount} VNĐ"
