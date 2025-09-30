from django.db import models
from .student import Student
from .subject import Subject

class Registration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="registrations", verbose_name="Sinh viên")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="registrations", verbose_name="Môn học")
    semester = models.CharField(max_length=10, verbose_name="Học kỳ")
    registered_credits = models.IntegerField(verbose_name="Số tín chỉ đăng ký")
    tuition_per_credit = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Học phí/tín chỉ")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Đăng ký học phần"
        verbose_name_plural = "Đăng ký học phần"
        unique_together = ["student", "subject", "semester"]

    @property
    def total_tuition(self):
        return self.registered_credits * self.tuition_per_credit

    def __str__(self):
        return f"{self.student.full_name} - {self.subject.subject_name} - {self.semester}"
