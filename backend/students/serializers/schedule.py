from rest_framework import serializers
from students.models.registration import Schedule

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'
        read_only_fields = ('student', 'class_instance', 'created_at', 'updated_at')