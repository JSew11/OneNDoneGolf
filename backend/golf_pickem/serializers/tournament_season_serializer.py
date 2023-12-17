from rest_framework.serializers import ModelSerializer

from ..models import TournamentSeason

class TournamentSeasonSerializer(ModelSerializer):
    """Serializer for the tournament season model.
    """

    class Meta:
        model = TournamentSeason
        exclude = ['created', 'updated', 'deleted']
        read_only_fields = ['id']