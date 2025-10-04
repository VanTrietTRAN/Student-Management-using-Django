from rest_framework import serializers
from students.models.tuition import TuitionFee, Payment, Invoice

class TuitionFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TuitionFee
        fields = '__all__'
        read_only_fields = ('student', 'semester', 'due_date', 'created_at', 'updated_at')

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('tuition_fee', 'payment_date', 'transaction_id', 'created_at', 'updated_at')

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'
        read_only_fields = ('payment', 'invoice_number', 'issue_date', 'created_at', 'updated_at')