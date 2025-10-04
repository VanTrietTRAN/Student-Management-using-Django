from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from students.permissions import IsStudent
from students.models.student import Student, Course, CourseRegistration, Grade, TuitionPayment
from students.serializers.validators import (
    StudentProfileSerializer, 
    CourseRegistrationSerializer,
    GradeSerializer,
    TuitionPaymentSerializer
)
from students.exceptions import (
    StudentNotFound,
    CourseRegistrationError,
    InvalidGradeError,
    PaymentError
)
from django.shortcuts import get_object_or_404
from django.db import transaction
from datetime import datetime

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsStudent])
def get_student_profile(request):
    try:
        student = get_object_or_404(Student, user=request.user)
        serializer = StudentProfileSerializer(student)
        return Response(serializer.data)
    except Student.DoesNotExist:
        raise StudentNotFound()

@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsStudent])
def update_student_profile(request):
    try:
        student = get_object_or_404(Student, user=request.user)
        serializer = StudentProfileSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Student.DoesNotExist:
        raise StudentNotFound()

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsStudent])
def register_course(request):
    try:
        with transaction.atomic():
            serializer = CourseRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                # Check if registration period is active
                if not is_registration_period_active():
                    raise CourseRegistrationError("Course registration period is closed")
                
                # Additional validation logic here
                
                serializer.save(student=request.user.student)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        raise CourseRegistrationError(str(e))

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsStudent])
def get_grades(request):
    try:
        student = get_object_or_404(Student, user=request.user)
        grades = Grade.objects.filter(student=student)
        serializer = GradeSerializer(grades, many=True)
        return Response(serializer.data)
    except Student.DoesNotExist:
        raise StudentNotFound()

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsStudent])
def submit_tuition_payment(request):
    try:
        with transaction.atomic():
            serializer = TuitionPaymentSerializer(data=request.data)
            if serializer.is_valid():
                # Process payment logic here
                payment = serializer.save(student=request.user.student)
                
                # Additional payment processing logic
                
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        raise PaymentError(str(e))

# Helper functions
def is_registration_period_active():
    # Logic to check if registration period is active
    return True