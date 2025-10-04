from django.db import models
from .profile import StudentProfile


class Semester(models.Model):
    name = models.CharField(max_length=50)
    year = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.year}"


class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    credits = models.IntegerField()
    description = models.TextField()
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='courses')
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False)
    
    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self):
        return f"{self.code} - {self.name}"


class Grade(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='grades')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='grades')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='grades')
    
    # Different types of grades
    attendance_grade = models.FloatField(default=0)
    midterm_grade = models.FloatField(default=0)
    final_grade = models.FloatField(default=0)
    total_grade = models.FloatField(default=0)
    
    status = models.CharField(max_length=20, choices=[
        ('passed', 'Passed'),
        ('failed', 'Failed'),
        ('incomplete', 'Incomplete'),
    ])
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'course', 'semester')
        verbose_name = "Grade"
        verbose_name_plural = "Grades"

    def __str__(self):
        return f"{self.student.student_id} - {self.course.code} - {self.total_grade}"


class AcademicHistory(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='academic_history')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    gpa = models.FloatField()
    credits_earned = models.IntegerField()
    credits_attempted = models.IntegerField()
    academic_status = models.CharField(max_length=20, choices=[
        ('good', 'Good Standing'),
        ('warning', 'Academic Warning'),
        ('probation', 'Academic Probation'),
    ])
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'semester')
        verbose_name = "Academic History"
        verbose_name_plural = "Academic Histories"

    def __str__(self):
        return f"{self.student.student_id} - {self.semester} - GPA: {self.gpa}"