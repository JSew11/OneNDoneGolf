from django.db.models import (
    UniqueConstraint,
    Q,
    BigAutoField,
    DateTimeField,
    ForeignKey,
    CASCADE,
)
from safedelete.models import SafeDeleteModel
from safedelete import SOFT_DELETE

from core.models import User
from . import (
    Season,
    Tournament,
    Golfer
)

class Pick(SafeDeleteModel):
    """Model for a user's pick.

    A user can only pick a golfer once per season.
    A user can only make one pick per tournament per season.
    """

    deleted_by_cascade = None # removes this default field from the db table
    _safedelete_policy = SOFT_DELETE

    class Meta:
        ordering = ['created']
        verbose_name = 'Picks'
        verbose_name_plural = 'Picks'
        constraints = [
            UniqueConstraint(
                fields=['user', 'tournament', 'season'],
                condition=Q(deleted__isnull=True),
                name='unique_user_tournament_season'
            ),
            UniqueConstraint(
                fields=['user', 'scored_golfer', 'season'],
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
    season = ForeignKey(Season, on_delete=CASCADE, related_name='pick_history')
    tournament = ForeignKey(Tournament, on_delete=CASCADE, related_name='picks')
    scored_golfer = ForeignKey(Golfer, on_delete=CASCADE, related_name='picked_by_history', blank=True, null=True)
    primary_selection = ForeignKey(Golfer, on_delete=CASCADE, related_name='primary_selections')
    backup_selection = ForeignKey(Golfer, on_delete=CASCADE, related_name='backup_selections')