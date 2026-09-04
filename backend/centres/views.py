from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ProcurementCentre, OperatingHours
from .serializers import ProcurementCentreSerializer, OperatingHoursSerializer
from accounts.permissions import IsAdminOrReadOnly


class CentresRootView(APIView):
    """
    Module health/root endpoint.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({
            "message": "Procurement Centres endpoint ready",
            "module": "centres"
        }, status=status.HTTP_200_OK)


class ProcurementCentreViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and retrieving procurement centres.
    - Anyone can browse active centres
    - Staff / Admins can modify centres
    """
    serializer_class = ProcurementCentreSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = ProcurementCentre.objects.all().prefetch_related('operating_hours', 'operators')
        district = self.request.query_params.get('district')
        is_active = self.request.query_params.get('is_active')

        if district:
            queryset = queryset.filter(district__iexact=district)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')

        return queryset


class OperatingHoursViewSet(viewsets.ModelViewSet):
    """
    ViewSet for operating hours of procurement centres.
    """
    serializer_class = OperatingHoursSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = OperatingHours.objects.all().select_related('centre')
        centre_id = self.request.query_params.get('centre')
        if centre_id:
            queryset = queryset.filter(centre_id=centre_id)
        return queryset
