from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import BaseInfoView, CompleteOrderCountView, OfferListViewSet, OfferDetailViewSet, OrderCountView, OrderViewSet, ReviewViewSet


router = DefaultRouter()
router.register(r'offers', OfferListViewSet, basename='offer')
router.register(r'offerdetails', OfferDetailViewSet, basename='offerdetail')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'reviews', ReviewViewSet, basename='review')

# ------------------------------
# Endpoints
# ------------------------------

urlpatterns = [
    path('', include(router.urls)),
    path('order-count/<int:business_user_id>/', OrderCountView.as_view(), name='order-count'),
    path('completed-order-count/<int:business_user_id>/', CompleteOrderCountView.as_view(), name='completed-order-count'),
    path('base-info/', BaseInfoView.as_view(), name='base-info')
]