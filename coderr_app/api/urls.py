from django.urls import path
from .views import OfferListView

# ------------------------------
# Endpoints
# ------------------------------

urlpatterns = [
    path('offers/', OfferListView.as_view(), name='offers-list'),
]