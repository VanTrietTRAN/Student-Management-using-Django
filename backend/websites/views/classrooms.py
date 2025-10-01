from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from oauth2_provider.views.mixins import OAuthLibMixin
from base.views.base import BaseViewSet
from oauth.permissions import TokenHasActionScope
from websites.models.classroom import Classroom
from websites.serializers.classroom import ClassroomSerializer


class ClassroomViewSet(OAuthLibMixin, BaseViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    permission_classes = [TokenHasActionScope]
    required_alternate_scopes = {
        'list': [['websites:classrooms:view']],
        'retrieve': [['websites:classrooms:view']],
        'create': [['websites:classrooms:edit']],
        'update': [['websites:classrooms:edit']],
        'partial_update': [['websites:classrooms:edit']],
        'destroy': [['websites:classrooms:edit']],
        'assign_teacher': [['websites:classrooms:assign'], ['websites:classrooms:edit']]
    }
    search_map = { 'class_name': 'icontains', 'major': 'icontains' }

    @action(detail=True, methods=['post'], url_path='assign-teacher')
    def assign_teacher(self, request, pk=None):
        classroom = self.get_object()
        teacher_name = request.data.get('teacher_name')
        if not teacher_name:
            return Response({'error': 'teacher_name is required'}, status=status.HTTP_400_BAD_REQUEST)
        classroom.teacher_name = teacher_name
        classroom.save()
        return Response(self.get_serializer(classroom).data, status=status.HTTP_200_OK)
