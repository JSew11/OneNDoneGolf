from rest_framework.serializers import ModelSerializer, SerializerMethodField

from core.models import User
from ..models import TournamentSeason, Golfer
from ..serializers import TournamentSerializer

class TournamentSeasonSerializer(ModelSerializer):
    """Serializer for the tournament season model.
    """
    tournament = TournamentSerializer(many=False, read_only=True)

    winners = SerializerMethodField()
    winning_golfers = SerializerMethodField()
    place = SerializerMethodField()

    class Meta:
        model = TournamentSeason
        exclude = ['created', 'updated', 'deleted']
        read_only_fields = ['id']
    
    def get_winners(self, obj: TournamentSeason):
        """Gets the usernames of the winning users for the tournament season.
        """
        winning_user_ids = obj.winning_user_ids()
        if winning_user_ids == None:
            return None
        winning_users = [user.username for user in User.objects.filter(id__in=winning_user_ids).all()]
        if len(winning_users) > 0:
            return ', '.join(winning_users)
    
    def get_winning_golfers(self, obj: TournamentSeason):
        """Gets the golfers selected by the winning users for the tournament
        season.
        """
        winning_picked_golfer_ids = obj.winning_picked_golfer_ids()
        if winning_picked_golfer_ids == None:
            return None
        winning_golfers = [golfer.first_name + ' ' + golfer.last_name for golfer in Golfer.objects.filter(id__in=winning_picked_golfer_ids).all()]
        if len(winning_golfers) > 0:
            return ', '.join(winning_golfers)
    
    def get_place(self, obj: TournamentSeason) -> int:
        """Gets the finishing position of the winning users' picks for the
        tournament season.
        """
        place, _ = obj.winning_pick_position()
        if place != None:
            return place