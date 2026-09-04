from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class FarmerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='farmer_profile')
    phone = models.CharField(max_length=15, unique=True, db_index=True)
    full_name = models.CharField(max_length=150)
    village = models.CharField(max_length=100, blank=True, default='')
    district = models.CharField(max_length=100, blank=True, default='')
    state = models.CharField(max_length=100, blank=True, default='')
    preferred_language = models.CharField(max_length=10, default='hi')
    crop_type = models.CharField(max_length=100, default='Wheat')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} ({self.phone}) - {self.district}"


class StaffProfile(models.Model):
    ROLE_CHOICES = [
        ('operator', 'Centre Operator'),
        ('officer', 'Procurement Officer'),
        ('admin', 'System Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='operator')
    centre_id = models.CharField(max_length=50, blank=True, default='')
    badge_number = models.CharField(max_length=50, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Staff: {self.user.username} [{self.role}]"


class OTPRecord(models.Model):
    phone = models.CharField(max_length=15, db_index=True)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def is_valid(self):
        # Valid for 10 minutes
        return not self.is_verified and timezone.now() - self.created_at < timedelta(minutes=10)

    def __str__(self):
        return f"OTP for {self.phone}: {self.otp_code} (Verified: {self.is_verified})"
