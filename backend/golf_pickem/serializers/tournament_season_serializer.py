from rest_framework.serializers import ModelSerializer

from ..models import TournamentSeason
from ..serializers import TournamentSerializer

class TournamentSeasonSerializer(ModelSerializer):
    """Serializer for the tournament season model.
    """
    tournament = TournamentSerializer(many=False, read_only=True)

    class Meta:
        model = TournamentSeason
        exclude = ['created', 'updated', 'deleted']
        read_only_fields = ['id']