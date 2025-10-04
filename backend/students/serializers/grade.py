from rest_framework import serializers
from students.models.academic import Grade

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'
        read_only_fields = ('student', 'created_at', 'updated_at')