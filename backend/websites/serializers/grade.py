from rest_framework import serializers
from websites.models.grade import Grade


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['id', 'student', 'subject', 'semester', 'midterm_score', 'final_score', 'gpa', 'status', 'created_at', 'updated_at']
