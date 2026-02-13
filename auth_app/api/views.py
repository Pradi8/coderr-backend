from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from .serializers import RegisterationSerializer

class RegisterView(APIView):
    """
    API endpoint for user registration.
    - Allows any user (no authentication required)
    - Accepts POST request with: fullname, email, password, repeated_password
    - Returns token and user info on successful registration
    """
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterationSerializer(data=request.data)
        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)
            data = {
                'token' : token.key,
                'username': saved_account.username,
                'email' : saved_account.email,
                'user_id': saved_account.pk,
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)