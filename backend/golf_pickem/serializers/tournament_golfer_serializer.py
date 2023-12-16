from rest_framework.serializers import ModelSerializer

from ..models import TournamentGolfer

class TournamentGolferSerializer(ModelSerializer):
    """Serializer for the tournament golfer model.
    """

    class Meta:
        model = TournamentGolfer
        exclude = ['created', 'updated', 'deleted']
        read_only_fields = ['id']