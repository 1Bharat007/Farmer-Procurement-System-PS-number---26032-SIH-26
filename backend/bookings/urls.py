from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SlotViewSet, BookingViewSet, PaymentStatusViewSet, BookingsRootView

app_name = 'bookings'

router = DefaultRouter()
router.register(r'slots', SlotViewSet, basename='slot')
router.register(r'payments', PaymentStatusViewSet, basename='payment')
router.register(r'', BookingViewSet, basename='booking')

urlpatterns = [
    path('root/', BookingsRootView.as_view(), name='bookings-root'),
    path('', include(router.urls)),
]
