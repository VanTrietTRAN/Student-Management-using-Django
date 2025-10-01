from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from oauth2_provider.views.mixins import OAuthLibMixin
from base.views.base import BaseViewSet
from oauth.permissions import TokenHasActionScope, IsOwnerOrHasActionScope
from websites.models.grade import Grade
from websites.serializers.grade import GradeSerializer


class GradeViewSet(OAuthLibMixin, BaseViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    search_map = { 'semester': 'exact' }
    permission_classes = [TokenHasActionScope, IsOwnerOrHasActionScope]
    owner_field = 'student'
    required_alternate_scopes = {
        'list': [['websites:grades:view']],
        'retrieve': [['websites:grades:view'], ['users:view-mine']],
        'create': [['websites:grades:enter']],
        'update': [['websites:grades:enter']],
        'partial_update': [['websites:grades:enter']],
        'by_student': [['websites:grades:view'], ['users:view-mine']]
    }

    @action(detail=False, methods=['get'], url_path='by-student/(?P<student_id>[^/.]+)')
    def by_student(self, request, student_id=None):
        grades = Grade.objects.filter(student__id=student_id)
        return Response(self.get_serializer(grades, many=True).data)
