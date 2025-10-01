from rest_framework import serializers
from websites.models.classroom import Classroom


class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ['id', 'class_name', 'major', 'year', 'teacher_name', 'room', 'student_count', 'status', 'created_at', 'updated_at']
