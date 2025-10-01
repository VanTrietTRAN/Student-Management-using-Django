from rest_framework import serializers
from websites.models.registration import Registration


class RegistrationSerializer(serializers.ModelSerializer):
    total_tuition = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)

    class Meta:
        model = Registration
        fields = ['id', 'student', 'subject', 'semester', 'registered_credits', 'tuition_per_credit', 'total_tuition', 'created_at', 'updated_at']
