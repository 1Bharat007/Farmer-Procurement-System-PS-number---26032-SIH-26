from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet, NotificationsRootView

app_name = 'notifications'

router = DefaultRouter()
router.register(r'', NotificationViewSet, basename='notification')

urlpatterns = [
    path('root/', NotificationsRootView.as_view(), name='notifications-root'),
    path('', include(router.urls)),
]
