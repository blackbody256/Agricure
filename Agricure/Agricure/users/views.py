from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from .forms import SignUpForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

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
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        
        # Redirect based on user role
        if user.role == 'ADMIN':
            return HttpResponseRedirect('/admin-dashboard/')
        else:
            return HttpResponseRedirect('/dashboard/')

# Profile edit page
class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileEditForm
    template_name = 'profile_edit.html'
    success_url = reverse_lazy('users:profile_edit')
    
    def get_object(self):
        # Return the current user's profile
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Your profile has been updated successfully!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

def home(request):
    return render(request, 'home.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def admin_dashboard(request):
    if request.user.role != 'ADMIN':
        raise PermissionDenied
    return render(request, 'admin_dashboard.html')

def about(request):
    return render(request, 'about.html')