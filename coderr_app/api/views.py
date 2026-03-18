from django.shortcuts import get_object_or_404
from django.db.models import Avg, Min
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from auth_app.api.permissions import IsBusinessUser, IsOrderParticipant, IsProfileOwner, IsReviewParticipant
from auth_app.models import CustomUser
from coderr_app.api.filters import OfferFilter, ReviewFilter
from coderr_app.api.serializers import OfferLinkDetailSerializer, OfferSerializer, OfferCreateSerializer, OfferDetailSerializer, OrderSerializer, ReviewSerializer
from coderr_app.models import Offer, OfferDetail, Orders, Review
from coderr_app.api.paginations import StandardResultsSetPagination

class OfferListViewSet(viewsets.ModelViewSet):
    """
    API endpoint to list all offers.
    - Requires authentication
    - Returns a list of all offers in the system
    """
    # Base queryset for the ViewSet
    queryset = Offer.objects.all().order_by('-created_at')
    # Permissions: only authenticated users can access
    permission_classes = [IsBusinessUser]
    # Use standard pagination for list results
    pagination_class = StandardResultsSetPagination
    # Enables filtering of the queryset using django-filter
    filter_backends = [DjangoFilterBackend]
    # Specifies the FilterSet class that defines available filters for this view
    filterset_class = OfferFilter

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

    def update(self, request, *args, **kwargs):
        # Run DRF's standard update (validates data, updates Offer and nested details)
        super().update(request, *args, **kwargs) 
        # Get the updated Offer object 
        instance = self.get_object()
        # Serialize the full updated Offer, including all nested details
        serializer = OfferCreateSerializer(instance, context={'request': request})
        # Return complete updated data
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        # Use the same logic for PATCH requests
        return self.update(request, *args, **kwargs)
    
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
    # Only authenticated users can access this view
    # and only if they pass the custom 'IsProfileOwner' check
    permission_classes = [IsAuthenticated, IsProfileOwner]
    
class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Orders.
    Provides standard CRUD operations.
    Permissions:
        - User must be authenticated
        - User must be a participant of the order (IsOrderParticipant)
    """
    # Only authenticated users can access this view
    # and only if they pass the custom 'IsOrderParticipant' check
    permission_classes = [IsAuthenticated, IsOrderParticipant]
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer

class OrderCountView(APIView):
    # Only authenticated users can access this view
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
    # Only authenticated users can access this view
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
    
class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Reviews.
    Provides standard CRUD operations.
    Permissions:
        - User must be authenticated
        - User must be the owner of the profile (IsProfileOwner)
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # Only authenticated users can access this view
    # and only if they pass the custom 'IsReviewParticipant' check
    permission_classes = [IsAuthenticated, IsReviewParticipant]
    # Enables filtering of the queryset using django-filter
    filter_backends = [DjangoFilterBackend]
    # Specifies the FilterSet class that defines available filters for this view
    filterset_class = ReviewFilter

class BaseInfoView(APIView):
    """
    API endpoint that returns basic statistics about the platform.
    The endpoint is public and does not require authentication.
    """
    permission_classes = [AllowAny]
    def get(self, request):
        """
        Handles GET requests and returns general platform statistics.
        """
        # Get all reviews that contain a rating
        reviews = Review.objects.filter(rating__isnull=False)
        # Count the number of reviews with a rating
        reviewCount = reviews.count()
        # Calculate the average rating (fallback to 0 if no ratings exist)
        averageRating = reviews.aggregate(average=Avg('rating'))['average'] or 0
        # Count all users with the type "business"
        businessProfiles = CustomUser.objects.filter(type='business').count()
        # Count all available offers
        offers = Offer.objects.count()
        # Return the collected statistics as a JSON response
        return Response({
                "review_count": reviewCount,
                "average_rating": averageRating,
                "business_profile_count": businessProfiles,
                "offer_count": offers
            })