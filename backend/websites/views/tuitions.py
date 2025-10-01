from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from oauth2_provider.views.mixins import OAuthLibMixin
from base.views.base import BaseViewSet
from oauth.permissions import TokenHasActionScope, IsOwnerOrHasActionScope
from websites.models.tuition import Tuition
from websites.serializers.tuition import TuitionSerializer


class TuitionViewSet(OAuthLibMixin, BaseViewSet):
    queryset = Tuition.objects.all()
    serializer_class = TuitionSerializer
    search_map = { 'semester': 'exact', 'status': 'exact' }
    permission_classes = [TokenHasActionScope, IsOwnerOrHasActionScope]
    owner_field = 'student'
    required_alternate_scopes = {
        'list': [['websites:tuitions:view']],
        'retrieve': [['websites:tuitions:view'], ['users:view-mine']],
        'create': [['websites:tuitions:view']],
        'pay': [['websites:tuitions:pay'], ['users:view-mine']]
    }

    @action(detail=True, methods=['post'], url_path='pay')
    def pay(self, request, pk=None):
        tuition = self.get_object()
        tuition.status = 'Đã đóng'
        from django.utils import timezone
        tuition.payment_date = timezone.now().date()
        tuition.save()
        return Response(self.get_serializer(tuition).data)
