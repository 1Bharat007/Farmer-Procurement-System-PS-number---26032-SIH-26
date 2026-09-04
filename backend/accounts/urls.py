from django.urls import path
from .views import (
    SendFarmerOTPView,
    VerifyFarmerOTPView,
    RegisterFarmerView,
    StaffLoginView,
    CurrentUserView,
)

app_name = 'accounts'

urlpatterns = [
    path('farmer/send-otp/', SendFarmerOTPView.as_view(), name='farmer-send-otp'),
    path('farmer/verify-otp/', VerifyFarmerOTPView.as_view(), name='farmer-verify-otp'),
    path('farmer/register/', RegisterFarmerView.as_view(), name='farmer-register'),
    path('staff/login/', StaffLoginView.as_view(), name='staff-login'),
    path('me/', CurrentUserView.as_view(), name='current-user'),
]
