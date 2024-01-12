from rest_framework.serializers import ModelSerializer

from ..models import Tournament

class TournamentSerializer(ModelSerializer):
    """Serializer for the tournament model.
    """

    class Meta:
        model = Tournament
        exclude = ['created', 'updated', 'deleted']
        read_only_fields = ['id']