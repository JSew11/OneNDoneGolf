from django.db.models import (
    BigAutoField,
    DateTimeField,
    CharField,
)
from django.core.validators import RegexValidator
from safedelete.models import SafeDeleteModel
from safedelete import SOFT_DELETE_CASCADE

from golf_pickem.models import UserSeason

class Golfer(SafeDeleteModel):
    """Model for a golfer.
    """
    deleted_by_cascade = None # removes this default field from the db table
    _safedelete_policy = SOFT_DELETE_CASCADE

    class Meta:
        ordering = ['created']
        verbose_name = 'Golfer'
        verbose_name_plural = 'Golfers'

    # database info
    id = BigAutoField(primary_key=True, editable=False)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    # golfer info
    first_name = CharField(max_length=255, validators=[RegexValidator(r'^[a-zA-Z]+$')])
    last_name = CharField(max_length=255, validators=[RegexValidator(r'^[a-zA-Z .]+$')])
    external_id = CharField(max_length=16) # id used in external api calls

    def times_picked(self, seasonId: int) -> int:
        """Get the number of times the golfer was picked in the given 
        season.
        """
        return self.picked_by_history.filter(user_season__season=seasonId).count()
    
    def times_picked_as_winner(self, seasonId: int) -> int:
        """Get the number of times the golfer was picked and won the
        tournament in the given season.
        """
        return len([pick for pick in self.picked_by_history.filter(user_season__season=seasonId).all() if pick.won_tournament])
    
    def remaining_available_picks(self, seasonId: int) -> int:
        """Get the number of users who have not picked the golfer in the
        given season.
        """
        return UserSeason.objects.filter(season=seasonId).count() - self.times_picked(seasonId)

    @staticmethod
    def create_from_external_data(external_api_data: dict) -> Golfer:
        """Creates a Golfer model from external api data taken from json.
        """
        return Golfer.objects.create(
            first_name=external_api_data['firstName'],
            last_name=external_api_data['lastName'],
            external_id=external_api_data['playerId']
        )