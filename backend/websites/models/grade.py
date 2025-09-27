from django.db import models
from .student import Student
from .subject import Subject

class Grade(models.Model):
    """Model cho điểm số"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Sinh viên")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Môn học")
    semester = models.PositiveIntegerField(verbose_name="Học kỳ")
    midterm_score = models.FloatField(verbose_name="Điểm giữa kỳ")
    final_score = models.FloatField(verbose_name="Điểm cuối kỳ")
    average_score = models.FloatField(verbose_name="Điểm trung bình")
    grade = models.CharField(max_length=5, verbose_name="Xếp loại")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    
    class Meta:
        db_table = 'grades'
        verbose_name = "Điểm số"
        verbose_name_plural = "Điểm số"
        unique_together = ['student', 'subject', 'semester']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student.full_name} - {self.subject.subject_name} - {self.average_score}"
    
    def save(self, *args, **kwargs):
        # Tự động tính điểm trung bình
        self.average_score = (self.midterm_score + self.final_score) / 2
        
        # Tự động xếp loại
        if self.average_score >= 9.5:
            self.grade = 'A+'
        elif self.average_score >= 8.5:
            self.grade = 'A'
        elif self.average_score >= 8.0:
            self.grade = 'B+'
        elif self.average_score >= 7.0:
            self.grade = 'B'
        elif self.average_score >= 6.5:
            self.grade = 'C+'
        elif self.average_score >= 5.5:
            self.grade = 'C'
        elif self.average_score >= 5.0:
            self.grade = 'D+'
        elif self.average_score >= 4.0:
            self.grade = 'D'
        else:
            self.grade = 'F'
        
        super().save(*args, **kwargs)
