from django.urls import path
from . import views

app_name = 'recommendations'

urlpatterns = [
    # Dashboard and main views
    path('', views.recommendation_dashboard, name='dashboard'),
    path('list/', views.recommendation_list, name='list'),
    
    # Recommendation management
    path('request/<int:diagnosis_id>/', views.request_recommendation, name='request'),
    path('detail/<int:pk>/', views.recommendation_detail, name='detail'),
    path('delete/<int:pk>/', views.delete_recommendation, name='delete'),
    path('feedback/<int:pk>/', views.provide_feedback, name='feedback'),
    
    # API endpoints
    path('api/generate/', views.get_agricultural_recommendation, name='api_generate'),
]
