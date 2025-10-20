"""
Context processors for Staff templates
Automatically adds common data to all staff views
"""

from student_management_app.models import Staffs, Subjects


def staff_subjects(request):
    """
    Add staff's subjects to all staff templates
    Usage in template: {% for subject in subjects %}
    """
    context = {}
    
    # Check if user is authenticated and is staff
    if request.user.is_authenticated:
        try:
            # Check if user has Staffs profile
            staff = Staffs.objects.get(admin=request.user.id)
            # Get all subjects taught by this staff (staff_id is ForeignKey to CustomUser)
            subjects = Subjects.objects.filter(staff_id=request.user)
            context['subjects'] = subjects
        except Staffs.DoesNotExist:
            # User is not a staff, no subjects
            context['subjects'] = []
    else:
        context['subjects'] = []
    
    return context
