from django.core.exceptions import ValidationError
from django.db.models import (
    UniqueConstraint,
    Q,
    BigAutoField,
    DateTimeField,
    ForeignKey,
    CASCADE,
)
from safedelete.models import SafeDeleteModel
from safedelete.managers import SafeDeleteManager
from safedelete import SOFT_DELETE, DELETED_VISIBLE_BY_PK

from core.models import User
from . import (
    TournamentSeason,
    GolferSeason
)

class Pick(SafeDeleteModel):
    """Model for a user's pick.

    A user can only pick a golfer once per year.
    """

    deleted_by_cascade = None # removes this default field from the db table
    _safedelete_policy = SOFT_DELETE

    class Meta:
        ordering = ['created']
        verbose_name = 'Picks'
        verbose_name_plural = 'Picks'
        constraints = [
            UniqueConstraint(
                fields=['user', 'tournament_season'],
                condition=Q(deleted__isnull=True),
                name='unique_user_tournament_season'
            ),
            UniqueConstraint(
                fields=['user', 'golfer_season'],
                condition=Q(deleted__isnull=True),
                name='unique_user_golfer_season'
            )
        ]

    # database info
    id = BigAutoField(primary_key=True, editable=False)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    # related models
    user = ForeignKey(User, on_delete=CASCADE, related_name='pick_history')
    tournament_season = ForeignKey(TournamentSeason, on_delete=CASCADE, related_name='picks')
    golfer_season = ForeignKey(GolferSeason, on_delete=CASCADE, related_name='picked_by_history')

    def clean(self) -> None:
        """Checks to see that the tournament season and golfer season refer to 
        the same season.
        """
        if self.tournament_season.season != self.golfer_season.season:
            raise ValidationError('Seasons must be the same for TournamentSeason and GolferSeason')
        return super().clean()