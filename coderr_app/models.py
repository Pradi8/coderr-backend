from django.db import models
from auth_app.models import CustomUser
class Offer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='offer_images/', blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

class OfferDetail(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="details")
    TYPE_CHOICES = [
        ("basic", "basic"),
        ("standard", "standard"),
        ("premium", "premium"),
    ]
    title = models.CharField(max_length=255)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(blank=True, default=list)
    offer_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="standard")