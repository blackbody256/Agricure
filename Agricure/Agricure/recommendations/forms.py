from django import forms
from django.core.exceptions import ValidationError
from .models import Recommendation, Feedback

class RecommendationRequestForm(forms.Form):
    """
    Form to request a recommendation for a specific diagnosis
    """
    city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your city name (e.g., Kampala)',
            'required': True
        }),
        help_text="Enter the city where your farm is located"
    )
    
    # Optional: allow users to specify country
    country_code = forms.CharField(
        max_length=2,
        initial='UG',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'UG'
        }),
        help_text="Country code (default: UG for Uganda)"
    )
    
    # Optional: allow manual coordinates
    latitude = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Optional: Enter latitude',
            'step': 'any'
        }),
        help_text="Optional: Manual latitude input"
    )
    
    longitude = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Optional: Enter longitude',
            'step': 'any'
        }),
        help_text="Optional: Manual longitude input"
    )
    
    def clean(self):
        cleaned_data = super().clean()
        city = cleaned_data.get('city')
        latitude = cleaned_data.get('latitude')
        longitude = cleaned_data.get('longitude')
        
        # Ensure either city or coordinates are provided
        if not city and not (latitude and longitude):
            raise ValidationError("Please provide either a city name or coordinates")
        
        # If coordinates are provided, validate they are reasonable
        if latitude is not None:
            if not (-90 <= latitude <= 90):
                raise ValidationError("Latitude must be between -90 and 90")
        
        if longitude is not None:
            if not (-180 <= longitude <= 180):
                raise ValidationError("Longitude must be between -180 and 180")
        
        return cleaned_data

class RecommendationFeedbackForm(forms.ModelForm):
    """
    Form for farmers to provide feedback on recommendations
    """
    class Meta:
        model = Feedback  # Change from RecommendationFeedback to Feedback
        fields = ['rating', 'usefulness', 'treatment_effectiveness', 'comments', 'improvements']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'usefulness': forms.Select(attrs={'class': 'form-control'}),
            'treatment_effectiveness': forms.Select(attrs={'class': 'form-control'}),
            'comments': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your experience with this recommendation...'
            }),
            'improvements': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input'
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes and customize field labels
        self.fields['rating'].label = 'Overall Rating (1-5 stars)'
        self.fields['usefulness'].label = 'How useful was this recommendation?'
        self.fields['treatment_effectiveness'].label = 'Did the treatment work?'
        self.fields['comments'].label = 'Additional Comments'
        self.fields['improvements'].label = 'What could be improved?'
        
        # Make some fields optional
        self.fields['treatment_effectiveness'].required = False
        self.fields['comments'].required = False
        self.fields['improvements'].required = False