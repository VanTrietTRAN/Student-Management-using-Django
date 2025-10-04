from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from oauth.models import User
from websites.models.student import Student
from websites.models.subject import Subject
from websites.models.registration import Registration
from websites.models.tuition import Tuition


class FakeJWT:
    def __init__(self, user_id, scope=''):
        self.user = type('U', (), {'id': user_id})()
        self.scope = scope

    def is_valid(self, scopes=None):
        if not scopes:
            return True
        provided = set(self.scope.split()) if self.scope else set()
        return set(scopes).issubset(provided)


class RegistrationFlowTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # create user and student
        self.user = User.objects.create_user(email='student1@example.com', password='pass', first_name='Student', last_name='One')
        self.student = Student.objects.create(user=self.user, student_id='S001', full_name='Student One', email='student1@example.com', major='CS')
        # create subject
        self.subject = Subject.objects.create(subject_code='CS101', subject_name='Intro', credits=3, major='CS', semester='2025-1', teacher_name='Dr A')

    def test_register_creates_tuition_and_unregister_deletes(self):
        # simulate authentication by setting request.auth to FakeJWT
        token = FakeJWT(user_id=self.user.id, scope='users:view-mine websites:registrations:create websites:tuitions:view')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer faketoken')

        # Monkeypatch the client's handler to inject auth on request
        original_request = self.client.request

        def patched_request(method, path, data=None, **kwargs):
            # call original to build request
            response = original_request(method, path, data=data, **kwargs)
            return response

        self.client.request = patched_request

        # Use the test client .post to call the register endpoint directly via view
        url = '/api/v1/websites/registrations/register'
        payload = {
            'student': self.student.id,
            'subject': self.subject.id,
            'semester': '2025-1',
            'registered_credits': 3,
            'tuition_per_credit': '1000.00'
        }

        # Instead of injecting into the low-level request pipeline (complex), call view directly
        from websites.views.registrations import RegistrationViewSet
        view = RegistrationViewSet.as_view({'post': 'register'})
        # build a DRF Request with force_authenticate equivalent by setting .auth and .user
        from rest_framework.test import APIRequestFactory
        factory = APIRequestFactory()
        req = factory.post(url, payload, format='json')
        from rest_framework.test import force_authenticate
        force_authenticate(req, user=self.user, token=token)

        response = view(req)
        if getattr(response, 'status_code', None) != 201:
            print('DEBUG RESPONSE:', getattr(response, 'data', response.rendered_content if hasattr(response, 'rendered_content') else response))
        assert response.status_code == 201

        # ensure registration and tuition exist
        regs = Registration.objects.filter(student=self.student, subject=self.subject, semester='2025-1')
        self.assertEqual(regs.count(), 1)
        reg = regs.first()
        tuitions = Tuition.objects.filter(registration=reg)
        self.assertEqual(tuitions.count(), 1)

        # now call unregister
        view_del = RegistrationViewSet.as_view({'post': 'unregister'})
        req2 = factory.post(f'/api/v1/websites/registrations/{reg.id}/unregister')
        force_authenticate(req2, user=self.user, token=token)
        response2 = view_del(req2, pk=str(reg.id))
        assert response2.status_code == 204

        # ensure deletion
        self.assertFalse(Registration.objects.filter(id=reg.id).exists())
        self.assertFalse(Tuition.objects.filter(registration=reg).exists())
