from django.db import models
from .student import Student

class Tuition(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Sinh viên")
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Số tiền")
    semester = models.CharField(max_length=10, verbose_name="Học kỳ")
    due_date = models.DateField(verbose_name="Hạn đóng")
    payment_date = models.DateField(null=True, blank=True, verbose_name="Ngày đóng")
    status = models.CharField(
        max_length=20,
        choices=[
            ('Chưa đóng', 'Chưa đóng'),
            ('Đã đóng', 'Đã đóng'),
            ('Quá hạn', 'Quá hạn'),
        ],
        default='Chưa đóng',
        verbose_name="Trạng thái"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Học phí"
        verbose_name_plural = "Học phí"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.full_name} - {self.semester} - {self.amount}"