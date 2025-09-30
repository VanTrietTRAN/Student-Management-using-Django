from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from oauth.models import User

class RoleBasedAccessMiddleware(MiddlewareMixin):
    """
    Middleware to handle role-based access control
    """
    
    # Define protected routes for each user type
    ADMIN_ROUTES = [
        '/websites/',
        '/websites/students',
        '/websites/classes', 
        '/websites/subjects',
        '/websites/grades',
        '/websites/schedule',
        '/websites/tuition',
        '/websites/notifications',
        '/websites/rewards',
        '/websites/teachers'
    ]
    
    TEACHER_ROUTES = [
        '/websites/',
        '/websites/classes',
        '/websites/subjects',
        '/websites/grades',
        '/websites/schedule',
        '/websites/notifications'
    ]
    
    STUDENT_ROUTES = [
        '/websites/',
        '/websites/student-dashboard',
        '/websites/student-grades',
        '/websites/student-schedule',
        '/websites/student-tuition',
        '/websites/student-profile'
    ]
    
    TRAINING_STAFF_ROUTES = [
        '/websites/',
        '/websites/students',
        '/websites/classes',
        '/websites/subjects',
        '/websites/grades',
        '/websites/schedule',
        '/websites/tuition',
        '/websites/notifications'
    ]
    
    STUDENT_AFFAIRS_ROUTES = [
        '/websites/',
        '/websites/students',
        '/websites/rewards',
        '/websites/notifications'
    ]
    
    def process_request(self, request):
        # Skip middleware for API calls and static files
        if (request.path.startswith('/api/') or 
            request.path.startswith('/static/') or 
            request.path.startswith('/media/') or
            request.path.startswith('/admin/')):
            return None
            
        # Skip middleware for login/logout
        if request.path in ['/login/', '/logout/', '/']:
            return None
            
        # Check if user is authenticated
        if not hasattr(request, 'user') or not request.user.is_authenticated:
            return redirect('/login/')
            
        # Get user type
        user_type = getattr(request.user, 'user_type', 'student')
        
        # Check if user has access to the requested route
        if not self.has_access(user_type, request.path):
            return JsonResponse({
                'error': 'Access denied',
                'message': f'You do not have permission to access this page'
            }, status=403)
            
        return None
    
    def has_access(self, user_type, path):
        """Check if user has access to the requested path"""
        
        # Admin has access to everything
        if user_type == 'admin':
            return True
            
        # Check specific routes for each user type
        if user_type == 'teacher':
            return any(path.startswith(route) for route in self.TEACHER_ROUTES)
        elif user_type == 'student':
            return any(path.startswith(route) for route in self.STUDENT_ROUTES)
        elif user_type == 'training_staff':
            return any(path.startswith(route) for route in self.TRAINING_STAFF_ROUTES)
        elif user_type == 'student_affairs':
            return any(path.startswith(route) for route in self.STUDENT_AFFAIRS_ROUTES)
            
        return False
