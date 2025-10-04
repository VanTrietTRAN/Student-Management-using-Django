from django.db import models
from .student import Student
from .subject import Subject

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Sinh viên")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Môn học")
    semester = models.CharField(max_length=10, verbose_name="Học kỳ")
    midterm_score = models.FloatField(default=0.0, verbose_name="Điểm giữa kỳ")
    final_score = models.FloatField(default=0.0, verbose_name="Điểm cuối kỳ")
    gpa = models.FloatField(default=0.0, verbose_name="Điểm TB")
    status = models.CharField(
        max_length=20,
        choices=[
            ('Hoàn thành', 'Hoàn thành'),
            ('Chưa hoàn thành', 'Chưa hoàn thành'),
            ('Thi lại', 'Thi lại'),
        ],
        default='Chưa hoàn thành',
        verbose_name="Trạng thái"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Điểm số"
        verbose_name_plural = "Điểm số"
        ordering = ['-created_at']
        unique_together = ['student', 'subject', 'semester']

    def __str__(self):
        return f"{self.student.full_name} - {self.subject.subject_name} - {self.semester}"

    def save(self, *args, **kwargs):
        # Auto-calculate GPA: 30% midterm + 70% final
        self.gpa = (self.midterm_score * 0.3) + (self.final_score * 0.7)
        super().save(*args, **kwargs)