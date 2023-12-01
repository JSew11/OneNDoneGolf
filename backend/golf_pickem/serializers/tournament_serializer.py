from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from ..models.tournament import Tournament

class TournamentSerializer(ModelSerializer):
    """Serializer for the tournament model.
    """

    class Meta:
        model = Tournament
        exclude = ['created', 'updated', 'deleted']
        read_only_fields = ['id']