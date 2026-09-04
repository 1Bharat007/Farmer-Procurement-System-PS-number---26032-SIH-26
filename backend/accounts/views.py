import random
import logging
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import Farmer, CentreOperator, OTPRecord
from .serializers import (
    FarmerSerializer,
    CentreOperatorSerializer,
    SendOTPSerializer,
    VerifyOTPSerializer,
    FarmerRegisterSerializer,
    StaffLoginSerializer,
)
from .permissions import IsOwnerOrCentreOperatorOrAdmin, IsCentreOperator

logger = logging.getLogger(__name__)


def get_tokens_for_user(user):
    """Generate JWT Access and Refresh tokens for authenticated user."""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class FarmerViewSet(viewsets.ModelViewSet):
    """
    CRUD ViewSet for Farmer accounts.
    - Superusers: view/manage all farmers
    - Centre Operators: view farmers who have bookings at their centre
    - Farmers: view/manage only their own profile
    """
    serializer_class = FarmerSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrCentreOperatorOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Farmer.objects.all()

        if hasattr(user, 'centre_operator') and user.centre_operator.is_active:
            centre = user.centre_operator.centre
            return Farmer.objects.filter(bookings__slot__centre=centre).distinct()

        # Regular farmer sees only self
        return Farmer.objects.filter(id=user.id)


class CentreOperatorViewSet(viewsets.ModelViewSet):
    """
    CRUD ViewSet for Centre Operators.
    - Superusers: view/manage all operators
    - Operators: view their own operator profile
    """
    serializer_class = CentreOperatorSerializer
    permission_classes = [IsAuthenticated, IsCentreOperator]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return CentreOperator.objects.all().select_related('user', 'centre')

        if hasattr(user, 'centre_operator') and user.centre_operator.is_active:
            return CentreOperator.objects.filter(id=user.centre_operator.id).select_related('user', 'centre')

        return CentreOperator.objects.none()


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

        # Generate 6-digit OTP
        otp_code = str(random.randint(100000, 999999))
        OTPRecord.objects.create(phone=phone, otp_code=otp_code)

        logger.info(f"[SMS GATEWAY STUB] OTP for {phone}: {otp_code}")

        # Check if farmer is already registered
        is_registered = Farmer.objects.filter(phone_number=phone).exists()

        return Response({
            "status": "success",
            "message": "OTP sent successfully to registered mobile number.",
            "phone": phone,
            "is_registered": is_registered,
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

        # Check OTPRecord: allow matching active OTP or master demo OTP '123456'
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

        # Find or create Farmer user
        farmer, _ = Farmer.objects.get_or_create(
            phone_number=phone,
            defaults={
                'full_name': f"Farmer {phone[-4:]}",
                'preferred_language': 'hi',
                'crop_type': 'Wheat',
            }
        )

        tokens = get_tokens_for_user(farmer)

        return Response({
            "status": "success",
            "message": "Farmer authenticated successfully.",
            "tokens": tokens,
            "user": {
                "id": farmer.id,
                "phone": farmer.phone_number,
                "full_name": farmer.full_name,
                "village": farmer.village,
                "district": farmer.district,
                "state": farmer.state,
                "preferred_language": farmer.preferred_language,
                "crop_type": farmer.crop_type,
                "role": "farmer",
            }
        }, status=status.HTTP_200_OK)


class RegisterFarmerView(APIView):
    """
    Endpoint: POST /api/accounts/farmer/register/
    Creates or updates a farmer profile and returns JWT authentication tokens.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = FarmerRegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        phone = data['phone']

        farmer, created = Farmer.objects.update_or_create(
            phone_number=phone,
            defaults={
                'full_name': data['full_name'],
                'village': data.get('village', ''),
                'district': data.get('district', ''),
                'state': data.get('state', ''),
                'preferred_language': data.get('preferred_language', 'hi'),
                'crop_type': data.get('crop_type', 'Wheat'),
            }
        )

        tokens = get_tokens_for_user(farmer)

        return Response({
            "status": "success",
            "message": "Farmer registered and authenticated successfully.",
            "tokens": tokens,
            "user": {
                "id": farmer.id,
                "phone": farmer.phone_number,
                "full_name": farmer.full_name,
                "village": farmer.village,
                "district": farmer.district,
                "state": farmer.state,
                "preferred_language": farmer.preferred_language,
                "crop_type": farmer.crop_type,
                "role": "farmer",
            }
        }, status=status.HTTP_201_CREATED)


class StaffLoginView(APIView):
    """
    Endpoint: POST /api/accounts/staff/login/
    Authenticates Centre Operators, Officers, and Admins.
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
            user = authenticate(request, phone_number=username, password=password)

        if user is None:
            return Response({
                "status": "error",
                "message": "Invalid staff credentials. Please check your username and password."
            }, status=status.HTTP_401_UNAUTHORIZED)

        tokens = get_tokens_for_user(user)
        is_operator = hasattr(user, 'centre_operator') and user.centre_operator.is_active
        role = "operator" if is_operator else ("admin" if user.is_superuser else "staff")

        user_data = {
            "id": user.id,
            "username": user.phone_number,
            "full_name": user.full_name,
            "role": role,
            "is_staff": user.is_staff,
        }
        if is_operator:
            user_data["centre_id"] = user.centre_operator.centre_id
            user_data["centre_name"] = user.centre_operator.centre.name

        return Response({
            "status": "success",
            "message": "Staff authenticated successfully.",
            "tokens": tokens,
            "user": user_data,
        }, status=status.HTTP_200_OK)


class CurrentUserView(APIView):
    """
    Endpoint: GET /api/accounts/me/
    Returns current authenticated user details from JWT token.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        is_operator = hasattr(user, 'centre_operator') and user.centre_operator.is_active

        if is_operator:
            role = "operator"
            profile_data = {
                "centre_id": user.centre_operator.centre_id,
                "centre_name": user.centre_operator.centre.name,
                "badge": user.centre_operator.badge_number
            }
        elif user.is_superuser:
            role = "admin"
            profile_data = {}
        else:
            role = "farmer"
            profile_data = FarmerSerializer(user).data

        return Response({
            "id": user.id,
            "phone": user.phone_number,
            "full_name": user.full_name,
            "role": role,
            "profile": profile_data,
        })
