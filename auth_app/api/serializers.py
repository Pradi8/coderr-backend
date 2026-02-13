from django.contrib.auth import get_user_model
from rest_framework import serializers

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
    - Accepts 'fullname', 'email', 'password', 'repeated_password'
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