from django.contrib import admin
from .models import CustomUser


admin.site.register(CustomUser)


# Superuser
# Username: admin
# Password: admin1234