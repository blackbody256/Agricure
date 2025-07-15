from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import User  

@login_required
def dashboard(request):
    if request.user.role != 'AGRONOMIST':
        return render(request, '403.html')  # or redirect with error

    return render(request, 'agronomist/dashboard.html')
