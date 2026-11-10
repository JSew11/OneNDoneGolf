import re
from django.db.models import (
    UniqueConstraint,
    Q,
    BigAutoField,
    DateTimeField,
    PositiveSmallIntegerField,
    PositiveIntegerField,
    CharField,
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
    position = CharField(max_length=16, null=True)
    overall_score = CharField(max_length=16, null=True)
    r1_strokes = CharField(max_length=16, null=True)
    r2_strokes = CharField(max_length=16, null=True)
    r3_strokes = CharField(max_length=16, null=True)
    r4_strokes = CharField(max_length=16, null=True)
    total_strokes = CharField(max_length=16, null=True)
    prize_money = PositiveIntegerField(null=True)

    # related models
    tournament_season = ForeignKey(TournamentSeason, on_delete=CASCADE, related_name='field')
    golfer_season = ForeignKey(GolferSeason, on_delete=CASCADE, related_name='tournaments')

    def update_scores_from_external_api(self, external_api_data: dict) -> None:
        """Updates the scores of the model based on the data from the external api.
        """
        self.position = external_api_data['position'] if external_api_data['position'] else None
        self.overall_score = external_api_data['total'] or None
        for round in external_api_data['rounds']:
            roundId = round['roundId']['$numberInt']
            if roundId == '1':
                self.r1_strokes = round['strokes']['$numberInt']
            if roundId == '2':
                self.r2_strokes = round['strokes']['$numberInt']
            if roundId == '3':
                self.r3_strokes = round['strokes']['$numberInt']
            if roundId == '4':
                self.r4_strokes = round['strokes']['$numberInt']
        self.total_strokes = external_api_data['totalStrokesFromCompletedRounds'] if external_api_data['totalStrokesFromCompletedRounds'] else None
        self.save()