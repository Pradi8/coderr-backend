import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from coderr_app.api.serializers import OfferSerializer
from coderr_app.models import Offer


class OfferListView(generics.ListCreateAPIView):
    """
    API endpoint to list all offers.
    - Requires authentication
    - Returns a list of all offers in the system
    """
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated]
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['user__id']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)