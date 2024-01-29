from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token

from core.models import User

class CustomTokenSerializer(TokenObtainPairSerializer):
    """Custom jwt toke serializer to add custom claims to the token.
    """
    @classmethod
    def get_token(cls, user: User) -> Token:
        """Method for getting the token for the given user. Overwritten to add
        custom claims.
        """
        token = super().get_token(user)

        token['username'] = user.username

        return token