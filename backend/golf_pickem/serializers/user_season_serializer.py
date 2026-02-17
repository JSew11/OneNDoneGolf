from rest_framework.serializers import (
    ModelSerializer,
    ReadOnlyField,
    SerializerMethodField,
)

from core.models import User
from core.serializers import UserSerializer
from ..models import UserSeason
from ..serializers import SeasonSerializer

class NewUserSeasonSerializer(ModelSerializer):
    """Serializer for creating user seasons.
    """

    class Meta:
        model = UserSeason
        exclude = ['created', 'updated', 'deleted']
        read_only_fields = ['id']

class UserSeasonSerializer(ModelSerializer):
    """Serializer for the user season model.
    """
    user = UserSerializer(many=False, read_only=True)
    season = SeasonSerializer(many=False, read_only=True)

    prize_money = ReadOnlyField()
    tournaments_won = ReadOnlyField()

    class Meta:
        model = UserSeason
        exclude = ['created', 'updated', 'deleted']
        read_only_fields = ['id']