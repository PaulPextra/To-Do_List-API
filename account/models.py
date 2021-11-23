from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """Extending our user model"""
    address = models.TextField(null=True, blank=True)