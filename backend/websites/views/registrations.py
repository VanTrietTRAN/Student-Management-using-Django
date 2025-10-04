from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from oauth2_provider.views.mixins import OAuthLibMixin
from base.views.base import BaseViewSet
from oauth.permissions import TokenHasActionScope, IsOwnerOrHasActionScope
from websites.models.registration import Registration
from websites.serializers.registration import RegistrationSerializer
from websites.models.tuition import Tuition
from websites.serializers.tuition import TuitionSerializer


class RegistrationViewSet(OAuthLibMixin, BaseViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    search_map = { 'semester': 'exact' }
    permission_classes = [TokenHasActionScope, IsOwnerOrHasActionScope]
    owner_field = 'student'
    required_alternate_scopes = {
        'list': [['websites:registrations:view']],
        'retrieve': [['websites:registrations:view'], ['users:view-mine']],
        'create': [['websites:registrations:create'], ['users:view-mine']],
        'register': [['websites:registrations:create'], ['users:view-mine']],
        'unregister': [['websites:registrations:delete'], ['users:view-mine']]
    }

    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        # create registration and corresponding tuition
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            reg = serializer.save()
            # create tuition record
            amount = reg.total_tuition
            from django.utils import timezone
            from datetime import timedelta
            due_date = timezone.now().date() + timedelta(days=30)
            tuition = Tuition.objects.create(
                registration=reg,
                student=reg.student,
                amount=amount,
                semester=reg.semester,
                due_date=due_date,
                status='Chưa đóng'
            )
            return Response({ 'registration': RegistrationSerializer(reg).data, 'tuition': TuitionSerializer(tuition).data }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='unregister')
    def unregister(self, request, pk=None):
        reg = self.get_object()
        # remove tuition if exists
        Tuition.objects.filter(registration=reg).delete()
        reg.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
