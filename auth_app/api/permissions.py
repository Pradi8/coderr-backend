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

class IsBusinessUser(BasePermission):
    """
    Custom permission to control access to Offer endpoints.

    Rules:
    - Anyone can view the list of offers (public access)
    - Only authenticated users can view offer details
    - Only authenticated business users can create offers
    - Only the owner of an offer can update or delete it
    """

    def has_permission(self, request, view):
        """
        General permission check (no object yet).
        This runs BEFORE accessing a specific object.
        """

        if view.action == "list":
            return True

        if view.action == "retrieve":
            return request.user.is_authenticated

        if view.action == "create":
            return (
                request.user.is_authenticated
                and request.user.type == "business"
            )

        if view.action in ["update", "partial_update", "destroy"]:
            return request.user.is_authenticated

        return False

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission check.
        This runs AFTER the object has been retrieved.
        """

        if view.action in ["update", "partial_update", "destroy"]:
            return obj.user == request.user

        return True
class IsOrderParticipant(BasePermission):
    """
    General permission check (object-level permissions are not checked yet).

    This method runs **before accessing a specific object**.
    
    Rules implemented here:
    - Only authenticated users with type 'customer' are allowed to make POST requests.
    - All other request methods (GET, PUT, DELETE, etc.) are allowed for any user.
    """

    def has_permission(self, request, view):
        if request.method == "POST":
            return request.user.is_authenticated and request.user.type == "customer"
        return True

    """
    Custom permission to control access to Order objects.

    Rules:
    1. DELETE requests:
       - Only allow if the requesting user is staff.
    2. Other requests (GET, POST, PUT, PATCH):
       - Allow only if the requesting user is the business user associated with the order.
    """

    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE":
            return request.user.is_staff
        return obj.business_user_id == request.user.id
    
class IsReviewParticipant(BasePermission):
    """
    Custom permission to control access to Review objects.

    Rules:
    1. PATCH, DELETE requests:
       - Only allow if the requesting user is the reviewer associated with the review.
    2. POST requests :
       - Only authenticated users with a customer profile are allowed to create reviews.
    3. GET requests:
         - Allow any authenticated user to view reviews.
     """
    
    def has_permission(self, request, view):
        if request.method == "POST":
            return request.user.is_authenticated and request.user.type == "customer"
        if request.method == "GET":
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in ["PATCH", "DELETE"]:
            return obj.reviewer == request.user
        return True