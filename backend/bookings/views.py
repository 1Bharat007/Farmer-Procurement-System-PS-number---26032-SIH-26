from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Slot, Booking, PaymentStatus
from .serializers import SlotSerializer, BookingSerializer, PaymentStatusSerializer
from accounts.permissions import IsOwnerOrCentreOperatorOrAdmin, IsAdminOrReadOnly


class BookingsRootView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({
            "message": "Slot Bookings endpoint ready",
            "module": "bookings"
        }, status=status.HTTP_200_OK)


class SlotViewSet(viewsets.ModelViewSet):
    """
    ViewSet for available delivery time slots.
    - Anyone can browse available slots
    - Centre Operators and Admins can create and manage slots
    """
    serializer_class = SlotSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = Slot.objects.all().select_related('centre')
        centre_id = self.request.query_params.get('centre')
        date = self.request.query_params.get('date')
        from_date = self.request.query_params.get('from_date')
        to_date = self.request.query_params.get('to_date')

        if centre_id:
            queryset = queryset.filter(centre_id=centre_id)
        if date:
            queryset = queryset.filter(date=date)
        if from_date:
            queryset = queryset.filter(date__gte=from_date)
        if to_date:
            queryset = queryset.filter(date__lte=to_date)

        return queryset.order_by('date', 'start_time')


class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for crop intake slot bookings.
    - Farmers see only their own bookings
    - Centre Operators see bookings for their assigned centre
    - Admins see all bookings
    """
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrCentreOperatorOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Booking.objects.all().select_related('farmer', 'slot', 'slot__centre', 'payment', 'queue_token')

        if hasattr(user, 'centre_operator') and user.centre_operator.is_active:
            centre = user.centre_operator.centre
            return Booking.objects.filter(slot__centre=centre).select_related(
                'farmer', 'slot', 'slot__centre', 'payment', 'queue_token'
            )

        return Booking.objects.filter(farmer=user).select_related(
            'farmer', 'slot', 'slot__centre', 'payment', 'queue_token'
        )

    def perform_create(self, serializer):
        user = self.request.user
        # If user is farmer or operator booking on farmer's behalf
        farmer = serializer.validated_data.get('farmer')
        if not farmer or not user.is_staff:
            serializer.save(farmer=user)
        else:
            serializer.save()

    @action(detail=True, methods=['post'], url_path='check-in')
    def check_in(self, request, pk=None):
        """
        Mark farmer as checked-in at the centre gate and generate queue token.
        """
        booking = self.get_object()
        if booking.status in ['completed', 'cancelled']:
            return Response(
                {"error": f"Cannot check in a booking with status '{booking.status}'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking.status = 'checked_in'
        booking.save(update_fields=['status', 'updated_at'])

        # Auto-create queue token if not exists
        from queue_app.models import QueueToken
        from django.db.models import Max

        token, created = QueueToken.objects.get_or_create(
            booking=booking,
            defaults={
                'centre': booking.slot.centre,
                'date': booking.slot.date,
                'token_number': (
                    QueueToken.objects.filter(centre=booking.slot.centre, date=booking.slot.date)
                    .aggregate(Max('token_number'))['token_number__max'] or 0
                ) + 1,
                'status': 'waiting',
                'estimated_wait_minutes': 20,
            }
        )

        return Response({
            "status": "success",
            "message": "Farmer checked in successfully.",
            "booking_id": booking.id,
            "token_number": token.token_number,
        })

    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel_booking(self, request, pk=None):
        """
        Cancel a booking and release slot capacity.
        """
        booking = self.get_object()
        if booking.status in ['completed', 'cancelled']:
            return Response(
                {"error": f"Cannot cancel booking with status '{booking.status}'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking.status = 'cancelled'
        booking.save(update_fields=['status', 'updated_at'])

        if booking.slot.booked_count > 0:
            booking.slot.booked_count -= 1
            booking.slot.save(update_fields=['booked_count'])

        return Response({
            "status": "success",
            "message": "Booking cancelled successfully.",
            "booking_id": booking.id,
        })


class PaymentStatusViewSet(viewsets.ModelViewSet):
    """
    ViewSet for DBT payment statuses.
    - Farmers see only payments for their own bookings
    - Centre Operators see payments for bookings at their centre
    - Admins see all payments
    """
    serializer_class = PaymentStatusSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrCentreOperatorOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return PaymentStatus.objects.all().select_related('booking', 'booking__farmer')

        if hasattr(user, 'centre_operator') and user.centre_operator.is_active:
            centre = user.centre_operator.centre
            return PaymentStatus.objects.filter(booking__slot__centre=centre).select_related(
                'booking', 'booking__farmer'
            )

        return PaymentStatus.objects.filter(booking__farmer=user).select_related('booking', 'booking__farmer')
