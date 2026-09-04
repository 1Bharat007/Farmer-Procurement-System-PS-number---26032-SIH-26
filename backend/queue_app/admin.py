from django.contrib import admin
from .models import QueueToken


@admin.register(QueueToken)
class QueueTokenAdmin(admin.ModelAdmin):
    list_display = (
        'token_number',
        'centre',
        'date',
        'status',
        'get_farmer',
        'estimated_wait_minutes',
        'called_at',
        'served_at',
    )
    list_filter = ('status', 'centre', 'date')
    search_fields = ('token_number', 'booking__farmer__full_name', 'booking__farmer__phone_number')

    @admin.display(description='Farmer')
    def get_farmer(self, obj):
        return obj.booking.farmer.full_name
