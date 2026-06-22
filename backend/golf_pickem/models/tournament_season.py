from datetime import (
  datetime,
  timezone
)
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
    UserSeason,)

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
    
    def winning_pick_position(self):
        """Get the highest finishing position of the picked golfers for this tournament
        season and the positions of each user pick.
        """
        if self.end_date > datetime.now(timezone.utc):
            return -1, []
        
        users = [season_user.user for season_user in UserSeason.objects.filter(season=self.season_id).all()]
        picks = [self.user_pick(user) for user in users if self.user_pick(user) is not None]
        pick_user_positions = [(pick.user_season.user.id, pick.scored_tournament_golfer().position) for pick in picks if pick.scored_golfer != None]

        if (pick_user_positions != None and len(pick_user_positions) > 0):
            return min(pick_user_positions, key=lambda x: 9999999 if x[1] is None else x[1])[1], pick_user_positions
    
        return -1, []
    
    def winning_user_ids(self):
        """Get the user ids of the winner(s) of this tournament season. Returns none
        if the tournament has not yet finished.
        """
        if self.end_date > datetime.now(timezone.utc):
            return []
        
        highest_position, pick_user_positions = self.winning_pick_position()
        if (highest_position != None and pick_user_positions != None):
            return [obj[0] for obj in filter(lambda x: x[1] == highest_position, pick_user_positions)]
        
    def user_pick(self, user: User):
        """Returns the given user's pick for the tournament season. Returns none if
        the user has not yet picked.
        """
        user_season: UserSeason = UserSeason.objects.get(user=user.id, season=self.season.id)
        pick_history = user_season.pick_history.all()
        if self.tournament.id in [obj['tournament_id'] for obj in pick_history.values('tournament_id').all()]:
            return pick_history.get(tournament_id=self.tournament.id)
        return None
    
    def picked_golfers(self):
        """Returns a list of all golfers that were picked for this tournament season.
        """
        users = [season_user.user for season_user in UserSeason.objects.filter(season=self.season_id).all()]
        return [self.user_pick(user).scored_golfer for user in users if self.user_pick(user) is not None]
    
    def finish_tournament_season(self) -> None:
        """Scores all picks for the current tournament season.
        """
        # TODO - make sure external API has obtained all final tournament data before scoring picks
        
        users = [season_user.user for season_user in UserSeason.objects.filter(season=self.season_id).all()]
        picks = [self.user_pick(user) for user in users if self.user_pick(user) is not None]
        for pick in picks:
            pick.score_pick()

    def winning_picked_golfer_ids(self):
        """Get the golfers for the winning picks for the tournament season.
        """
        if self.end_date > datetime.now(timezone.utc):
            return None
        
        users = [season_user.user for season_user in UserSeason.objects.filter(season=self.season_id).all()]
        picked_tournament_golfers = [self.user_pick(user).scored_tournament_golfer() for user in users if self.user_pick(user) is not None and self.user_pick(user).scored_golfer != None]
        highest_position, _ = self.winning_pick_position()

        return [picked_golfer.golfer_season.golfer.id for picked_golfer in picked_tournament_golfers if picked_golfer.position == highest_position]
