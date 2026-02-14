from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Custom user model that extends Django's built-in AbstractUser.
    This allows us to:
    - Keep all default user fields (username, email, password, etc.)
    - Add additional custom fields (in this case: 'type')
    """
    # Defines the possible user types.
    # (value_stored_in_database, human_readable_display_name)
    TYPE_CHOICES = [
        ("customer", "customer"),
        ("business", "business"),
    ]
    # New field that specifies the type of user.
    # Choices restricts the allowed values to TYPE_CHOICES.
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="customer")