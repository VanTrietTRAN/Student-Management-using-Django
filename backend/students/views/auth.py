from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .services.auth import AuthService

class StudentLoginView(APIView):
    """View for student login"""
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response({
                'error': 'Both email and password are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        auth_data, error = AuthService.authenticate_student(email, password)
        if error:
            return Response({
                'error': error
            }, status=status.HTTP_401_UNAUTHORIZED)
            
        return Response(auth_data, status=status.HTTP_200_OK)


class StudentRefreshTokenView(APIView):
    """View for refreshing student access token"""
    
    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({
                'error': 'Refresh token is required'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        is_valid, error = AuthService.validate_student_token(refresh_token)
        if not is_valid:
            return Response({
                'error': error
            }, status=status.HTTP_401_UNAUTHORIZED)
            
        # Generate new access token
        try:
            refresh = RefreshToken(refresh_token)
            return Response({
                'access': str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)