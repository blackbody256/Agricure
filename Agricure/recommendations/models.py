from django.db import models
from django.contrib.auth import get_user_model
from diagnosis.models import Diagnosis

User = get_user_model()

class Recommendation(models.Model):
    """
    Model to store AI-generated recommendations for crop diagnoses
    Links to the diagnosis that triggered the recommendation
    """
    # Foreign key to the diagnosis that prompted this recommendation
    diagnosis = models.OneToOneField(
        Diagnosis, 
        on_delete=models.CASCADE,
        related_name='recommendation',
        help_text="The diagnosis this recommendation is based on"
    )
    
    # Location information
    city = models.CharField(
        max_length=100,
        help_text="City where the farm is located"
    )
    latitude = models.FloatField(
        null=True, 
        blank=True,
        help_text="Latitude coordinates of the farm"
    )
    longitude = models.FloatField(
        null=True, 
        blank=True,
        help_text="Longitude coordinates of the farm"
    )
    
    # Environmental data used for recommendation
    temperature = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    pressure = models.FloatField(null=True, blank=True)
    wind_speed = models.FloatField(null=True, blank=True)
    weather_description = models.CharField(max_length=200, null=True, blank=True)
    
    # Soil data used for recommendation
    soil_ph = models.FloatField(null=True, blank=True)
    organic_carbon = models.FloatField(null=True, blank=True)
    soil_nitrogen = models.FloatField(null=True, blank=True)
    soil_phosphorus = models.FloatField(null=True, blank=True)
    soil_potassium = models.FloatField(null=True, blank=True)
    
    # AI-generated recommendation content (stored as JSON)
    recommendation_json = models.TextField(
        help_text="Complete JSON response from Gemini AI"
    )
    
    # Parsed recommendation fields for easy access
    treatment_summary = models.TextField(
        null=True, 
        blank=True,
        help_text="Brief summary of recommended treatments"
    )
    prevention_summary = models.TextField(
        null=True, 
        blank=True,
        help_text="Brief summary of prevention measures"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this recommendation is still relevant"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Recommendation"
        verbose_name_plural = "Recommendations"
    
    def __str__(self):
        return f"Recommendation for {self.diagnosis.disease_name} in {self.city}"
    
    @property
    def is_healthy(self):
        """Check if the diagnosis is for a healthy plant"""
        return self.diagnosis.disease_name.lower() == 'healthy'
    
    @property
    def farmer(self):
        """Get the user who owns this recommendation through diagnosis"""
        # Assuming diagnosis has a user field - you might need to add this
        return getattr(self.diagnosis, 'user', None)

class Feedback(models.Model):
    recommendation = models.ForeignKey(
        Recommendation, 
        on_delete=models.CASCADE, 
        related_name='feedback'
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )
    rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)],
        help_text="Rating from 1 to 5"
    )
    usefulness = models.CharField(
        max_length=50,
        choices=[
            ('very_useful', 'Very Useful'),
            ('somewhat_useful', 'Somewhat Useful'),
            ('not_useful', 'Not Useful'),
        ]
    )
    treatment_effectiveness = models.CharField(
        max_length=50,
        choices=[
            ('completely_effective', 'Completely Effective'),
            ('mostly_effective', 'Mostly Effective'),
            ('partially_effective', 'Partially Effective'),
            ('not_effective', 'Not Effective'),
        ],
        blank=True,
        null=True
    )
    comments = models.TextField(blank=True)
    improvements = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['recommendation', 'user']
        ordering = ['-created_at']
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedback'
    
    def __str__(self):
        return f'Feedback for {self.recommendation.diagnosis.disease_name} - {self.rating}/5 stars'
    
    def get_rating_display(self):
        """Get star rating display"""
        return '⭐' * self.rating
    
    def get_usefulness_color(self):
        """Get color for usefulness display"""
        colors = {
            'very_useful': 'green',
            'somewhat_useful': 'yellow',
            'not_useful': 'red'
        }
        return colors.get(self.usefulness, 'gray')
