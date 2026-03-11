import django_filters
from coderr_app.models import Offer, Review

class OfferFilter(django_filters.FilterSet):

    # createrId = django_filters.NumberFilter(field_name='creater__id')
    creater_id = django_filters.NumberFilter(field_name='user__id')

    # Filter for minimum price
    min_price = django_filters.NumberFilter(field_name='details__price', lookup_expr='lte')

    # Filter for maximum delivery time in days
    max_delivery_time = django_filters.NumberFilter(field_name='details__delivery_time_in_days', lookup_expr='lte')

    # Ordering filter allows sorting by 'updated_at'
    ordering = django_filters.OrderingFilter(fields=(('updated_at', 'updated_at')))

    # Custom search filter to look in title or description
    search = django_filters.CharFilter(method='filter_by_title_or_description')

    class Meta:
        # Model associated with this FilterSet
        model = Offer
        # List of fields for which automatic filters will be generated
        # Empty list because custom filters are defined above
        fields = []

        # -----------------------------
    # Example custom methods:
    # -----------------------------
    def filter_by_title_or_description(self, queryset, name, value):
        """
        Filter offers whose title OR description contains the search term (case-insensitive)
        """
        return queryset.filter(Q(title__icontains=value) | Q(description__icontains=value))
    
class ReviewFilter(django_filters.FilterSet):
    
    # Filter for the business user ID (exact match)
    business_user_id = django_filters.NumberFilter(field_name='business_user__id')

    # Filter for the reviewer ID (exact match)
    reviewer_id = django_filters.NumberFilter(field_name='reviewer__id')

    # Ordering filter allows clients to sort results by rating
    # Use ?ordering=rating for ascending, ?ordering=-rating for descending
    ordering = django_filters.OrderingFilter(fields=(('rating', 'rating')))
    class Meta:
        # Model associated with this FilterSet
        model = Review
        # List of fields for which automatic filters will be generated
        # Empty list because custom filters are defined abov
        fields = []