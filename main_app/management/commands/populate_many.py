from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from main_app.models import CustomUser, Course, Session, Subject
import os
import datetime

class Command(BaseCommand):
    help = 'Populate DB: 6 courses, 2 staff, 30 students; assign staff to 3 courses each and distribute students.'

    def handle(self, *args, **options):
        # create 6 courses
        courses = []
        for i in range(1,7):
            c, created = Course.objects.get_or_create(name=f'Course {i}')
            courses.append(c)
            self.stdout.write(self.style.SUCCESS(f'Course {c.name} - {"created" if created else "exists"}'))

        # create session
        s, created = Session.objects.get_or_create(start_year=datetime.date(2023,1,1), end_year=datetime.date(2023,12,31))
        self.stdout.write(self.style.SUCCESS(f'Session {s} - {"created" if created else "exists"}'))

        # placeholder image
        placeholder = os.path.join(settings.BASE_DIR, 'media', 'profile_placeholder.png')

        # ensure staff users
        staff_emails = ['staff@staff.com', 'staff2@staff.com']
        staff_users = []
        for e in staff_emails:
            u = CustomUser.objects.filter(email=e).first()
            if not u:
                u = CustomUser(email=e, first_name='Staff', last_name=e.split('@')[0], user_type='2', gender='M', address='Auto')
                u.set_password('staff')
                u.save()
                if os.path.exists(placeholder):
                    with open(placeholder,'rb') as f:
                        u.profile_pic.save(os.path.basename(placeholder), File(f), save=True)
                self.stdout.write(self.style.SUCCESS(f'Created staff {e}'))
            else:
                self.stdout.write(self.style.NOTICE(f'Staff exists {e}'))
            staff_users.append(u)

        # assign each staff 3 courses and create Subject entries
        for idx, u in enumerate(staff_users):
            # ensure Staff profile exists
            st_profile = getattr(u, 'staff', None)
            if not st_profile:
                from main_app.models import Staff as StaffModel
                st_profile = StaffModel.objects.create(admin=u)
                self.stdout.write(self.style.SUCCESS(f'Created Staff profile for {u.email}'))

            assigned = courses[idx*3:(idx+1)*3]
            for c in assigned:
                subj_name = f'Subject {c.name} - {u.email}'
                subj, created = Subject.objects.get_or_create(name=subj_name, staff=st_profile, course=c)
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created subject {subj_name}'))
            if st_profile:
                st_profile.course = assigned[0]
                st_profile.save()
                self.stdout.write(self.style.SUCCESS(f'Assigned {assigned[0].name} to {u.email}'))

        # create students until total 30
        existing_students = CustomUser.objects.filter(user_type='3').count()
        needed = max(0, 30 - existing_students)
        self.stdout.write(self.style.SUCCESS(f'Existing students: {existing_students}, need to create: {needed}'))
        created_count = 0
        num = 1
        while created_count < needed:
            email = f'student{num}@student.com'
            if not CustomUser.objects.filter(email=email).exists():
                u = CustomUser(email=email, first_name=f'Student{num}', last_name='User', user_type='3', gender='M', address='Auto')
                u.set_password('student')
                u.save()
                if os.path.exists(placeholder):
                    with open(placeholder,'rb') as f:
                        u.profile_pic.save(os.path.basename(placeholder), File(f), save=True)
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created {email}'))
            num += 1

        # assign students to courses round-robin
        all_students = list(CustomUser.objects.filter(user_type='3').order_by('id'))
        for i, u in enumerate(all_students):
            st_profile = getattr(u, 'student', None)
            if st_profile:
                course = courses[i % len(courses)]
                st_profile.course = course
                st_profile.session = s
                st_profile.save()
                if i < 6:
                    self.stdout.write(self.style.SUCCESS(f'Assigned {u.email} to {course.name}'))

        self.stdout.write(self.style.SUCCESS(f'Done. Total students now: {CustomUser.objects.filter(user_type="3").count()}'))
