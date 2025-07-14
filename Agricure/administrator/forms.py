from django import forms

# forms.py
from django import forms
from .models import DatasetUpload

class DatasetUploadForm(forms.ModelForm):
    class Meta:
        model = DatasetUpload
        fields = ['name', 'zip_file']
        labels = {
            'name': 'Dataset Name',
            'zip_file': 'Upload ZIP File',
        }
