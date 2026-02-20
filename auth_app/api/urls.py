from django.urls import path
from .views import RegisterView, UserLoginView, LogoutView, ProfileDetailView, BusinesView, CustomerView

# ------------------------------
# Endpoints
# ------------------------------

urlpatterns = [
    path('registration/', RegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='get-profile-detail'),
    path('profiles/business/', BusinesView.as_view(), name='get-business-profile'),
    path('profiles/customer/', CustomerView.as_view(), name='get-customer-profile'),
]