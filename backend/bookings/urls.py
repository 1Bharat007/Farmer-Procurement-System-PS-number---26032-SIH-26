from django.urls import path
from .views import BookingsRootView

app_name = 'bookings'

urlpatterns = [
    path('', BookingsRootView.as_view(), name='bookings-root'),
]
