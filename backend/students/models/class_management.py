from django.db import models
from .academic import Course
from oauth.models import User


class Class(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='classes')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teaching_classes')
    class_code = models.CharField(max_length=20, unique=True)
    room = models.CharField(max_length=50)
    
    # Schedule information
    day_of_week = models.CharField(max_length=20, choices=[
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ])
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    start_date = models.DateField()
    end_date = models.DateField()
    
    max_students = models.IntegerField()
    current_students = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Classes"

    def __str__(self):
        return f"{self.class_code} - {self.course.name}"


class CourseMaterial(models.Model):
    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='course_materials/')
    material_type = models.CharField(max_length=20, choices=[
        ('syllabus', 'Syllabus'),
        ('lecture', 'Lecture Notes'),
        ('assignment', 'Assignment'),
        ('reading', 'Reading Material'),
        ('other', 'Other'),
    ])
    
    upload_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Course Material"
        verbose_name_plural = "Course Materials"

    def __str__(self):
        return f"{self.class_instance.class_code} - {self.title}"