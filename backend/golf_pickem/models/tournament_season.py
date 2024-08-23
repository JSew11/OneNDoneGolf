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
    UserSeason,
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
    start_date = DateTimeField(blank=True, null=True)
    end_date = DateTimeField(blank=True, null=True)

    # related models
    tournament = ForeignKey(Tournament, on_delete=CASCADE, related_name='seasons')
    season = ForeignKey(Season, on_delete=CASCADE, related_name='schedule')
    
    def user_pick(self, user: User):
        """Returns the given user's pick for the tournament season. Returns none if
        the user has not yet picked.
        """
        user_season: UserSeason = UserSeason.objects.get(user=user.id, season=self.season.id)
        pick_history = user_season.pick_history.all()
        if self.tournament.id in [obj['tournament_id'] for obj in pick_history.values('tournament_id').all()]:
            return pick_history.get(tournament_id=self.tournament.id)
        return None