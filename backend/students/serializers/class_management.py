from rest_framework import serializers
from students.models.class_management import Class

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')