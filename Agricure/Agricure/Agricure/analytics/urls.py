from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('farmer/', views.farmer_analytics, name='farmer_analytics'),
    path('admin-dashboard/', views.admin_analytics, name='admin_dashboard'),
]
