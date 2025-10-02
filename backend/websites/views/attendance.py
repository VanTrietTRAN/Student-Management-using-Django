from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from oauth2_provider.views.mixins import OAuthLibMixin
from base.views.base import BaseViewSet
from oauth.permissions import TokenHasActionScope
from ..models.attendance import Attendance
from ..serializers.attendance import AttendanceSerializer
from django.db.models import Q
from django.utils import timezone

class AttendanceViewSet(OAuthLibMixin, BaseViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [TokenHasActionScope]
    search_map = {'date': 'exact', 'status': 'exact'}
    
    required_alternate_scopes = {
        'list': [['websites:attendance:view']],
        'retrieve': [['websites:attendance:view']],
        'create': [['websites:attendance:enter']],
        'update': [['websites:attendance:enter']],
        'partial_update': [['websites:attendance:enter']],
        'destroy': [['websites:attendance:enter']],
        'by_subject': [['websites:attendance:view']],
        'by_student': [['websites:attendance:view'], ['users:view-mine']],
        'bulk_create': [['websites:attendance:enter']],
    }

    @action(detail=False, methods=['post'], url_path='bulk-create')
    def bulk_create(self, request):
        """Create multiple attendance records at once"""
        serializer = self.get_serializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], url_path='by-subject/(?P<subject_id>[^/.]+)')
    def by_subject(self, request, subject_id=None):
        """Get attendance records for a specific subject"""
        attendances = Attendance.objects.filter(subject__id=subject_id)
        return Response(self.get_serializer(attendances, many=True).data)
    
    @action(detail=False, methods=['get'], url_path='by-student/(?P<student_id>[^/.]+)')
    def by_student(self, request, student_id=None):
        """Get attendance records for a specific student"""
        attendances = Attendance.objects.filter(student__id=student_id)
        return Response(self.get_serializer(attendances, many=True).data)