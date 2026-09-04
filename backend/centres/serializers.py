from rest_framework import serializers
from .models import ProcurementCentre, OperatingHours


class OperatingHoursSerializer(serializers.ModelSerializer):
    day_name = serializers.CharField(source='get_day_of_week_display', read_only=True)

    class Meta:
        model = OperatingHours
        fields = [
            'id',
            'centre',
            'day_of_week',
            'day_name',
            'opening_time',
            'closing_time',
            'is_closed',
        ]


class ProcurementCentreSerializer(serializers.ModelSerializer):
    """
    Serializer for ProcurementCentre with nested operating hours read representation.
    """
    operating_hours = OperatingHoursSerializer(many=True, read_only=True)
    operators_count = serializers.IntegerField(source='operators.count', read_only=True)

    class Meta:
        model = ProcurementCentre
        fields = [
            'id',
            'name',
            'address',
            'latitude',
            'longitude',
            'district',
            'state',
            'daily_capacity',
            'avg_processing_time_minutes',
            'is_active',
            'operating_hours',
            'operators_count',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
