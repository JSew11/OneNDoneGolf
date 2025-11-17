from rest_framework.serializers import ModelSerializer

from ..models import Pick
from ..serializers import UserSeasonSerializer, TournamentSerializer, GolferSerializer

class NewPickSerializer(ModelSerializer):
    """Serializer for the pick model.
    """

    class Meta:
        model = Pick
        exclude = ['created', 'updated', 'deleted']
        read_only_fields = ['id']

class PickSerializer(ModelSerializer):
    """Serializer for the pick model.
    """
    user_season = UserSeasonSerializer(many=False, read_only=True)
    tournament = TournamentSerializer(many=False, read_only=True)
    scored_golfer = GolferSerializer(many=False, read_only=True)

    class Meta:
        model = Pick
        exclude = ['created', 'updated', 'deleted']
        read_only_fields = ['id']