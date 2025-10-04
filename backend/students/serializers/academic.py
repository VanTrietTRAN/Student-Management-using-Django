from rest_framework import serializers
from students.models.academic import AcademicHistory

class AcademicHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicHistory
        fields = '__all__'
        read_only_fields = ('student', 'created_at', 'updated_at')