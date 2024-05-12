from datetime import timedelta
from django.utils import timezone
from rest_framework import serializers
from.models import PurchaseOrderModel

utc = timezone.now()

class PurchaseOrderSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying purchase orders.
    """
    class Meta:
        model = PurchaseOrderModel
        fields = ['po_number', 'vendor', 'status']

class PurchaseOrderCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating purchase orders.
    """
    order_date = serializers.DateTimeField(read_only=True)
    delivery_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = PurchaseOrderModel
        fields = '__all__'

    def create(self, validated_data):
        """
        Override the create method to set order_date, delivery_date, and status.
        """
        order_date = timezone.localtime(utc)
        delivery_date = order_date + timedelta(days=5)
        status = "Pending"
        issue_date = order_date

        validated_data['order_date'] = order_date
        validated_data['delivery_date'] = delivery_date
        validated_data['status'] = status
        validated_data['issue_date'] = issue_date

        return super().create(validated_data)

class PurchaseOrderUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating purchase orders.
    """
    class Meta:
        model = PurchaseOrderModel
        fields = ['delivery_date', 'quality_rating', 'status']

class PurchaseOrderAcknowledgeSerializer(serializers.ModelSerializer):
    """
    Serializer for acknowledging purchase orders.
    """
    class Meta:
        model = PurchaseOrderModel
        fields = ['acknowledgment_date']
