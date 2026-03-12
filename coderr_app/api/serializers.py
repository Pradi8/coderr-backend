from rest_framework import serializers
from rest_framework.reverse import reverse
from django.db.models import Min
from auth_app.models import CustomUser
from coderr_app.models import Offer, OfferDetail, Orders, Review

class OfferLinkDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for Offer objects with a detailed link for related OfferDetail objects.

    Features:
    - Includes basic offer fields: id, user, title, image, description, timestamps
    - Adds a 'details' field containing a list of related OfferDetail objects with their URLs
    """
    # SerializerMethodField allows custom method-based fields
    details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details']

    def get_details(self, obj):
        """
        Custom method to populate the 'details' field.

        For each related OfferDetail:
        - Include the ID
        - Include the API URL for retrieving that detail
        """
        request = self.context.get('request')
        return [
            {
                'id': detail.id,
                'url': reverse('offerdetail-detail', kwargs={'pk': detail.pk}, request=request)
            }
            for detail in obj.details.all()
        ]
class OfferDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for OfferDetail objects.

    Purpose:
    - Serialize OfferDetail fields for API responses
    - Used when returning details of an offer
    """
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']

class OfferSerializer(serializers.ModelSerializer):
    """
    Serializer for Offer objects.

    Purpose:
    - Serialize Offer fields including related OfferDetail objects
    - Provides a 'details' field with URLs for each related OfferDetail
    """
    # Custom field to include links to related OfferDetail objects
    details = serializers.SerializerMethodField()

    # Returns the lowest price among the related offer details
    min_price = serializers.SerializerMethodField()

    # Returns the lowest delivery time among the related offer details

    # Returns the minimum delivery time among the related offer details
    min_delivery_time = serializers.SerializerMethodField()

    # Returns additional information about the user who created the offer
    user_details = serializers.SerializerMethodField()
    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time', 'user_details']

    def get_details(self, obj):
        """
        Returns a list of related OfferDetail objects with their IDs and URLs.

        Args:
            obj (Offer): The Offer instance being serialized

        Returns:
            list: Each entry contains:
                - 'id': primary key of the OfferDetail
                - 'url': absolute URL for the OfferDetail API endpoint
        """
        # Get the request from the serializer context to build absolute URLs
        request = self.context.get('request')
        # Build a list of dictionaries for each related OfferDetail
        return [
            {
                'id': detail.id,
                'url': reverse(
                    'offerdetail-detail',
                    kwargs={'pk': detail.pk},
                    request=request
                )
            }
            for detail in obj.details.all()
        ]
    

    def get_user_details(self, obj):
        """
        Returns details about the user who created the offer.
        """
        request = self.context.get('request')
        return {
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
            'username': obj.user.username,
        }
    
    def get_min_price(self, obj):
        """
        Returns the minimum price among all related OfferDetail objects.
        """
        min_price = obj.details.aggregate(Min('price'))['price__min']
        return min_price

    def get_min_delivery_time(self, obj):
        """
        Returns the minimum delivery time among all related OfferDetail objects.
        """
        min_delivery_time = obj.details.aggregate(Min('delivery_time_in_days'))['delivery_time_in_days__min']
        return min_delivery_time

class OfferCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating Offer objects with nested OfferDetail objects.
    
    Features:
    - Allows creating/updating an Offer along with multiple OfferDetail entries.
    - Nested 'details' field handles multiple OfferDetail objects.
    """
    # Nested serializer for related OfferDetail objects (many=True for multiple)
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']

    def create(self, validated_data):
        """
        Create an Offer and its nested OfferDetail objects.
        """
        # Extract nested details data from the validated data
        details_data = validated_data.pop('details')
        # Create the Offer instance
        offer = Offer.objects.create(**validated_data)
        # Create each OfferDetail and associate with the Offer
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        return offer
    
    def update(self, instance, validated_data):
        """
        Update an Offer and optionally its nested OfferDetail objects.
        """
        # Extract nested details if provided
        details_data = validated_data.pop('details', None)
        # Update Offer fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        # If details are provided, delete existing and recreate
        if details_data is not None:
            instance.details.all().delete()
            for detail_data in details_data:
                OfferDetail.objects.create(offer=instance, **detail_data)
        return instance 
    
class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for Orders.
    
    Features:
    - Links an order to a specific OfferDetail using 'offer_detail_id'.
    - Automatically assigns customer_user from the request.
    - Pulls read-only fields from the related OfferDetail for convenience.
    """
    # Write-only field to select the related OfferDetail
    offer_detail_id = serializers.PrimaryKeyRelatedField(
        queryset=OfferDetail.objects.all(), write_only=True,
        source="offer_detail"   
    )
    # Automatically assigned read-only fields 
    customer_user = serializers.PrimaryKeyRelatedField(read_only=True)
    business_user = serializers.PrimaryKeyRelatedField(read_only=True)

    # Read-only fields from the related OfferDetail
    title = serializers.CharField(source="offer_detail.title", read_only=True)
    revisions = serializers.IntegerField(source="offer_detail.revisions", read_only=True)
    delivery_time_in_days = serializers.IntegerField(source="offer_detail.delivery_time_in_days", read_only=True)
    price = serializers.IntegerField(source="offer_detail.price", read_only=True)
    features = serializers.ListField(source="offer_detail.features", read_only=True)
    offer_type = serializers.CharField(source="offer_detail.offer_type", read_only=True)
    class Meta:
        model = Orders
        fields = [
            'id',
            'offer_detail_id',  # für Request
            'customer_user',
            'business_user',
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type',
            'status',
            'created_at',
            'updated_at'
        ]

    def create(self, validated_data):
        """
        Create a new Order instance.
        Automatically assigns:
        - customer_user from the request
        - business_user from the related OfferDetail's owner
        """
        request = self.context.get("request")
        offer_detail = validated_data.pop("offer_detail")

        return Orders.objects.create(
            offer_detail=offer_detail,
            customer_user=request.user,        
            business_user=offer_detail.offer.user 
        )
    
class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for Review objects.

    Purpose:
    - Serialize Review fields for API responses
    - Used when returning reviews of a business user
    """

    reviewer = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']

    def validate(self, data):
        reviewer = self.context['request'].user
        # In PATCH requests, business_user may be missing, use the existing instance instead
        business_user = data.get("business_user")
        if business_user is None and self.instance is not None:
            business_user = self.instance.business_user

        # Check if the reviewer already has a review for this business
        # In PATCH, exclude the current review instance
        existing_reviews = Review.objects.filter(
            reviewer=reviewer,
            business_user=business_user
        )
        if self.instance:
            existing_reviews = existing_reviews.exclude(pk=self.instance.pk)
        if existing_reviews.exists():
            raise serializers.ValidationError("You have already reviewed this business.")
        return data
        
    def create(self, validated_data):
        """
        Create a new Order instance.
        Automatically assigns:
        - reviewer from the request 
        """
        request = self.context.get("request")

        return Review.objects.create(
            reviewer=request.user,
            **validated_data)