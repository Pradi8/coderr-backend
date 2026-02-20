from django.db.models import Q
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsProfileOwner(BasePermission):
    """
    Custom permission to allow users to access only their own profile.
    - Allows safe methods (GET, HEAD, OPTIONS) for any authenticated user
    - For other methods (PUT, PATCH, DELETE), only allows if the user is the owner of the profile
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        return obj == user