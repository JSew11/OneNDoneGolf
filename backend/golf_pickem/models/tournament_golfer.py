from django.core.exceptions import ValidationError
from django.db.models import (
    UniqueConstraint,
    Q,
    BigAutoField,
    DateTimeField,
    PositiveSmallIntegerField,
    PositiveIntegerField,
    ForeignKey,
    CASCADE,
)
from safedelete.models import SafeDeleteModel
from safedelete import SOFT_DELETE_CASCADE

from . import (
    TournamentSeason,
    GolferSeason
)

class TournamentGolfer(SafeDeleteModel):
    """Model for a golfer playing in a tournament (in a specific season).
    """
    deleted_by_cascade = None # removes this default field from the db table
    _safedelete_policy = SOFT_DELETE_CASCADE
    
    class Meta:
        ordering = ['created']
        verbose_name = 'Tournament'
        verbose_name_plural = 'Tournaments'
        constraints = [
            UniqueConstraint(
                fields=['tournament_season', 'golfer_season'],
                condition=Q(deleted__isnull=True),
                name='unique_tournament_golfer'
            )
        ]

    # database info
    id = BigAutoField(primary_key=True, editable=False)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    # tournament_golfer info
    position = PositiveSmallIntegerField(null=True)
    prize_money = PositiveIntegerField(null=True)

    # related models
    tournament_season = ForeignKey(TournamentSeason, on_delete=CASCADE, related_name='tournaments')
    golfer_season = ForeignKey(GolferSeason, on_delete=CASCADE, related_name='field')

    def clean(self) -> None:
        """Checks to see that the tournament season and golfer season refer to 
        the same season.
        """
        if self.tournament_season.season != self.golfer_season.season:
            raise ValidationError('Seasons must be the same for TournamentSeason and GolferSeason')
        return super().clean()