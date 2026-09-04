from django.urls import path
from .views import NotificationsRootView

app_name = 'notifications'

urlpatterns = [
    path('', NotificationsRootView.as_view(), name='notifications-root'),
]
