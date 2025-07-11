from django import forms
from .models import Diagnosis

class DiagnosisForm(forms.ModelForm):
    class Meta:
        model = Diagnosis
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={
                'accept': 'image/*',
                'capture': 'environment',
                'class': 'form-control d-none',
                'id': 'id_image'
            })
        }

    # ✅ Mark image field optional so we can fallback to webcam input
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False

