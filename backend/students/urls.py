from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.auth import StudentLoginView, StudentRefreshTokenView
from .views.student import (
    get_student_profile,
    update_student_profile,
    register_course,
    get_grades,
    submit_tuition_payment
)
from .views import (
    StudentProfileViewSet,
    ClassManagementViewSet,
    CourseRegistrationViewSet,
    TuitionFeeViewSet,
)

router = DefaultRouter()
router.register(r'profile', StudentProfileViewSet, basename='student-profile')
router.register(r'classes', ClassManagementViewSet, basename='student-classes')
router.register(r'registration', CourseRegistrationViewSet, basename='course-registration')
router.register(r'tuition', TuitionFeeViewSet, basename='tuition-fee')

app_name = 'students'

urlpatterns = [
    path('', include(router.urls)),
    
    # Authentication endpoints
    path('auth/login/', StudentLoginView.as_view(), name='student-login'),
    path('auth/refresh/', StudentRefreshTokenView.as_view(), name='student-refresh-token'),

    # Additional student endpoints
    path('me/profile/', get_student_profile, name='student-profile'),
    path('me/profile/update/', update_student_profile, name='update-profile'),
    path('me/courses/register/', register_course, name='register-course'),
    path('me/grades/', get_grades, name='student-grades'),
    path('me/tuition/payment/', submit_tuition_payment, name='tuition-payment'),
]