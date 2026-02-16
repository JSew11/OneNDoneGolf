from rest_framework.serializers import ModelSerializer, SerializerMethodField

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

    position = SerializerMethodField()
    prize_money = SerializerMethodField()

    class Meta:
        model = Pick
        exclude = ['created', 'updated', 'deleted']
        read_only_fields = ['id']
    
    def get_position(self, obj: Pick) -> int:
        """Gets the finishing place of the scored golfer.
        """
        if (tournament_golfer := obj.scored_tournament_golfer()):
            return tournament_golfer.position
        return None
    
    def get_prize_money(self, obj: Pick) -> int:
        """Gets the amount of prize money won by the scored golfer.
        """
        if (tournament_golfer := obj.scored_tournament_golfer()):
            return tournament_golfer.prize_money
        return None