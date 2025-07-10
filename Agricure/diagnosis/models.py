from django.db import models

# Create your models here.
class Diagnosis(models.Model):
    image = models.ImageField(upload_to='diagnosis_images/')
    disease_name = models.CharField(max_length=200)
    severity = models.CharField(max_length=250)
    affected_part = models.CharField(max_length=500)
    confidence = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.disease_name} - {self.severity}"


    