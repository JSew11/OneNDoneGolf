from django.db.models import (
    UniqueConstraint,
    Q,
    BigAutoField,
    DateTimeField,
    ForeignKey,
    CASCADE,
)
from safedelete.models import SafeDeleteModel
from safedelete import SOFT_DELETE_CASCADE
from safedelete.queryset import SafeDeleteQueryset

from core.models import User
from .season import Season

class UserSeason(SafeDeleteModel):
    """Model for a user participating in a season.
    """
    deleted_by_cascade = None # removes this default field from the db table
    _safedelete_policy = SOFT_DELETE_CASCADE

    class Meta:
        ordering = ['created']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        constraints = [
            UniqueConstraint(
                fields=['user', 'season'],
                condition=Q(deleted__isnull=True),
                name='unique_user_season'
            )
        ]

    # database info
    id = BigAutoField(primary_key=True, editable=False)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    # related models
    user = ForeignKey(User, on_delete=CASCADE, related_name='golf_pickem_seasons')
    season = ForeignKey(Season, on_delete=CASCADE, related_name='users')

    @property
    def pick_history(self) -> SafeDeleteQueryset:
        """Get a user's pick history for this season.
        """
        return self.user.pick_history.filter(season__id=self.season.id).all()
    
    @property
    def prize_money(self) -> int:
        """Get the total prize money won by a user's picks for this season.
        """
        return sum(pick.prize_money for pick in self.pick_history)
    
    @property
    def tournaments_won(self) -> int:
        """Get the total number of tournaments where the user picked the winner of the tournament
        for this season.
        """
        return sum(pick.won_tournament for pick in self.pick_history)
    