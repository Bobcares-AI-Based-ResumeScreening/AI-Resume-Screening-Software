from django.urls import path
from .views import candidates_dashboard

urlpatterns = [
    path('', candidates_dashboard, name='candidates_dashboard'),
]
