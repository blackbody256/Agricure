from django.urls import path
from .views import SignUpView, home, dashboard, admin_dashboard, CustomLoginView
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

app_name = 'users'

urlpatterns = [
    path('', home, name='home'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
