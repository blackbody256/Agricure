from django.db import models

# Create your models here.

class DatasetUpload(models.Model):
    name = models.CharField(max_length=100)
    zip_file = models.FileField(upload_to='datasets/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
