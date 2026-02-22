from rest_framework import serializers
from rest_framework.reverse import reverse
from coderr_app.models import Offer, OfferDetail

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

    details = OfferDetailSerializer(many=True)
    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details']

    def create(self, validated_data):
        details_data = validated_data.pop('details', [])
        offer = Offer.objects.create(**validated_data)
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        return offer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")

        if request:
            if request.method == "POST":
                self.fields.pop("user")
                self.fields.pop("created_at")
                self.fields.pop("updated_at")