from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import models
from ..models import StudentProfile, Class, CourseRegistration, Schedule
from ..serializers import ClassSerializer, CourseRegistrationSerializer, ScheduleSerializer

class ClassManagementViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ClassSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        profile = get_object_or_404(StudentProfile, user=self.request.user)
        return Class.objects.filter(
            registrations__student=profile,
            registrations__status='approved'
        )

    @action(detail=True, methods=['get'])
    def course_materials(self, request, pk=None):
        """Download course materials"""
        class_instance = self.get_object()
        materials = class_instance.materials.all()
        serializer = self.get_serializer(materials, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_schedule(self, request):
        """View personal class schedule"""
        profile = get_object_or_404(StudentProfile, user=self.request.user)
        schedule = Schedule.objects.filter(
            student=profile,
            class_instance__registrations__status='approved'
        )
        serializer = ScheduleSerializer(schedule, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def exam_schedule(self, request):
        """View exam schedule"""
        profile = get_object_or_404(StudentProfile, user=self.request.user)
        exam_schedule = Schedule.objects.filter(
            student=profile,
            exam_date__isnull=False
        )
        serializer = ScheduleSerializer(exam_schedule, many=True)
        return Response(serializer.data)