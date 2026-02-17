from rest_framework.serializers import ModelSerializer, SerializerMethodField

from ..models import GolferSeason
from ..serializers import GolferSerializer

class GolferSeasonSerializer(ModelSerializer):
    """Serializer for the golfer season model.
    """
    golfer = GolferSerializer(many=False, read_only=True)

    times_picked = SerializerMethodField()
    times_picked_as_winner = SerializerMethodField()
    remaining_available_picks = SerializerMethodField()

    class Meta:
        model = GolferSeason
        exclude = ['created', 'updated', 'deleted']
        read_only_fields = ['id']
    
    def get_times_picked(self, obj: GolferSeason) -> int:
        """Returns the number of times the model's golfer was picked in the
        model's season.
        """
        return obj.golfer.times_picked(obj.season.id)
    
    def get_remaining_available_picks(self, obj: GolferSeason) -> int:
        """Returns the number of users have not picked the model's golfer
        in the model's season.
        """
        return obj.golfer.remaining_available_picks(obj.season.id)
    
    def get_times_picked_as_winner (self, obj: GolferSeason) -> int:
        """Returns the number of times the model's golfer was picked and won
        the tournament in the model's season.
        """
        return obj.golfer.times_picked_as_winner(obj.season.id)