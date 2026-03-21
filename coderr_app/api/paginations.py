from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    """
    Custom pagination class for API endpoints.

    Features:
    - Default page size: 6 items per page
    - Allows clients to specify a custom page size via 'page_size' query parameter
    - Maximum page size allowed: 100 items
    """
    
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 100