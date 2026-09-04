from django.urls import path
from .views import CentresRootView

app_name = 'centres'

urlpatterns = [
    path('', CentresRootView.as_view(), name='centres-root'),
]
