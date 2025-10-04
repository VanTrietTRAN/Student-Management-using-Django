from rest_framework import serializers
from students.models.profile import StudentProfile

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = '__all__'
        read_only_fields = ('user', 'student_id', 'created_at', 'updated_at')