from django.urls import path
from . import views

app_name = 'diagnosis'

urlpatterns = [
    path('', views.diagnose, name='diagnose'),
    path('history/', views.diagnosis_history, name='diagnosis_history'),
]
