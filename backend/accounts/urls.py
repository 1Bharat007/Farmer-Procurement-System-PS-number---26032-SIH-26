from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    FarmerViewSet,
    CentreOperatorViewSet,
    SendFarmerOTPView,
    VerifyFarmerOTPView,
    RegisterFarmerView,
    StaffLoginView,
    CurrentUserView,
)

app_name = 'accounts'

router = DefaultRouter()
router.register(r'farmers', FarmerViewSet, basename='farmer')
router.register(r'operators', CentreOperatorViewSet, basename='operator')

urlpatterns = [
    # Auth endpoints
    path('farmer/send-otp/', SendFarmerOTPView.as_view(), name='farmer-send-otp'),
    path('farmer/verify-otp/', VerifyFarmerOTPView.as_view(), name='farmer-verify-otp'),
    path('farmer/register/', RegisterFarmerView.as_view(), name='farmer-register'),
    path('staff/login/', StaffLoginView.as_view(), name='staff-login'),
    path('me/', CurrentUserView.as_view(), name='current-user'),

    # REST Resource routes
    path('', include(router.urls)),
]
