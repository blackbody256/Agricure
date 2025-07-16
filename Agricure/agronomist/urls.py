from django.urls import path
from . import views

app_name = 'agronomist'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
     path('list/', views.dataset_list, name='dataset_list'),
]
