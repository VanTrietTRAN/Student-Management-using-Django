from functools import wraps
from rest_framework.permissions import BasePermission
from oauth.models import User

class IsStudent(BasePermission):
    """
    Custom permission to only allow students to access the view.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'student')

def student_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.role != 'student':
            raise PermissionDenied("Access denied. Student role required.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view