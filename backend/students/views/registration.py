from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import models
from ..models import StudentProfile, Class, CourseRegistration
from ..serializers import CourseRegistrationSerializer, ClassSerializer

class CourseRegistrationViewSet(viewsets.ModelViewSet):
    serializer_class = CourseRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CourseRegistration.objects.filter(student__user=self.request.user)

    @action(detail=False, methods=['get'])
    def available_courses(self, request):
        """View list of available courses for registration"""
        profile = get_object_or_404(StudentProfile, user=request.user)
        available_classes = Class.objects.filter(
            course__semester__is_current=True,
            current_students__lt=models.F('max_students')
        )
        serializer = ClassSerializer(available_classes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def registration_status(self, request):
        """View course registration status"""
        profile = get_object_or_404(StudentProfile, user=request.user)
        registrations = self.get_queryset()
        serializer = self.get_serializer(registrations, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Register for a course"""
        profile = get_object_or_404(StudentProfile, user=request.user)
        class_id = request.data.get('class_instance')
        class_instance = get_object_or_404(Class, id=class_id)
        
        # Check if already registered
        if CourseRegistration.objects.filter(
            student=profile,
            class_instance=class_instance
        ).exists():
            return Response(
                {'detail': 'Already registered for this class'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if class is full
        if class_instance.current_students >= class_instance.max_students:
            return Response(
                {'detail': 'Class is full'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        registration = CourseRegistration.objects.create(
            student=profile,
            class_instance=class_instance,
            status='pending'
        )
        serializer = self.get_serializer(registration)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        """Cancel course registration"""
        instance = self.get_object()
        if instance.status == 'approved':
            return Response(
                {'detail': 'Cannot cancel approved registration'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)