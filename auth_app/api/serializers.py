from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from auth_app.models import FileUpload

User = get_user_model()

def validate_registration_data(data):
    """
    Validate registration input data.
    - Ensure that 'password' and 'repeated_password' match
    - Ensure the email is unique in the system
    """
    if data['password'] != data['repeated_password']:
        raise serializers.ValidationError({'password': 'Passwords do not match'})
    if User.objects.filter(email=data['email']).exists():
        raise serializers.ValidationError({'email': 'Email already exists'})
    return data


class RegisterationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    - Accepts 'username', 'email', 'password', 'repeated_password', and 'type' fields
    - Validates input data and creates a new user
    """
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'repeated_password', 'type']
        extra_kwargs = {
            'password' :  {
                'write_only' : True
            }
        }

    def validate(self, data):
        return validate_registration_data(data)
    
    def create(self, validated_data):
        validated_data.pop('repeated_password')
        return User.objects.create_user(**validated_data)
    
class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    - Accepts 'email' and 'password'
    - Validates credentials and authenticates the user
    """
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True)
    def validate(self, data):
        """
        Validate user login credentials.
        - Raise ValidationError if email does not exist
        - Raise ValidationError if password is incorrect
        - Add the authenticated user object to data['user']
        """
        username = data.get('username')
        password = data.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("Ungültige E-mail")
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Passwort ist falsch")
        data['user'] = user
        return data

class FileSerializer(serializers.ModelSerializer):
    """
    Serializer for FileUpload model
    - Used to serialize file upload data
    """
    class Meta:
        model = FileUpload
        fields = ['file', 'uploaded_at']
    
class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for CustomUser model
    """
    # Expose the user's ID as "user" in the API response
    user = serializers.IntegerField(source='id', read_only=True)
    # Exposes the URL of the user's uploaded file
    # Read-only because this is a computed value from the related FileUpload model
    file = serializers.ReadOnlyField(source="get_file")
    class Meta:
        model = User
        fields = [
            'user', 
            'username', 
            'first_name', 
            'last_name', 
            'file',
            'location', 
            'tel', 
            'description', 
            'working_hours', 
            'email', 
            'type', 
            'created_at'
        ]
    
class BusinessProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for Business profile.
    - Includes fields relevant to business profiles
    """
    # Expose the user's ID as "user" in the API response
    user = serializers.IntegerField(source='id', read_only=True)
    # Exposes the URL of the user's uploaded file
    # Read-only because this is a computed value from the related FileUpload model
    file = serializers.ReadOnlyField(source="get_file")
    class Meta:
        model = User
        fields = [ 
            'user',
            'username',
            'first_name', 
            'last_name', 
            'file',
            'location', 
            'tel', 
            'description', 
            'working_hours', 
            'type'
        ]

class CustomerProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for Customer profile.
    - Includes fields relevant to customer profiles
    """
    # Expose the user's ID as "user" in the API response
    user = serializers.IntegerField(source='id', read_only=True)
    # Exposes the URL of the user's uploaded file
    # Read-only because this is a computed value from the related FileUpload model
    file = serializers.ReadOnlyField(source="get_file")
    # Exposes the timestamp when the user's file was uploaded
    # Read-only because it comes from the related FileUpload model
    uploaded_at = serializers.ReadOnlyField(source="get_uploaded_at")
    class Meta:
        model = User
        fields = [ 
            'user',
            'username',
            'first_name', 
            'last_name', 
            'file',
            'uploaded_at',
            'type'
        ]