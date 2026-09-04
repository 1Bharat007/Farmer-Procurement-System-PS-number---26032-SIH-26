from django.contrib import admin
from .models import Slot, Booking, PaymentStatus


class PaymentStatusInline(admin.StackedInline):
    model = PaymentStatus
    extra = 0


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ('id', 'centre', 'date', 'start_time', 'end_time', 'capacity', 'booked_count', 'is_full')
    list_filter = ('centre', 'date')
    search_fields = ('centre__name', 'centre__district')
    ordering = ('date', 'start_time')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'farmer',
        'get_centre',
        'get_date',
        'status',
        'quantity_kg',
        'qr_code_token',
        'created_at',
    )
    list_filter = ('status', 'slot__centre', 'slot__date')
    search_fields = ('farmer__full_name', 'farmer__phone_number', 'qr_code_token')
    inlines = [PaymentStatusInline]

    @admin.display(description='Centre')
    def get_centre(self, obj):
        return obj.slot.centre.name

    @admin.display(description='Slot Date')
    def get_date(self, obj):
        return f"{obj.slot.date} ({obj.slot.start_time.strftime('%H:%M')})"


@admin.register(PaymentStatus)
class PaymentStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'amount', 'status', 'transaction_reference', 'paid_at')
    list_filter = ('status',)
    search_fields = ('transaction_reference', 'booking__farmer__full_name')
