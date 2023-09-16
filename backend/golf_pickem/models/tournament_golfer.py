from django.db.models import (
    UniqueConstraint,
    Q,
    BigAutoField,
    DateTimeField,
    SmallIntegerField,
    PositiveIntegerField,
    ForeignKey,
    CASCADE
)
from safedelete.models import SafeDeleteModel
from safedelete import SOFT_DELETE

from .golfer import Golfer
from .tournament import Tournament

class TournamentGolfer(SafeDeleteModel):
    """Model for a golfer participating in a tournament.
    """

    deleted_by_cascade = None # removes this default field from the db table
    _safedelete_policy = SOFT_DELETE

    class Meta:
        ordering = ['created']
        verbose_name = 'Tournament Golfer'
        verbose_name_plural = 'Tournament Golfers'
        constraints = [
            UniqueConstraint(
                fields=['tournament', 'golfer'],
                condition=Q(deleted__isnull=True),
                name='unique_active_tournament_golfer'
            )
        ]

    # database info
    id = BigAutoField(primary_key=True, editable=False)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    # tournament golfer info
    place = SmallIntegerField()
    prize_money_won = PositiveIntegerField()

    # related models
    tournament = ForeignKey(Tournament, on_delete=CASCADE, related_name='golfers')
    golfer = ForeignKey(Golfer, on_delete=CASCADE, related_name='tournaments')
    