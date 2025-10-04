from rest_framework import serializers
from websites.models.student import Student

<<<<<<< HEAD

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'id',
            'student_id',
            'full_name',
            'email',
            'phone',
            'classroom',
            'major',
            'profile_picture',
            'status',
            'gpa',
            'created_at',
            'updated_at'
        ]
=======
class StudentSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False, allow_null=True)
    class_name = serializers.CharField(source='classroom.name', read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'student_id', 'full_name', 'email', 'phone', 
                'classroom', 'class_name', 'major', 'profile_picture',
                'status', 'gpa', 'created_at', 'updated_at']
        
    def create(self, validated_data):
        # Handle profile picture upload
        profile_picture = validated_data.get('profile_picture')
        instance = super().create(validated_data)
        if profile_picture:
            instance.profile_picture = profile_picture
            instance.save()
        return instance

    def update(self, instance, validated_data):
        # Handle profile picture update
        profile_picture = validated_data.pop('profile_picture', None)
        instance = super().update(instance, validated_data)
        if profile_picture:
            instance.profile_picture = profile_picture
            instance.save()
        return instance
>>>>>>> 3b3381a6d34ff10ab244e9176bf5c5305c89c0c0
