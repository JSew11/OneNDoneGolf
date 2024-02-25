from rest_framework.serializers import ModelSerializer, SerializerMethodField

from core.models import User
from ..models import Golfer

class GolferSerializer(ModelSerializer):
    """Serializer for the golfer model.
    """
    already_picked = SerializerMethodField()
    tournament_picked_in = SerializerMethodField()

    class Meta:
        model = Golfer
        exclude = ['created', 'updated', 'deleted']
        read_only_fields = ['id']
    
    def get_already_picked(self, obj: Golfer):
        """Method to tell if a golfer has already been picked by a given user and
        season.
        Returns None if no user/season is given.
        """
        user: User = self.context.get('user')
        season_id: int = self.context.get('season_id')
        if user != None and season_id != None:
            return obj in [pick.golfer for pick in user.pick_history_by_season(season_id=season_id)]
        return None
    
    def get_tournament_picked_in(self, obj: Golfer):
        """Method to get the tournament the golfer was already picked in for the
        given user and season.
        Returns None if no user/season is given.
        """
        user: User = self.context.get('user')
        season_id: int = self.context.get('season_id')
        if user != None and season_id != None:
            pick = user.pick_history_by_season(season_id=season_id).filter(golfer=obj.id).first()
            return pick.tournament.alias if pick else None
        return None
