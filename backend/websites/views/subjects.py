from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from oauth2_provider.views.mixins import OAuthLibMixin
from base.views.base import BaseViewSet
from oauth.permissions import TokenHasActionScope
from websites.models.subject import Subject
from websites.serializers.subject import SubjectSerializer


class SubjectViewSet(OAuthLibMixin, BaseViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [TokenHasActionScope]
    required_alternate_scopes = {
        'list': [['websites:subjects:view']],
        'retrieve': [['websites:subjects:view']],
        'create': [['websites:subjects:edit']],
        'update': [['websites:subjects:edit']],
        'partial_update': [['websites:subjects:edit']],
        'destroy': [['websites:subjects:edit']],
        'assign_teacher': [['websites:subjects:assign'], ['websites:subjects:edit']]
    }
    search_map = { 'subject_code': 'icontains', 'subject_name': 'icontains' }

    @action(detail=True, methods=['post'], url_path='assign-teacher')
    def assign_teacher(self, request, pk=None):
        subject = self.get_object()
        teacher_name = request.data.get('teacher_name')
        if not teacher_name:
            return Response({'error': 'teacher_name is required'}, status=status.HTTP_400_BAD_REQUEST)
        subject.teacher_name = teacher_name
        subject.save()
        return Response(self.get_serializer(subject).data, status=status.HTTP_200_OK)
