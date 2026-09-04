from rest_framework import serializers
from django.contrib.auth.models import User
from .models import FarmerProfile, StaffProfile


class FarmerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerProfile
        fields = [
            'id',
            'phone',
            'full_name',
            'village',
            'district',
            'state',
            'preferred_language',
            'crop_type',
            'created_at',
        ]


class SendOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15, required=True)

    def validate_phone(self, value):
        cleaned = value.strip().replace(" ", "").replace("-", "")
        if cleaned.startswith("+91"):
            cleaned = cleaned[3:]
        if not cleaned.isdigit() or len(cleaned) != 10:
            raise serializers.ValidationError("Please enter a valid 10-digit mobile number.")
        return cleaned


class VerifyOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15, required=True)
    otp = serializers.CharField(max_length=6, required=True)

    def validate_phone(self, value):
        cleaned = value.strip().replace(" ", "").replace("-", "")
        if cleaned.startswith("+91"):
            cleaned = cleaned[3:]
        if not cleaned.isdigit() or len(cleaned) != 10:
            raise serializers.ValidationError("Please enter a valid 10-digit mobile number.")
        return cleaned

    def validate_otp(self, value):
        cleaned = value.strip()
        if not cleaned.isdigit() or len(cleaned) != 6:
            raise serializers.ValidationError("OTP must be a 6-digit number.")
        return cleaned


class FarmerRegisterSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15, required=True)
    full_name = serializers.CharField(max_length=150, required=True)
    village = serializers.CharField(max_length=100, required=False, allow_blank=True, default="")
    district = serializers.CharField(max_length=100, required=False, allow_blank=True, default="")
    state = serializers.CharField(max_length=100, required=False, allow_blank=True, default="")
    preferred_language = serializers.CharField(max_length=10, required=False, default="hi")
    crop_type = serializers.CharField(max_length=100, required=False, default="Wheat")

    def validate_phone(self, value):
        cleaned = value.strip().replace(" ", "").replace("-", "")
        if cleaned.startswith("+91"):
            cleaned = cleaned[3:]
        if not cleaned.isdigit() or len(cleaned) != 10:
            raise serializers.ValidationError("Please enter a valid 10-digit mobile number.")
        return cleaned


class StaffLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
