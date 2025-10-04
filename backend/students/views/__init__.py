from .profile import StudentProfileViewSet
from .class_management import ClassManagementViewSet
from .registration import CourseRegistrationViewSet
from .tuition import TuitionFeeViewSet

__all__ = [
    'StudentProfileViewSet',
    'ClassManagementViewSet',
    'CourseRegistrationViewSet',
    'TuitionFeeViewSet',
]