from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from oauth2_provider.views.mixins import OAuthLibMixin
from base.views.base import BaseViewSet
from oauth.permissions import TokenHasActionScope, IsOwnerOrHasActionScope
from websites.models.student import Student
from websites.serializers.student import StudentSerializer


class StudentViewSet(OAuthLibMixin, BaseViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [TokenHasActionScope, IsOwnerOrHasActionScope]
    owner_field = 'user'
    required_alternate_scopes = {
        'list': [['websites:students:view']],
        'retrieve': [['websites:students:view'], ['users:view-mine']],
        'create': [['websites:students:edit']],
        'update': [['websites:students:edit'], ['users:edit-mine']],
        'partial_update': [['websites:students:edit'], ['users:edit-mine']],
        'destroy': [['websites:students:edit']],
        'registrations': [['websites:registrations:view'], ['users:view-mine']]
    }
    search_map = { 'student_id': 'icontains', 'full_name': 'icontains', 'email': 'icontains' }

    @action(detail=True, methods=['get'], url_path='registrations')
    def registrations(self, request, pk=None):
        student = self.get_object()
        regs = student.registrations.all()
        from websites.serializers.registration import RegistrationSerializer
        return Response(RegistrationSerializer(regs, many=True).data)
