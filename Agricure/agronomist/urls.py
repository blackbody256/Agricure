from django.urls import path
from . import views

app_name = 'agronomist'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
     path('list/', views.dataset_list, name='dataset_list'),
     path('report/', views.agronomist_report, name='report'),
     path('upload/', views.upload_data, name='upload_data'),
    path('uploads/', views.view_uploads, name='view_uploads'),
    path('uploads/delete/<int:upload_id>/', views.delete_upload, name='delete_upload'),

]
