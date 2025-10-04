from django.db import models
from .profile import StudentProfile
from .class_management import Class


class CourseRegistration(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='registrations')
    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='registrations')
    
    registration_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ])
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'class_instance')
        verbose_name = "Course Registration"
        verbose_name_plural = "Course Registrations"

    def __str__(self):
        return f"{self.student.student_id} - {self.class_instance.class_code}"


class Schedule(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='schedules')
    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='schedules')
    
    # Exam schedule
    exam_date = models.DateField(null=True, blank=True)
    exam_start_time = models.TimeField(null=True, blank=True)
    exam_end_time = models.TimeField(null=True, blank=True)
    exam_room = models.CharField(max_length=50, null=True, blank=True)
    
    notification_sent = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Schedule"
        verbose_name_plural = "Schedules"

    def __str__(self):
        return f"{self.student.student_id} - {self.class_instance.class_code}"