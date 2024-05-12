import uuid
from rest_framework import serializers
from.models import VendorModel

class VendorSerializers(serializers.ModelSerializer):
    """
    Serializer for creating and displaying vendors with specific details.
    """

    class Meta:
        model = VendorModel
        fields = [
            'name',
            'contact_details',
            'address',
            'vendor_code'
        ]

    def create(self, validated_data):
        """
        Override the create method to generate a unique vendor_code.
        """
        return VendorModel.objects.create(**validated_data)

class UpdateVendorSerializer(serializers.ModelSerializer):
    """
    Serializer for updating a vendor, excluding the vendor_code.
    """
    # vendor_code = serializers.CharField(read_only=True)

    class Meta:
        model = VendorModel
        fields = [
            'name',
            'contact_details',
            'address',
          
        ]
        
    def validate(self, data):
        if not any(field in data for field in ['name', 'contact_details', 'address']):
            raise serializers.ValidationError("At least one of 'name', 'contact_details', or 'address' must be provided.")
        return data    

class VendorListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing vendors, showing only vendor_code and name.
    """
    class Meta:
        model = VendorModel
        fields = [
            'vendor_code',
            'name'
        ]

class VendorPerformanceSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving performance metrics of a vendor.
    """
    class Meta:
        model = VendorModel
        fields = [
            'on_time_delivery_rate',
            'quality_rating_avg',
            'average_response_time',
            'fulfillment_rate'
        ]
