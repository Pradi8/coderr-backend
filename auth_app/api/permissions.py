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

        # Public access to list endpoint
        if view.action == "list":
            return True

        # Only authenticated users can access detail view
        if view.action == "retrieve":
            return request.user.is_authenticated

        # Only authenticated business users can create offers
        if view.action == "create":
            return (
                request.user.is_authenticated
                and request.user.type == "business"
            )

        # Update/Delete requires authentication (ownership checked later)
        if view.action in ["update", "partial_update", "destroy"]:
            return request.user.is_authenticated

        #  Everything else by default
        return False

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission check.
        This runs AFTER the object has been retrieved.
        """

        # Only the owner of the offer can update or delete it
        if view.action in ["update", "partial_update", "destroy"]:
            return obj.user == request.user

        # Allow access in all other cases
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
        # POST requests: Only allow if user is authenticated AND type is 'customer'
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
        # DELETE requests are restricted to staff users
        if request.method == "DELETE":
            return request.user.is_staff
        # Other actions are allowed only for the business user of the order
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
        # POST requests are allowed only for authenticated users with a customer profile
        if request.method == "POST":
            return request.user.is_authenticated and request.user.type == "customer"
        # GET requests are allowed for any authenticated user
        if request.method == "GET":
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        # PATCH and DELETE requests are restricted to the reviewer of the review
        if request.method in ["PATCH", "DELETE"]:
            return obj.reviewer == request.user
        return True
    