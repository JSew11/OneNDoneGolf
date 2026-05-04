from rest_framework.serializers import ModelSerializer, SerializerMethodField

from ..models import TournamentGolfer
from ..serializers import TournamentSeasonSerializer, GolferSeasonSerializer

class TournamentGolferSerializer(ModelSerializer):
    """Serializer for the tournament golfer model.
    """
    tournament_season = TournamentSeasonSerializer(many=False, read_only=True)
    golfer_season = GolferSeasonSerializer(many=False, read_only=True)

    picked = SerializerMethodField()

    class Meta:
        model = TournamentGolfer
        exclude = ['created', 'updated', 'deleted']
        read_only_fields = ['id']

    def get_picked(self, obj: TournamentGolfer):
        """Method to tell if a golfer has already been picked by a given user and
        season.
        Returns None if no user/season is given.
        """
        return obj.golfer_season.golfer in obj.tournament_season.picked_golfers()