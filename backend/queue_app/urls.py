from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QueueTokenViewSet, QueueRootView

app_name = 'queue_app'

router = DefaultRouter()
router.register(r'tokens', QueueTokenViewSet, basename='queue-token')
router.register(r'', QueueTokenViewSet, basename='queue')

urlpatterns = [
    path('root/', QueueRootView.as_view(), name='queue-root'),
    path('', include(router.urls)),
]
