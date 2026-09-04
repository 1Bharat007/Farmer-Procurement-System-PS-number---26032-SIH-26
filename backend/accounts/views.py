import random
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import FarmerProfile, StaffProfile, OTPRecord
from .serializers import (
    FarmerProfileSerializer,
    SendOTPSerializer,
    VerifyOTPSerializer,
    FarmerRegisterSerializer,
    StaffLoginSerializer,
)

logger = logging.getLogger(__name__)


def get_tokens_for_user(user):
    """Generate JWT Access and Refresh tokens for authenticated user."""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class SendFarmerOTPView(APIView):
    """
    Endpoint: POST /api/accounts/farmer/send-otp/
    Generates and sends a 6-digit OTP to the farmer's mobile number.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        phone = serializer.validated_data['phone']

        # Generate 6-digit OTP (in dev/demo mode, predictable or random)
        otp_code = str(random.randint(100000, 999999))

        # Save to OTPRecord table
        OTPRecord.objects.create(phone=phone, otp_code=otp_code)

        # TODO: Fast2SMS / SMS Gateway integration
        # Example: send_sms_via_fast2sms(phone, f"Your KisanSlot verification code is {otp_code}")
        logger.info(f"[SMS GATEWAY STUB] OTP for {phone}: {otp_code}")

        # Check if farmer is already registered
        is_registered = FarmerProfile.objects.filter(phone=phone).exists()

        return Response({
            "status": "success",
            "message": "OTP sent successfully to registered mobile number.",
            "phone": phone,
            "is_registered": is_registered,
            # In development/demo, expose dev_otp for seamless testing without SMS credits
            "dev_otp": otp_code,
        }, status=status.HTTP_200_OK)


class VerifyFarmerOTPView(APIView):
    """
    Endpoint: POST /api/accounts/farmer/verify-otp/
    Validates OTP and logs the farmer in with JWT tokens.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        phone = serializer.validated_data['phone']
        otp = serializer.validated_data['otp']

        # Check OTPRecord
        # Allow matching valid OTP or master demo OTP '123456'
        valid_record = OTPRecord.objects.filter(
            phone=phone,
            otp_code=otp,
            is_verified=False
        ).order_by('-created_at').first()

        if not valid_record and otp != "123456":
            return Response({
                "status": "error",
                "message": "Invalid or expired OTP. Please enter the correct 6-digit code."
            }, status=status.HTTP_400_BAD_REQUEST)

        if valid_record:
            valid_record.is_verified = True
            valid_record.save()

        # Find or create User with username = phone
        user, created = User.objects.get_or_create(
            username=phone,
            defaults={'first_name': f"Farmer {phone[-4:]}"}
        )

        # Find or create FarmerProfile
        farmer_profile, _ = FarmerProfile.objects.get_or_create(
            user=user,
            defaults={
                'phone': phone,
                'full_name': user.first_name,
                'preferred_language': 'hi',
            }
        )

        tokens = get_tokens_for_user(user)

        return Response({
            "status": "success",
            "message": "Farmer authenticated successfully.",
            "tokens": tokens,
            "user": {
                "id": user.id,
                "phone": phone,
                "full_name": farmer_profile.full_name,
                "village": farmer_profile.village,
                "district": farmer_profile.district,
                "state": farmer_profile.state,
                "preferred_language": farmer_profile.preferred_language,
                "crop_type": farmer_profile.crop_type,
                "role": "farmer",
            }
        }, status=status.HTTP_200_OK)


class RegisterFarmerView(APIView):
    """
    Endpoint: POST /api/accounts/farmer/register/
    Creates a new farmer profile inline and returns JWT authentication tokens.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = FarmerRegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        phone = data['phone']

        # Create or update Django User
        user, _ = User.objects.get_or_create(
            username=phone,
            defaults={'first_name': data['full_name']}
        )
        user.first_name = data['full_name']
        user.save()

        # Create or update FarmerProfile
        farmer_profile, created = FarmerProfile.objects.update_or_create(
            user=user,
            defaults={
                'phone': phone,
                'full_name': data['full_name'],
                'village': data.get('village', ''),
                'district': data.get('district', ''),
                'state': data.get('state', ''),
                'preferred_language': data.get('preferred_language', 'hi'),
                'crop_type': data.get('crop_type', 'Wheat'),
            }
        )

        tokens = get_tokens_for_user(user)

        return Response({
            "status": "success",
            "message": "Farmer registered and authenticated successfully.",
            "tokens": tokens,
            "user": {
                "id": user.id,
                "phone": phone,
                "full_name": farmer_profile.full_name,
                "village": farmer_profile.village,
                "district": farmer_profile.district,
                "state": farmer_profile.state,
                "preferred_language": farmer_profile.preferred_language,
                "crop_type": farmer_profile.crop_type,
                "role": "farmer",
            }
        }, status=status.HTTP_201_CREATED)


class StaffLoginView(APIView):
    """
    Endpoint: POST /api/accounts/staff/login/
    Authenticates Centre Operators, Officers, and Admins with username and password.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = StaffLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(request, username=username, password=password)

        if user is None:
            # Check if user exists or demo fallback
            return Response({
                "status": "error",
                "message": "Invalid staff credentials. Please check your username and password."
            }, status=status.HTTP_401_UNAUTHORIZED)

        tokens = get_tokens_for_user(user)
        staff_profile = getattr(user, 'staff_profile', None)
        role = staff_profile.role if staff_profile else ("admin" if user.is_superuser else "operator")

        return Response({
            "status": "success",
            "message": "Staff authenticated successfully.",
            "tokens": tokens,
            "user": {
                "id": user.id,
                "username": user.username,
                "full_name": user.get_full_name() or user.username,
                "email": user.email,
                "role": role,
                "is_staff": user.is_staff,
            }
        }, status=status.HTTP_200_OK)


class CurrentUserView(APIView):
    """
    Endpoint: GET /api/accounts/me/
    Returns current authenticated user details from JWT token.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        farmer_profile = getattr(user, 'farmer_profile', None)
        staff_profile = getattr(user, 'staff_profile', None)

        if farmer_profile:
            role = "farmer"
            profile_data = FarmerProfileSerializer(farmer_profile).data
        elif staff_profile:
            role = staff_profile.role
            profile_data = {"centre_id": staff_profile.centre_id, "badge": staff_profile.badge_number}
        else:
            role = "admin" if user.is_superuser else "staff"
            profile_data = {}

        return Response({
            "id": user.id,
            "username": user.username,
            "role": role,
            "profile": profile_data,
        })
