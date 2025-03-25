from rest_framework.serializers import ModelSerializer

from ..models import TournamentGolfer
from ..serializers import TournamentSeasonSerializer, GolferSeasonSerialier

class TournamentGolferSerializer(ModelSerializer):
    """Serializer for the tournament golfer model.
    """
    tournament_season = TournamentSeasonSerializer(many=False, read_only=True)
    golfer_season = GolferSeasonSerialier(many=False, read_only=True)

    class Meta:
        model = TournamentGolfer
        exclude = ['created', 'updated', 'deleted']
        read_only_fields = ['id']