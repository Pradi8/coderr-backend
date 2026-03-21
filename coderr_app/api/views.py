from django.shortcuts import get_object_or_404
from django.db.models import Avg, Min
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
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
    
    queryset = Offer.objects.all().order_by('-created_at')
    permission_classes = [IsBusinessUser]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
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
        super().update(request, *args, **kwargs)  
        instance = self.get_object()
        serializer = OfferCreateSerializer(instance, context={'request': request})
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
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
    permission_classes = [IsAuthenticated, IsProfileOwner]
    
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
        
        business_user = get_object_or_404(CustomUser, id=business_user_id, type="business")

        order_count = Orders.objects.filter(
            business_user=business_user,
            status="in_progress"
        ).count()

        return Response({'order_count': order_count})
    
class CompleteOrderCountView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        """
        Returns the number of orders with status 'completed'
        for a specific business user.
        """
        
        business_user = get_object_or_404(CustomUser, id=business_user_id, type="business")

        completed_order_count = Orders.objects.filter(
            business_user_id=business_user_id,
            status="completed"
        ).count()
    
        return Response({
            "completed_order_count": completed_order_count
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
    permission_classes = [IsAuthenticated, IsReviewParticipant]
    filter_backends = [DjangoFilterBackend]
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
        
        reviews = Review.objects.filter(rating__isnull=False)
        reviewCount = reviews.count()
        averageRating = reviews.aggregate(average=Avg('rating'))['average'] or 0
        businessProfiles = CustomUser.objects.filter(type='business').count()
        offers = Offer.objects.count()
        
        return Response({
                "review_count": reviewCount,
                "average_rating": averageRating,
                "business_profile_count": businessProfiles,
                "offer_count": offers
            })