from django.db import models
from .student import Student
from .subject import Subject
from .classroom import Classroom
from django.utils import timezone

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances', verbose_name="Sinh viên")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='attendances', verbose_name="Môn học")
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='attendances', verbose_name="Lớp học")
    date = models.DateField(default=timezone.now, verbose_name="Ngày điểm danh")
    status = models.CharField(
        max_length=20,
        choices=[
            ('present', 'Có mặt'),
            ('absent', 'Vắng mặt'),
            ('late', 'Đi muộn'),
            ('excused', 'Có phép'),
        ],
        default='present',
        verbose_name="Trạng thái"
    )
    notes = models.TextField(blank=True, null=True, verbose_name="Ghi chú")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Điểm danh"
        verbose_name_plural = "Điểm danh"
        ordering = ['-date', '-created_at']
        unique_together = ['student', 'subject', 'date']
        
    def __str__(self):
        return f"{self.student.full_name} - {self.subject.subject_name} - {self.date}"