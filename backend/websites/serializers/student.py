from rest_framework import serializers
from websites.models.student import Student


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'id',
            'student_id',
            'full_name',
            'email',
            'phone',
            'classroom',
            'major',
            'profile_picture',
            'status',
            'gpa',
            'created_at',
            'updated_at'
        ]
