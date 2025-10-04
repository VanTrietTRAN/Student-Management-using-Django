from django.db import models
from .profile import StudentProfile
from .academic import Semester, Course


class TuitionFee(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='tuition_fees')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='tuition_fees')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='tuition_fees')
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('partial', 'Partially Paid'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
    ])
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Tuition Fee"
        verbose_name_plural = "Tuition Fees"

    def __str__(self):
        return f"{self.student.student_id} - {self.semester} - {self.course.code}"


class Payment(models.Model):
    tuition_fee = models.ForeignKey(TuitionFee, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=[
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('credit_card', 'Credit Card'),
        ('other', 'Other'),
    ])
    transaction_id = models.CharField(max_length=100, unique=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    def __str__(self):
        return f"{self.tuition_fee.student.student_id} - {self.amount}"


class Invoice(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name='invoice')
    invoice_number = models.CharField(max_length=50, unique=True)
    generated_date = models.DateTimeField(auto_now_add=True)
    pdf_file = models.FileField(upload_to='invoices/', null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"

    def __str__(self):
        return self.invoice_number