from django.core.management.base import BaseCommand
from django.db import transaction

from main_app.models import CustomUser, Student, Course, Session


class Command(BaseCommand):
    help = 'Ensure all student users have Student profiles and assign them to courses round-robin'

    def handle(self, *args, **options):
        students = CustomUser.objects.filter(user_type=3)
        courses = list(Course.objects.all())
        session = Session.objects.first()
        if not courses:
            self.stdout.write(self.style.WARNING('No courses found. Create courses first.'))
            return
        created_profiles = 0
        assigned = 0
        with transaction.atomic():
            for i, u in enumerate(students):
                # ensure Student profile exists
                if not hasattr(u, 'student'):
                    Student.objects.create(admin=u, course=courses[i % len(courses)], session=session)
                    created_profiles += 1
                    assigned += 1
                    self.stdout.write(self.style.SUCCESS(f'Created Student profile for {u.email} and assigned to {courses[i % len(courses)].name}'))
                else:
                    s = u.student
                    if not s.course:
                        s.course = courses[i % len(courses)]
                        assigned += 1
                        s.session = session
                        s.save()
                        self.stdout.write(self.style.SUCCESS(f'Assigned existing Student {u.email} to {s.course.name}'))

        self.stdout.write(self.style.NOTICE(f'Done. Profiles created: {created_profiles}. Assignments made: {assigned}.'))
