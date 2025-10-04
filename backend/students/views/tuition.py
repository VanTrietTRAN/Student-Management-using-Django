from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..models import StudentProfile, TuitionFee, Payment, Invoice
from ..serializers import TuitionFeeSerializer, PaymentSerializer, InvoiceSerializer

class TuitionFeeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TuitionFeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TuitionFee.objects.filter(student__user=self.request.user)

    @action(detail=False, methods=['get'])
    def semester_fees(self, request):
        """View tuition fees for current semester"""
        profile = get_object_or_404(StudentProfile, user=request.user)
        fees = TuitionFee.objects.filter(
            student=profile,
            semester__is_current=True
        )
        serializer = self.get_serializer(fees, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def payment_history(self, request):
        """View payment history"""
        profile = get_object_or_404(StudentProfile, user=request.user)
        payments = Payment.objects.filter(tuition_fee__student=profile)
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def get_invoice(self, request, pk=None):
        """Generate/download invoice for a payment"""
        tuition_fee = self.get_object()
        invoice = get_object_or_404(Invoice, payment__tuition_fee=tuition_fee)
        serializer = InvoiceSerializer(invoice)
        return Response(serializer.data)