from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from ..models.tournament import Tournament

class TournamentSerializer(ModelSerializer):
    """Serializer for the tournament model.
    """
    golfers = PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Tournament
        exclude = ['created', 'updated', 'deleted']
        read_only_fields = ['id']