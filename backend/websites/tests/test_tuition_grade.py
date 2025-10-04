from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from oauth.models import User
from websites.models.student import Student
from websites.models.subject import Subject
from websites.models.tuition import Tuition
from websites.models.grade import Grade
from websites.views.tuitions import TuitionViewSet
from websites.views.grades import GradeViewSet


class TuitionAndGradeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='student2@example.com', password='pass', first_name='Student', last_name='Two')
        self.student = Student.objects.create(user=self.user, student_id='S002', full_name='Student Two', email='student2@example.com', major='CS')
        self.subject = Subject.objects.create(subject_code='CS102', subject_name='Data', credits=3, major='CS', semester='2025-1', teacher_name='Dr B')
        # create a tuition
        from django.utils import timezone
        self.tuition = Tuition.objects.create(student=self.student, amount='3000.00', semester='2025-1', due_date=timezone.now().date())

    def test_pay_tuition_marks_paid_and_sets_date(self):
        factory = APIRequestFactory()
        view = TuitionViewSet.as_view({'post': 'pay'})
        req = factory.post(f'/api/v1/websites/tuitions/{self.tuition.id}/pay')
        class TokenObj:
            def __init__(self, user_id):
                self.user = type('U', (), {'id': user_id})()
                self.scope = 'websites:tuitions:pay'

            def is_valid(self, scopes=None):
                if not scopes:
                    return True
                provided = set(self.scope.split()) if self.scope else set()
                return set(scopes).issubset(provided)

        token = TokenObj(self.user.id)
        force_authenticate(req, user=self.user, token=token)
        response = view(req, pk=str(self.tuition.id))
        assert response.status_code == 200
        t = Tuition.objects.get(id=self.tuition.id)
        self.assertEqual(t.status, 'Đã đóng')
        self.assertIsNotNone(t.payment_date)

    def test_grade_entry_calculates_gpa(self):
        # create a grade and ensure GPA auto-calculated
        g = Grade.objects.create(student=self.student, subject=self.subject, semester='2025-1', midterm_score=7.0, final_score=8.0)
        # GPA = 0.3*7 + 0.7*8 = 2.1 + 5.6 = 7.7
        self.assertAlmostEqual(g.gpa, 7.7, places=3)
