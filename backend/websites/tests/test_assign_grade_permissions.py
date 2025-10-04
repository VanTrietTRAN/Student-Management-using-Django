from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from oauth.models import User
from websites.models.subject import Subject
from websites.models.classroom import Classroom
from websites.views.subjects import SubjectViewSet
from websites.views.classrooms import ClassroomViewSet
from websites.views.grades import GradeViewSet
from websites.models.student import Student
from websites.models.grade import Grade


class AssignAndGradePermissionTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(email='admin@example.com', password='pass', first_name='Admin', last_name='A')
        self.teacher = User.objects.create_user(email='teacher@example.com', password='pass', first_name='Teacher', last_name='T')
        self.student_user = User.objects.create_user(email='stud@example.com', password='pass', first_name='Stud', last_name='S')
        self.student = Student.objects.create(user=self.student_user, student_id='S010', full_name='Student Ten', email='stud@example.com', major='CS')
        self.subject = Subject.objects.create(subject_code='CS200', subject_name='Advanced', credits=3, major='CS', semester='2025-1', teacher_name='')
        self.classroom = Classroom.objects.create(class_name='C1', major='CS', year='2025', teacher_name='')

    def token_with_scopes(self, user, scopes_str):
        class Token:
            def __init__(self, user_id, scope):
                self.user = type('U', (), {'id': user_id})()
                self.scope = scope

            def is_valid(self, scopes=None):
                if not scopes:
                    return True
                provided = set(self.scope.split()) if self.scope else set()
                return set(scopes).issubset(provided)

        return Token(user.id, scopes_str)

    def test_assign_teacher_allowed_with_scope(self):
        factory = APIRequestFactory()
        view = SubjectViewSet.as_view({'post': 'assign_teacher'})
        req = factory.post(f'/api/v1/websites/subjects/{self.subject.id}/assign-teacher', {'teacher_name': 'Dr Nice'}, format='json')
        token = self.token_with_scopes(self.admin, 'websites:subjects:assign')
        force_authenticate(req, user=self.admin, token=token)
        resp = view(req, pk=str(self.subject.id))
        assert resp.status_code == 200

    def test_assign_teacher_denied_without_scope(self):
        factory = APIRequestFactory()
        view = ClassroomViewSet.as_view({'post': 'assign_teacher'})
        req = factory.post(f'/api/v1/websites/classrooms/{self.classroom.id}/assign-teacher', {'teacher_name': 'Dr No'}, format='json')
        token = self.token_with_scopes(self.teacher, '')
        force_authenticate(req, user=self.teacher, token=token)
        resp = view(req, pk=str(self.classroom.id))
        assert resp.status_code in (403, 401)

    def test_grade_entry_allowed_for_lecturer_scope(self):
        factory = APIRequestFactory()
        view = GradeViewSet.as_view({'post': 'create'})
        payload = {'student': self.student.id, 'subject': self.subject.id, 'semester': '2025-1', 'midterm_score': 6.0, 'final_score': 7.0}
        req = factory.post('/api/v1/websites/grades', payload, format='json')
        token = self.token_with_scopes(self.teacher, 'websites:grades:enter')
        force_authenticate(req, user=self.teacher, token=token)
        resp = view(req)
        assert resp.status_code in (200, 201)

    def test_grade_entry_denied_for_student_scope(self):
        factory = APIRequestFactory()
        view = GradeViewSet.as_view({'post': 'create'})
        payload = {'student': self.student.id, 'subject': self.subject.id, 'semester': '2025-1', 'midterm_score': 6.0, 'final_score': 7.0}
        req = factory.post('/api/v1/websites/grades', payload, format='json')
        token = self.token_with_scopes(self.student_user, 'users:view-mine')
        force_authenticate(req, user=self.student_user, token=token)
        resp = view(req)
        assert resp.status_code in (403, 401)
