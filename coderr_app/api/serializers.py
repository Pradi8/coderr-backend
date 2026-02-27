from rest_framework import serializers
from rest_framework.reverse import reverse
from django.db import models
from auth_app.models import CustomUser
from coderr_app.models import Offer, OfferDetail, Orders

class OfferLinkDetailSerializer(serializers.ModelSerializer):

    details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details']

    def get_details(self, obj):
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
    Serializer for Offer model
    - Used to serialize offer data
    """

    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']

class OfferSerializer(serializers.ModelSerializer):
    """
    Serializer for Offer model
    - Used to serialize offer data
    """

    details = serializers.SerializerMethodField()
    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details']

    def get_details(self, obj):
        request = self.context.get('request')
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

class OfferCreateSerializer(serializers.ModelSerializer):
    
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        offer = Offer.objects.create(**validated_data)
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        return offer
    
    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if details_data is not None:
            instance.details.all().delete()
            for detail_data in details_data:
                OfferDetail.objects.create(offer=instance, **detail_data)
        return instance 
    
class OrderSerializer(serializers.ModelSerializer):

    offer_detail_id = serializers.PrimaryKeyRelatedField(
        queryset=OfferDetail.objects.all(), write_only=True,
        source="offer_detail"   # 👈 wichtig!
    ) 
    customer_user = serializers.PrimaryKeyRelatedField(read_only=True)
    business_user = serializers.PrimaryKeyRelatedField(read_only=True)
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
        request = self.context.get("request")
        offer_detail = validated_data.pop("offer_detail")

        return Orders.objects.create(
            offer_detail=offer_detail,
            customer_user=request.user,          # automatisch vom eingeloggten User
            business_user=offer_detail.offer.user  # automatisch vom zugehörigen Offer
        )