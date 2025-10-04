from rest_framework import serializers
from students.models.registration import CourseRegistration

class CourseRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseRegistration
        fields = '__all__'
        read_only_fields = ('student', 'registration_date', 'status', 'created_at', 'updated_at')