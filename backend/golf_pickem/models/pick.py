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

from . import (
    UserSeason,
    Tournament,
    Golfer,
    TournamentSeason,
    GolferSeason,
    TournamentGolfer
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
                fields=['user_season', 'tournament'],
                condition=Q(deleted__isnull=True),
                name='unique_user_tournament_season'
            ),
            UniqueConstraint(
                fields=['user_season', 'scored_golfer'],
                condition=Q(deleted__isnull=True),
                name='unique_user_golfer_season'
            )
        ]

    # database info
    id = BigAutoField(primary_key=True, editable=False)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    # related models
    user_season = ForeignKey(UserSeason, on_delete=CASCADE, related_name='pick_history')
    tournament = ForeignKey(Tournament, on_delete=CASCADE, related_name='picks')
    scored_golfer = ForeignKey(Golfer, on_delete=CASCADE, related_name='picked_by_history', blank=True, null=True)
    primary_selection = ForeignKey(Golfer, on_delete=CASCADE, related_name='primary_selections')
    backup_selection = ForeignKey(Golfer, on_delete=CASCADE, related_name='backup_selections')

    @property
    def prize_money(self) -> int:
        """Gets the prize money won by the scored golfer for this pick.
        """
        if self.scored_golfer is None:
            return 0

        tournament_season = TournamentSeason.objects.get(tournament=self.tournament.id, season=self.user_season.season.id)
        golfer_season = GolferSeason.objects.get(golfer=self.scored_golfer.id, season=self.user_season.season.id)
        tournament_golfer = TournamentGolfer.objects.get(tournament_season=tournament_season.id, golfer_season=golfer_season.id)
        return tournament_golfer.prize_money
    
    @property
    def won_tournament(self) -> bool:
        """Gets a boolean value representing whether the scored golfer won the tournament that was picked in.
        """
        if self.scored_golfer is None:
            return False
        
        tournament_season = TournamentSeason.objects.get(tournament=self.tournament.id, season=self.user_season.season.id)
        golfer_season = GolferSeason.objects.get(golfer=self.scored_golfer.id, season=self.user_season.season.id)
        tournament_golfer = TournamentGolfer.objects.get(tournament_season=tournament_season.id, golfer_season=golfer_season.id)
        return tournament_golfer.position == 1