from rest_framework import serializers
from ..models.attendance import Attendance
from ..models.student import Student
from ..models.subject import Subject
from ..models.classroom import Classroom

class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    subject_name = serializers.CharField(source='subject.subject_name', read_only=True)
    classroom_name = serializers.CharField(source='classroom.class_name', read_only=True)
    
    class Meta:
        model = Attendance
        fields = [
            'id', 'student', 'subject', 'classroom',
            'student_name', 'subject_name', 'classroom_name',
            'date', 'status', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']