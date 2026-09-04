from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import QueueToken
from .serializers import QueueTokenSerializer
from accounts.permissions import IsOwnerOrCentreOperatorOrAdmin


class QueueRootView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({
            "message": "Real-time Queue endpoint ready",
            "module": "queue"
        }, status=status.HTTP_200_OK)


class QueueTokenViewSet(viewsets.ModelViewSet):
    """
    ViewSet for live token queue.
    - Farmers see tokens for their own bookings
    - Centre operators see tokens for their assigned centre
    - Superusers see all tokens
    """
    serializer_class = QueueTokenSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrCentreOperatorOrAdmin]

    def get_permissions(self):
        if self.action == 'live_status':
            return [permissions.AllowAny()]
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        user = self.request.user
        queryset = QueueToken.objects.all().select_related(
            'booking', 'booking__farmer', 'centre'
        )

        centre_id = self.request.query_params.get('centre')
        date = self.request.query_params.get('date')
        status_filter = self.request.query_params.get('status')

        if centre_id:
            queryset = queryset.filter(centre_id=centre_id)
        if date:
            queryset = queryset.filter(date=date)
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        if user.is_superuser:
            return queryset

        if hasattr(user, 'centre_operator') and user.centre_operator.is_active:
            centre = user.centre_operator.centre
            return queryset.filter(centre=centre)

        return queryset.filter(booking__farmer=user)

    @action(detail=False, methods=['get'], url_path='live', permission_classes=[permissions.AllowAny])
    def live_status(self, request):
        """
        Public/dashboard feed for live queue board at a centre.
        Query params: ?centre=<id>&date=<YYYY-MM-DD>
        """
        centre_id = request.query_params.get('centre')
        date = request.query_params.get('date') or timezone.localdate().isoformat()

        if not centre_id:
            return Response(
                {"error": "Please provide the 'centre' query parameter."},
                status=status.HTTP_400_BAD_REQUEST
            )

        tokens = QueueToken.objects.filter(
            centre_id=centre_id,
            date=date
        ).select_related('booking', 'booking__farmer').order_by('token_number')

        current_token = tokens.filter(status__in=['called', 'processing']).first()
        waiting_tokens = tokens.filter(status='waiting')
        completed_tokens_count = tokens.filter(status='completed').count()

        return Response({
            "centre_id": int(centre_id),
            "date": date,
            "total_tokens_issued": tokens.count(),
            "completed_count": completed_tokens_count,
            "current_serving": QueueTokenSerializer(current_token).data if current_token else None,
            "waiting_count": waiting_tokens.count(),
            "waiting_tokens": QueueTokenSerializer(waiting_tokens[:10], many=True).data,
        })

    @action(detail=True, methods=['post'], url_path='call')
    def call_token(self, request, pk=None):
        """Call token to gate / weighbridge."""
        token = self.get_object()
        token.status = 'called'
        token.called_at = timezone.now()
        token.save(update_fields=['status', 'called_at'])

        # Sync booking status
        token.booking.status = 'in_queue'
        token.booking.save(update_fields=['status', 'updated_at'])

        return Response({
            "status": "success",
            "message": f"Token #{token.token_number} called to gate.",
            "token_id": token.id,
        })

    @action(detail=True, methods=['post'], url_path='complete')
    def complete_token(self, request, pk=None):
        """Mark token intake as completed."""
        token = self.get_object()
        token.status = 'completed'
        token.served_at = timezone.now()
        token.save(update_fields=['status', 'served_at'])

        # Sync booking status
        token.booking.status = 'completed'
        token.booking.save(update_fields=['status', 'updated_at'])

        return Response({
            "status": "success",
            "message": f"Token #{token.token_number} marked as completed.",
            "token_id": token.id,
        })
