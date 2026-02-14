from django.db import models

class Profile(models.Model):
    user = models.OneToOneField('auth_app.CustomUser', on_delete=models.CASCADE, related_name='profile')
    file = models.FileField(upload_to='uploads/')
    location = models.CharField(max_length=255)
    tel = models.IntegerField()
    description = models.TextField()
    working_hours = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username