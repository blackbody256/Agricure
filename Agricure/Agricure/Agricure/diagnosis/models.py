# from django.db import models
# from django.conf import settings

# # Create your models here.
# class Diagnosis(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Add this line
#     image = models.ImageField(upload_to='diagnosis_images/')
#     disease_name = models.CharField(max_length=100, blank=True)
#     severity = models.CharField(max_length=50, blank=True)
#     affected_part = models.CharField(max_length=100, blank=True)
#     confidence = models.FloatField(default=0.0)
#     timestamp = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return f"{self.disease_name} - {self.confidence}%"



from django.db import models
from django.conf import settings

# Create your models here.
class Diagnosis(models.Model):
    # Add user field if it doesn't exist
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='diagnoses',
        null=True,  # Allow null for existing records
        blank=True
    )
    
    image = models.ImageField(upload_to='diagnosis_images/')
    disease_name = models.CharField(max_length=200)
    severity = models.CharField(max_length=250)
    affected_part = models.CharField(max_length=500)
    confidence = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Add location context for better recommendations
    location_context = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text="Optional location context for this diagnosis"
    )
    
    def __str__(self):
        return f"{self.disease_name} - {self.severity}"
    
    @property
    def has_recommendation(self):
        """Check if this diagnosis has a recommendation"""
        return hasattr(self, 'recommendation')



