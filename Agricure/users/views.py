from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import SignUpForm
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied

class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return '/admin-dashboard/'
        return '/dashboard/'

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = '/dashboard/'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        if user.role == 'ADMIN':
            return HttpResponseRedirect('/admin-dashboard/')
        return super().form_valid(form)

def home(request):
    return render(request, 'home.html')

def is_farmer_or_admin(user):
    return user.is_authenticated and (user.role == 'FARMER' or user.role == 'ADMIN')

@user_passes_test(is_farmer_or_admin)
def manager_dashboard(request):
    return render(request, 'dashboards/manager.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def admin_dashboard(request):
    if request.user.role != 'ADMIN':
        raise PermissionDenied
    return render(request, 'admin_dashboard.html')
