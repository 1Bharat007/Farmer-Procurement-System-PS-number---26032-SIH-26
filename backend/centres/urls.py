from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProcurementCentreViewSet, OperatingHoursViewSet, CentresRootView

app_name = 'centres'

router = DefaultRouter()
router.register(r'operating-hours', OperatingHoursViewSet, basename='operating-hours')
router.register(r'', ProcurementCentreViewSet, basename='centre')

urlpatterns = [
    path('root/', CentresRootView.as_view(), name='centres-root'),
    path('', include(router.urls)),
]
