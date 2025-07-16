from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import User  
from administrator.models import DatasetUpload


@login_required
def dashboard(request):
    if request.user.role != 'AGRONOMIST':
        return render(request, '403.html')  # or redirect with error

    return render(request, 'agronomist/dashboard.html')


@login_required
def dataset_list(request):
    if request.user.role.lower() != 'agronomist':
        return render(request, '403.html')  # Optional error page

    datasets = DatasetUpload.objects.all().order_by('-uploaded_at')
    return render(request, 'agronomist/dataset_list.html', {'datasets': datasets})