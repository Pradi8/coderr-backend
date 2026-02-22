from django.shortcuts import get_object_or_404
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from coderr_app.api.serializers import OfferLinkDetailSerializer, OfferSerializer
from coderr_app.models import Offer, OfferDetail
from coderr_app.api.paginations import StandardResultsSetPagination

class OfferListViewSet(viewsets.ModelViewSet):
    """
    API endpoint to list all offers.
    - Requires authentication
    - Returns a list of all offers in the system
    """
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['user__id']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OfferLinkDetailSerializer  # Detail-View
        return OfferSerializer  # List-View
    
class OfferDetailViewSet(viewsets.ModelViewSet):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated]