from rest_framework import viewsets
from websites.models.teacher import Teacher
from websites.serializers.teacher import TeacherSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
