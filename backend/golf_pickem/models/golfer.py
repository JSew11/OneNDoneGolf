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
    country = CharField(max_length=255, validators=[RegexValidator(r'^[a-zA-Z .,]+$')])

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