from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):

    TYPE_CHOICES = [
        ("customer", "customer"),
        ("business", "business"),
    ]

    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="customer")