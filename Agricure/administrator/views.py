# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import DatasetUploadForm

def upload_dataset_view(request):
    if request.method == 'POST':
        form = DatasetUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dataset uploaded successfully!')
            return redirect('administrator:upload_dataset')  
    else:
        form = DatasetUploadForm()
    
    return render(request, 'admin/upload_dataset.html', {'form': form})
