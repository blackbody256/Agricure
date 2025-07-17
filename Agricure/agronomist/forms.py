from django import forms
from .models import AgronomistUpload

class AgronomistUploadForm(forms.ModelForm):
    class Meta:
        model = AgronomistUpload
        fields = ['title', 'file']
