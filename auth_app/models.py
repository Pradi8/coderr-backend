from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Custom user model that extends Django's built-in AbstractUser.
    This allows us to:
    - Keep all default user fields (username, email, password, etc.)
    - Add additional custom fields
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
    tel = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    working_hours = models.CharField(max_length=255, blank=True)
    created_at = models.DateField(auto_now_add=True)

    def get_upload(self):
        """
        Attempts to retrieve the related FileUpload object for this user.
        Returns:
        FileUpload instance if it exists, otherwise None.
        Explanation:
        - 'self.uploads' uses the reverse relation from the OneToOneField 
          in FileUpload (related_name='uploads').
        - If no related FileUpload exists, Django raises FileUpload.DoesNotExist.
        - We catch that exception and return None to avoid errors.
        """
        try:
            return self.uploads
        except FileUpload.DoesNotExist:
            return None

    def get_file(self):
        """
        Returns the URL of the uploaded file for this user.
        Returns:
        str: URL of the file if it exists, otherwise an empty string.
        Explanation:
        - Calls get_upload() to get the related FileUpload instance.
        - If a FileUpload exists, returns upload.file.url, which is the accessible file URL.
        - If no file exists, returns an empty string as a safe fallback.
        """
        upload = self.get_upload()
        return upload.file.url if upload else ""

    def get_uploaded_at(self):
        """
        Returns the timestamp of when the user's file was uploaded.
        Returns:
        datetime or str: uploaded_at timestamp if a file exists, otherwise an empty string.
    
        Explanation:
        - Calls get_upload() to get the related FileUpload instance.
        - If a FileUpload exists, returns upload.uploaded_at.
        - If no file exists, returns an empty string as a safe fallback.
        """
        upload = self.get_upload()
        return upload.uploaded_at if upload else ""

    def __str__(self):
        return self.username
    
class FileUpload(models.Model):
    """
    File upload model
    This model is used to store uploaded files
    """
    fileowner = models.OneToOneField(CustomUser, related_name='uploads', on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)