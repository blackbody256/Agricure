from django.urls import path
from . import views

app_name = 'administrator'


# URL patterns for the administrator app
urlpatterns = [
    path('upload/', views.upload_dataset_view, name='upload_dataset'),
    path('datasets/', views.dataset_list_view, name='dataset_list'),
    path('datasets/delete/<int:pk>/', views.delete_dataset_view, name='delete_dataset'),

]
