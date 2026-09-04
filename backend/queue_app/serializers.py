from rest_framework import serializers
from .models import QueueToken
from centres.serializers import ProcurementCentreSerializer


class QueueTokenSerializer(serializers.ModelSerializer):
    """
    Serializer for live queue token tracking.
    """
    farmer_id = serializers.IntegerField(source='booking.farmer.id', read_only=True)
    farmer_name = serializers.CharField(source='booking.farmer.full_name', read_only=True)
    farmer_phone = serializers.CharField(source='booking.farmer.phone_number', read_only=True)
    crop_type = serializers.CharField(source='booking.farmer.crop_type', read_only=True)
    quantity_kg = serializers.DecimalField(source='booking.quantity_kg', max_digits=10, decimal_places=2, read_only=True)
    booking_status = serializers.CharField(source='booking.status', read_only=True)
    centre_name = serializers.CharField(source='centre.name', read_only=True)
    centre_district = serializers.CharField(source='centre.district', read_only=True)

    class Meta:
        model = QueueToken
        fields = [
            'id',
            'booking',
            'centre',
            'centre_name',
            'centre_district',
            'date',
            'token_number',
            'status',
            'estimated_wait_minutes',
            'farmer_id',
            'farmer_name',
            'farmer_phone',
            'crop_type',
            'quantity_kg',
            'booking_status',
            'called_at',
            'served_at',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']
