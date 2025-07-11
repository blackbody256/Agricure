from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from .forms import SignUpForm, ProfileEditForm
from .models import User  # Add this import
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User


#for user management
from django.contrib.auth import get_user_model
User = get_user_model()
from .forms import FarmerCreationForm
from django import forms
from .forms import FarmerForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
from functools import wraps


#decorator to check if user is admin
def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'ADMIN':
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return _wrapped_view

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
    model = User  # Now this will work because User is imported
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


# User management views
@login_required
@admin_required
def manage_farmers(request):
    farmers = User.objects.exclude(role='ADMIN')
    return render(request, "manage_farmers.html", {"farmers": farmers})

@login_required
@admin_required
def edit_farmer(request, user_id):
    farmer = get_object_or_404(User, pk=user_id)

    if request.method == "POST":
        form = FarmerForm(request.POST, instance=farmer)
        if form.is_valid():
            form.save()
            messages.success(request, "Farmer updated successfully.")
            return redirect("users:manage_farmers")
    else:
        form = FarmerForm(instance=farmer)

    return render(request, "edit_farmer.html", {"form": form, "farmer": farmer})

@login_required
@admin_required
def delete_farmer(request, user_id):
    farmer = get_object_or_404(User, pk=user_id)
    farmer.delete()
    messages.success(request, "Farmer deleted.")
    return redirect("users:manage_farmers")


@login_required
@admin_required
def add_farmer(request):
    if request.method == "POST":
        form = FarmerCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Farmer added successfully.")
            return redirect("users:manage_farmers")
    else:
        form = FarmerCreationForm()
    
    return render(request, "add_farmer.html", {"form": form})
