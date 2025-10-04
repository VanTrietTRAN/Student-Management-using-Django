from rest_framework.exceptions import APIException
from rest_framework import status

class StudentNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Student not found.'

class CourseRegistrationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Course registration failed.'

class InvalidGradeError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid grade value.'

class PaymentError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Payment processing failed.'