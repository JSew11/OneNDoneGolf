from datetime import datetime
from celery import shared_task

from golf_pickem.models import (
    Season,
    TournamentSeason
)

@shared_task
def score_active_tournament_season():
    """Score the most recent round of the active tournament in the active season.
    """
    active_season: Season = Season.active_season()
    if active_tournament_id := active_season.active_tournament_id() is not None:
        active_tournament_season: TournamentSeason = TournamentSeason.objects.filter(
            season_id=active_season.id,
            tournament_id=active_tournament_id
        ).first()
        # TODO - store the most recently completed rounds' scores in the tournament golfer models
        if datetime.now() > active_tournament_season.end_date:
            active_tournament_season.finish_tournament_season()
