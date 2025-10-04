from rest_framework import serializers
from .models import (
    StudentProfile, Course, Grade, Semester, AcademicHistory,
    Class, CourseMaterial, CourseRegistration, Schedule,
    TuitionFee, Payment, Invoice
)
from oauth.serializers import UserSerializer


class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = StudentProfile
        fields = '__all__'
        read_only_fields = ('student_id', 'enrollment_year', 'current_semester')


class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class GradeSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    semester = SemesterSerializer(read_only=True)
    
    class Meta:
        model = Grade
        fields = '__all__'


class AcademicHistorySerializer(serializers.ModelSerializer):
    semester = SemesterSerializer(read_only=True)
    
    class Meta:
        model = AcademicHistory
        fields = '__all__'


class CourseMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseMaterial
        fields = '__all__'


class ClassSerializer(serializers.ModelSerializer):
    teacher = UserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    materials = CourseMaterialSerializer(many=True, read_only=True)
    
    class Meta:
        model = Class
        fields = '__all__'


class CourseRegistrationSerializer(serializers.ModelSerializer):
    class_instance = ClassSerializer(read_only=True)
    
    class Meta:
        model = CourseRegistration
        fields = '__all__'


class ScheduleSerializer(serializers.ModelSerializer):
    class_instance = ClassSerializer(read_only=True)
    
    class Meta:
        model = Schedule
        fields = '__all__'


class TuitionFeeSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    semester = SemesterSerializer(read_only=True)
    
    class Meta:
        model = TuitionFee
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    tuition_fee = TuitionFeeSerializer(read_only=True)
    
    class Meta:
        model = Payment
        fields = '__all__'


class InvoiceSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(read_only=True)
    
    class Meta:
        model = Invoice
        fields = '__all__'