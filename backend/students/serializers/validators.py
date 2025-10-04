from rest_framework import serializers

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = 'Student'
        fields = ('id', 'first_name', 'last_name', 'email', 'student_id', 'department', 'major')

    def validate_student_id(self, value):
        if not value or len(value) != 8:
            raise serializers.ValidationError("Student ID must be 8 characters long")
        return value

    def validate_email(self, value):
        if not value.endswith('.edu.vn'):
            raise serializers.ValidationError("Email must be a valid educational email")
        return value

class CourseRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = 'CourseRegistration'
        fields = ('id', 'student', 'course', 'semester', 'registration_date', 'status')

    def validate(self, data):
        # Check if course registration is within allowed period
        from datetime import datetime
        if data['registration_date'] > datetime.now():
            raise serializers.ValidationError("Cannot register for future dates")
            
        # Check if student has met prerequisites
        if not self.has_prerequisites(data['student'], data['course']):
            raise serializers.ValidationError("Prerequisites not met for this course")
            
        # Check if course capacity is full
        if self.is_course_full(data['course']):
            raise serializers.ValidationError("Course is already full")
            
        return data
    
    def has_prerequisites(self, student, course):
        # Logic to check prerequisites
        return True
        
    def is_course_full(self, course):
        # Logic to check course capacity
        return False

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = 'Grade'
        fields = ('id', 'student', 'course', 'grade_value', 'semester')

    def validate_grade_value(self, value):
        if value < 0 or value > 10:
            raise serializers.ValidationError("Grade must be between 0 and 10")
        return value

class TuitionPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = 'TuitionPayment'
        fields = ('id', 'student', 'amount', 'payment_date', 'payment_method', 'status')

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Payment amount must be positive")
        return value

    def validate_payment_method(self, value):
        valid_methods = ['credit_card', 'bank_transfer', 'cash']
        if value not in valid_methods:
            raise serializers.ValidationError(f"Payment method must be one of: {', '.join(valid_methods)}")
        return value