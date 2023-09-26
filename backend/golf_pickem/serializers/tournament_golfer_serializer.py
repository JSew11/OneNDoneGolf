from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from ..models.tournament_golfer import TournamentGolfer

class TournamentGolferSerializer(ModelSerializer):
    """Serializer for the tournament golfer model.
    """
    picked_by = PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = TournamentGolfer
        exclude = ['created', 'updated', 'deleted']
        read_only_fields = ['id']