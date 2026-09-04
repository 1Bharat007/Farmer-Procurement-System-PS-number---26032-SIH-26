from django.urls import path
from .views import QueueRootView

app_name = 'queue'

urlpatterns = [
    path('', QueueRootView.as_view(), name='queue-root'),
]
