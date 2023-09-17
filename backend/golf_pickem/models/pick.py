from typing import Any
from django.db.models import (
    BigAutoField,
    DateTimeField,
    ForeignKey,
    CASCADE
)
from safedelete.models import SafeDeleteModel
from safedelete.managers import SafeDeleteManager
from safedelete import SOFT_DELETE, DELETED_VISIBLE_BY_PK

from core.models.user import User
from .tournament_golfer import TournamentGolfer

class PickManager(SafeDeleteManager):
    """Manager for the pick model.
    
    Enforces the rule that a golfer can only be picked once per year.
    """
    _safedelete_visibility = DELETED_VISIBLE_BY_PK

    def create(self, user_id: str, tournament_golfer_id: str, **kwargs: Any) -> Any:
        """Overwritten create method that enforces the rule that a golfer can only be picked once per year.
        """
        user: User = User.objects.get(id=user_id)
        tournament_golfer: TournamentGolfer = TournamentGolfer.objects.get(id=tournament_golfer_id)
        kwargs['user'] = user
        kwargs['tournament_golfer'] = tournament_golfer
        if (not self._is_valid_pick(user=user, tournament_golfer=tournament_golfer)):
            raise Exception('Invalid Pick')
        return super().create(**kwargs)
    
    def _is_valid_pick(self, user: User, tournament_golfer: TournamentGolfer) -> bool:
        """Determines if a valid pick can be made with the given user and tournament golfer.
        """
        tournament_year: int = tournament_golfer.tournament.year
        previous_picks = user.pick_history_by_year(tournament_year)
        previously_picked_golfers = previous_picks.values_list('tournament_golfer__golfer', flat=True).all()
        tournaments_picked_in = previous_picks.values_list('tournament_golfer__tournament', flat=True).all()
        if tournament_golfer.golfer.id not in previously_picked_golfers and tournament_golfer.tournament.id not in tournaments_picked_in:
            return True
        return False

class Pick(SafeDeleteModel):
    """Model for a user's pick,

    A user can only pick a golfer once per year.
    """

    objects = PickManager()
    deleted_by_cascade = None # removes this default field from the db table
    _safedelete_policy = SOFT_DELETE

    class Meta:
        ordering = ['created']
        verbose_name = 'Picks'
        verbose_name_plural = 'Picks'

    # database info
    id = BigAutoField(primary_key=True, editable=False)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    # related models
    user = ForeignKey(User, on_delete=CASCADE, related_name='pick_history')
    tournament_golfer = ForeignKey(TournamentGolfer, on_delete=CASCADE, related_name='picked_by_history')
