from django.contrib import admin
from .models import CustomUser, FileUpload


admin.site.register(CustomUser)  
admin.site.register(FileUpload)