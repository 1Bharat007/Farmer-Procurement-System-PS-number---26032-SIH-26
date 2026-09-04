from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Farmer, CentreOperator, OTPRecord


@admin.register(Farmer)
class FarmerAdmin(BaseUserAdmin):
    list_display = ('phone_number', 'full_name', 'village', 'district', 'state', 'preferred_language', 'crop_type', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'preferred_language', 'crop_type', 'district')
    search_fields = ('phone_number', 'full_name', 'village', 'district')
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'village', 'district', 'state', 'preferred_language', 'crop_type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'full_name', 'district', 'crop_type', 'password'),
        }),
    )


@admin.register(CentreOperator)
class CentreOperatorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'centre', 'badge_number', 'is_active', 'created_at')
    list_filter = ('is_active', 'centre')
    search_fields = ('user__full_name', 'user__phone_number', 'badge_number', 'centre__name')


@admin.register(OTPRecord)
class OTPRecordAdmin(admin.ModelAdmin):
    list_display = ('phone', 'otp_code', 'is_verified', 'created_at')
    list_filter = ('is_verified', 'created_at')
    search_fields = ('phone',)
