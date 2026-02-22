from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import OfferListViewSet, OfferDetailViewSet


router = DefaultRouter()
router.register(r'offers', OfferListViewSet, basename='offer')
router.register(r'offerdetails', OfferDetailViewSet, basename='offerdetail')

# ------------------------------
# Endpoints
# ------------------------------

urlpatterns = [
    path('', include(router.urls)),
]