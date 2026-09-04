from django.contrib import admin
from .models import ProcurementCentre, OperatingHours


class OperatingHoursInline(admin.TabularInline):
    model = OperatingHours
    extra = 7
    max_num = 7


@admin.register(ProcurementCentre)
class ProcurementCentreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'district',
        'state',
        'daily_capacity',
        'avg_processing_time_minutes',
        'is_active',
        'created_at'
    )
    list_filter = ('district', 'state', 'is_active')
    search_fields = ('name', 'district', 'address')
    inlines = [OperatingHoursInline]


@admin.register(OperatingHours)
class OperatingHoursAdmin(admin.ModelAdmin):
    list_display = ('centre', 'day_of_week', 'opening_time', 'closing_time', 'is_closed')
    list_filter = ('day_of_week', 'is_closed', 'centre')
