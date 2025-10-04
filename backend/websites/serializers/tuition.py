from rest_framework import serializers
from websites.models.tuition import Tuition


class TuitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tuition
        fields = ['id', 'registration', 'student', 'amount', 'semester', 'due_date', 'payment_date', 'status', 'created_at', 'updated_at']
