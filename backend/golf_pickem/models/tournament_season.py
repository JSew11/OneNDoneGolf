from django.db.models import (
    UniqueConstraint,
    Q,
    BigAutoField,
    DateTimeField,
    PositiveIntegerField,
    ForeignKey,
    CASCADE
)
from safedelete.models import SafeDeleteModel
from safedelete import SOFT_DELETE_CASCADE

from .tournament import Tournament
from .season import Season

class TournamentSeason(SafeDeleteModel):
    """Model for a tournament taking part in a season.
    """
    deleted_by_cascade = None # removes this default field from the db table
    _safedelete_policy = SOFT_DELETE_CASCADE

    class Meta:
        ordering = ['created']
        verbose_name = 'Tournament'
        verbose_name_plural = 'Tournaments'
        constraints = [
            UniqueConstraint(
                fields=['tournament', 'season'],
                condition=Q(deleted__isnull=True),
                name='unique_tournament_season'
            )
        ]

    # database info
    id = BigAutoField(primary_key=True, editable=False)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    # tournament season info
    purse = PositiveIntegerField()

    # related models
    tournament = ForeignKey(Tournament, on_delete=CASCADE, related_name='seasons')
    season = ForeignKey(Season, on_delete=CASCADE, related_name='schedule')