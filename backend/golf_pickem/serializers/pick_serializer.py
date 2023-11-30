from rest_framework.serializers import ModelSerializer

from core.models.user import User
from ..models.pick import Pick
from ..models.tournament_golfer import TournamentGolfer

class PickSerializer(ModelSerializer):
    """Serializer for the pick model.
    """

    class Meta:
        model = Pick
        exclude = ['created', 'updated', 'deleted']
        read_only_fields = ['id']

    def create(self, validated_data):
        """Overwritten create method to work with the custom PickManager class.
        """
        user: User = validated_data['user']
        tournament_golfer: TournamentGolfer = validated_data['tournament_golfer']
        return Pick.objects.create(user_id=user.id, tournament_golfer_id=tournament_golfer.id)