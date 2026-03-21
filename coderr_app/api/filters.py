from django import forms
import django_filters
from django.db.models import Q
from coderr_app.models import Offer, Review

class OfferFilter(django_filters.FilterSet):
    '''
    FilterSet for the Offer model that provides various filtering options.
    It uses Django Filter to build query parameters that can be applied
    to a queryset, typically in a Django REST Framework API.
    '''
    creater_id = django_filters.NumberFilter(field_name='user__id')
    min_price = django_filters.NumberFilter(field_name='details__price', lookup_expr='gte')
    max_delivery_time = django_filters.NumberFilter(field_name='details__delivery_time_in_days', lookup_expr='lte')
    ordering = django_filters.OrderingFilter(fields=(('updated_at', 'updated_at')))
    search = django_filters.CharFilter(method='filter_by_title_or_description')

    class Meta:
        model = Offer
        fields = []


    def filter_by_title_or_description(self, queryset, name, value):
        """
        Filter offers whose title OR description contains the search term (case-insensitive)
        """
        return queryset.filter(Q(title__icontains=value) | Q(description__icontains=value))
    
    def filter_min_price(self, queryset, name, value):
        
        return queryset.filter(details__price__gte=value).distinct()
    
class ReviewFilter(django_filters.FilterSet):
    '''
    FilterSet for the Review model that provides various filtering options.
    '''
    business_user_id = django_filters.NumberFilter(field_name='business_user__id')
    reviewer_id = django_filters.NumberFilter(field_name='reviewer__id')
    ordering = django_filters.OrderingFilter(fields=(('rating', 'rating')))
    class Meta:
        model = Review
        fields = []