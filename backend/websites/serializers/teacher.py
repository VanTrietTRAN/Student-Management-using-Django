from rest_framework import serializers
from websites.models.teacher import Teacher

class TeacherSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Teacher
        fields = '__all__'
