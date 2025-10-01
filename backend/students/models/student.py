from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

class Student(models.Model):
    student_id = models.CharField(
        max_length=8, 
        unique=True,
        validators=[RegexValidator(regex=r'^\d{8}$', message='Student ID must be 8 digits')]
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)
    major = models.CharField(max_length=100)
    enrollment_date = models.DateField()
    graduation_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

class Course(models.Model):
    code = models.CharField(
        max_length=10,
        unique=True,
        validators=[RegexValidator(regex=r'^[A-Z]{2}\d{3}$', message='Course code must be in format XX999')]
    )
    name = models.CharField(max_length=200)
    credits = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)])
    description = models.TextField()
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True)
    capacity = models.IntegerField(validators=[MinValueValidator(1)])

class CourseRegistration(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled')
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.CharField(max_length=20)
    registration_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        unique_together = ('student', 'course', 'semester')

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade_value = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)]
    )
    semester = models.CharField(max_length=20)
    submission_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course', 'semester')

class TuitionPayment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('cash', 'Cash')
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded')
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, unique=True, null=True)
    notes = models.TextField(blank=True)