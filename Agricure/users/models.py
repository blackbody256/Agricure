from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('FARMER', 'Farmer'),
        ('ADMIN', 'Admin'),
        ('AGRONOMIST', 'Agronomist')
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='FARMER')
    
    def save(self, *args, **kwargs):
        # Check if trying to create/update to admin role
        if self.role == 'ADMIN':
            existing_admins = User.objects.filter(role='ADMIN').exclude(pk=self.pk).count()
            if existing_admins >= 1:
                raise ValidationError("Only one admin is allowed in the system.")
        super().save(*args, **kwargs)
