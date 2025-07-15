from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'chat'

urlpatterns = [
    path('', views.chat_dashboard, name='dashboard'),
    path('with/<int:user_id>/', views.chat_dashboard, name='open_chat'),  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)