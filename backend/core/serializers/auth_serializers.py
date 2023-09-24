from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenBlacklistSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken

from ..models.user import User

class LoginUserSerializer (TokenObtainPairSerializer):
    """Serializer to log a user into the system.
    """
    username_field = get_user_model().USERNAME_FIELD

class LogoutUserSerializer(TokenBlacklistSerializer):
    """Custom logout serializer to get refresh token from cookies.
    """
    refresh = None
    
    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh_token')
        if attrs['refresh']:
            return super().validate(attrs)
        raise InvalidToken('No valid token found in cookie \'refresh_token\'.')

class RegisterUserSerializer(ModelSerializer):
    """Serializer to register a new user.
    """
    class Meta:
        model = User
        fields = ('id','password','first_name', 'last_name', 'username', 'email')
        extra_kwargs = {
            'password':{'write_only': True},
        }

    def create(self, validated_data: dict) -> User:
        """Method for creating the new user based on the given data.
        """
        user_data = {
            'password': validated_data.pop('password'),
            'username': validated_data.pop('username'),
            'email': validated_data.pop('email'),
        }

        if first_name := validated_data.pop('first_name', None):
            user_data['first_name'] = first_name


        if last_name := validated_data.pop('last_name', None):
            user_data['last_name'] = last_name

        user: User = User.objects.create_user(
            **user_data
        )
        return user

class RefreshTokenSerializer(TokenRefreshSerializer):
    """Custom token refresh serializer to get refresh token from cookies.
    """
    refresh = None

    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh_token')
        if attrs['refresh']:
            return super().validate(attrs)
        raise InvalidToken('No valid token found in cookie \'refresh_token\'.')