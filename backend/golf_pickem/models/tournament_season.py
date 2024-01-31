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

from core.models import User
from . import (
    Tournament,
    Season,
)

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

    def available_golfer_ids(self, user: User):
        """Get the list of golfers who can be picked by the given user.
        """
        pick_history = user.pick_history_by_season(season_id=self.season.id)
        picked_golfer_ids = set([obj['golfer_id'] for obj in pick_history.values('golfer_id').all()])
        field_golfer_ids = [tournament_golfer.golfer_season.golfer.id for tournament_golfer in self.field.all()]
        available_golfer_ids = [golfer_id for golfer_id in field_golfer_ids if golfer_id not in picked_golfer_ids]
        if self.tournament.id in set([obj['tournament_id'] for obj in pick_history.values('tournament_id').all()]):
            available_golfer_ids.append(pick_history.get(tournament_id=self.tournament.id).golfer_id)
        return available_golfer_ids
