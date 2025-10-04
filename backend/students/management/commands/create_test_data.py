from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from students.models.student import Student, Course

class Command(BaseCommand):
    help = 'Create initial student and course data for testing'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        
        # Create test student user
        student_email = 'student@example.edu.vn'
        if not User.objects.filter(email=student_email).exists():
            user = User.objects.create_user(
                email=student_email,
                password='12345678',
                role='student'
            )
            
            # Create student profile
            Student.objects.create(
                student_id='20230001',
                first_name='John',
                last_name='Doe',
                email=student_email,
                department='Computer Science',
                major='Software Engineering',
                enrollment_date='2023-09-01'
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created test student: {student_email}'))
        
        # Create test courses
        courses = [
            {
                'code': 'CS101',
                'name': 'Introduction to Programming',
                'credits': 3,
                'description': 'Basic programming concepts and practices',
                'capacity': 30
            },
            {
                'code': 'CS201',
                'name': 'Data Structures',
                'credits': 4,
                'description': 'Fundamental data structures and algorithms',
                'capacity': 25
            },
            {
                'code': 'CS301',
                'name': 'Software Engineering',
                'credits': 4,
                'description': 'Software development lifecycle and practices',
                'capacity': 20
            }
        ]
        
        for course_data in courses:
            if not Course.objects.filter(code=course_data['code']).exists():
                Course.objects.create(**course_data)
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created course: {course_data["name"]}')
                )