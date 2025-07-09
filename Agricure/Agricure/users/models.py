from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    
    class Roles(models.TextChoices):
        ADMIN='ADMIN', 'Admin'
        FARMER='FARMER', 'Farmer'
        
    role = models.CharField(max_length=50, choices=Roles.choices, default=Roles.FARMER)    
