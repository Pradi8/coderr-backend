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
    
class IsOrderParticipant(BasePermission):
    """
    Custom permission to control access to Order objects.

    Rules:
    1. DELETE requests:
       - Only allow if the requesting user is staff.
    2. Other requests (GET, POST, PUT, PATCH):
       - Allow only if the requesting user is the business user associated with the order.
    """
    def has_object_permission(self, request, view, obj):
        # DELETE requests are restricted to staff users
        if request.method == "DELETE":
            return request.user.is_staff
        # Other actions are allowed only for the business user of the order
        return obj.business_user == request.user