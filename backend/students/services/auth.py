from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from oauth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

class AuthService:
    @staticmethod
    def authenticate_student(email: str, password: str):
        """Authenticate student user and return tokens"""
        try:
            user = authenticate(email=email, password=password)
            if user is None:
                return None, "Invalid credentials"
                
            if user.user_type != 'student':
                return None, "Access denied. Student account required."

            refresh = RefreshToken.for_user(user)
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': str(user.id),
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'user_type': user.user_type
                }
            }, None

        except ValidationError as e:
            return None, str(e)
        except Exception as e:
            return None, "Authentication failed"

    @staticmethod
    def validate_student_token(token: str):
        """Validate student's token"""
        try:
            refresh = RefreshToken(token)
            user_id = refresh['user_id']
            user = User.objects.get(id=user_id)
            
            if user.user_type != 'student':
                return False, "Invalid student token"
                
            return True, None
        except Exception as e:
            return False, str(e)