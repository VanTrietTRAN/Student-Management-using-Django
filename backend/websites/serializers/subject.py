from rest_framework import serializers
from websites.models.subject import Subject


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = [
            'id',
            'subject_code',
            'subject_name',
            'credits',
            'major',
            'type',
            'semester',
            'teacher_name',
            'status',
            'created_at',
            'updated_at'
        ]
