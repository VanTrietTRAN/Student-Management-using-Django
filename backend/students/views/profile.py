from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..models import StudentProfile, Grade, AcademicHistory
from ..serializers import (
    StudentProfileSerializer, GradeSerializer,
    AcademicHistorySerializer
)

class StudentProfileViewSet(viewsets.ModelViewSet):
    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return StudentProfile.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        """View personal profile information"""
        profile = get_object_or_404(StudentProfile, user=request.user)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_grades(self, request):
        """View all grades and academic performance"""
        profile = get_object_or_404(StudentProfile, user=request.user)
        grades = Grade.objects.filter(student=profile)
        serializer = GradeSerializer(grades, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def academic_history(self, request):
        """View academic history through semesters"""
        profile = get_object_or_404(StudentProfile, user=request.user)
        history = AcademicHistory.objects.filter(student=profile)
        serializer = AcademicHistorySerializer(history, many=True)
        return Response(serializer.data)