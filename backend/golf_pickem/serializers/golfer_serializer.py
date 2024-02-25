from rest_framework.serializers import ModelSerializer, SerializerMethodField

from core.models import User
from ..models import Golfer

class GolferSerializer(ModelSerializer):
    """Serializer for the golfer model.
    """
    already_picked = SerializerMethodField()

    class Meta:
        model = Golfer
        exclude = ['created', 'updated', 'deleted']
        read_only_fields = ['id', 'already_picked']
    
    def get_already_picked(self, obj: Golfer):
        """Method to tell if a golfer has already been picked by a given user.
        Returns None if no user/season is given.
        """
        user: User = self.context.get('user')
        season_id: int = self.context.get('season_id')
        if user != None and season_id != None:
            return obj in [pick.golfer for pick in user.pick_history_by_season(season_id=season_id)]
        return self.data