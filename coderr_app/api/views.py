from django.shortcuts import get_object_or_404
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from auth_app.api.permissions import IsProfileOwner
from coderr_app.api.serializers import OfferLinkDetailSerializer, OfferSerializer, OfferCreateSerializer, OfferDetailSerializer, OrderSerializer
from coderr_app.models import Offer, OfferDetail, Orders
from coderr_app.api.paginations import StandardResultsSetPagination

class OfferListViewSet(viewsets.ModelViewSet):
    """
    API endpoint to list all offers.
    - Requires authentication
    - Returns a list of all offers in the system
    """
    queryset = Offer.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['user__id']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OfferLinkDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return OfferCreateSerializer
        return OfferSerializer

    
class OfferDetailViewSet(viewsets.ModelViewSet):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticated, IsProfileOwner]

    def retrieve(self, request, pk=None):
        queryset = OfferDetail.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = OfferDetailSerializer(user)
        return Response(serializer.data)
    
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsProfileOwner]

    def retrieve(self, request, pk=None):
        queryset = Orders.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = OrderSerializer(user)
        return Response(serializer.data)