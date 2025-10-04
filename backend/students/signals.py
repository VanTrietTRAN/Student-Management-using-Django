from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models.profile import StudentProfile

User = get_user_model()


@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'student':
        StudentProfile.objects.get_or_create(
            user=instance,
            email=instance.email,
            student_id=f"ST{instance.id:06d}"  # Generate student ID based on user ID
        )