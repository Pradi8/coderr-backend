from django.shortcuts import get_object_or_404
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from auth_app.api.permissions import IsOrderParticipant, IsProfileOwner
from coderr_app.api.serializers import OfferLinkDetailSerializer, OfferSerializer, OfferCreateSerializer, OfferDetailSerializer, OrderSerializer
from coderr_app.models import Offer, OfferDetail, Orders
from coderr_app.api.paginations import StandardResultsSetPagination

class OfferListViewSet(viewsets.ModelViewSet):
    """d
    API endpoint to list all offers.
    - Requires authentication
    - Returns a list of all offers in the system
    """
    # Base queryset for the ViewSet
    queryset = Offer.objects.all()
    # Permissions: only authenticated users can access
    permission_classes = [IsAuthenticated]
    # Use standard pagination for list results
    pagination_class = StandardResultsSetPagination
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['user__id']

    def perform_create(self, serializer):
        """
        Override the default create behavior.
        Automatically sets the `user` field to the currently authenticated user.
        """
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        """
        Dynamically select the serializer class based on the action:

        - 'retrieve': return detailed link serializer
        - 'create', 'update', 'partial_update': use creation/update serializer
        - default: use standard OfferSerializer
        """
        if self.action == 'retrieve':
            return OfferLinkDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return OfferCreateSerializer
        return OfferSerializer

    
class OfferDetailViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing OfferDetail objects.
    Provides standard CRUD operations.
    Permissions:
        - User must be authenticated
        - User must be the owner of the profile (IsProfileOwner)
    """
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticated, IsProfileOwner]

    def retrieve(self, request, pk=None):
        """
        Retrieve a specific OfferDetail by primary key.
        Overrides the default retrieve to explicitly use get_object_or_404.
        """
        # Get the OfferDetail object by primary key or return 404
        offer_detail = get_object_or_404(self.queryset, pk=pk)
        serializer = OfferDetailSerializer(offer_detail)
        # Return serialized data in the response
        return Response(serializer.data)
    
class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Orders.
    Provides standard CRUD operations.
    Permissions:
        - User must be authenticated
        - User must be a participant of the order (IsOrderParticipant)
    """
    permission_classes = [IsAuthenticated, IsOrderParticipant]
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer

class OrderCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        """
        Returns the number of orders with status 'in_progress'
        for a specific business user.
        """
        # Filter orders belonging to the given business user
        # and with status 'in_progress'
        queryset = Orders.objects.filter(
            business_user_id=business_user_id,
            status="in_progress"
        )

        return Response({'order_count': queryset.count()})
    
class CompleteOrderCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        """
        Returns the number of orders with status 'completed'
        for a specific business user.
        """
        # Filter orders belonging to the given business user
        # and with status 'completed'
        queryset = Orders.objects.filter(
            business_user_id=business_user_id,
            status="completed"
        )
    
        return Response({
            "completed_order_count": queryset.count()
        })