import logging
from datetime import datetime, timezone
from celery import shared_task

from golf_pickem.models import (
    Season,
    Tournament,
    TournamentSeason,
    Golfer,
    GolferSeason,
    TournamentGolfer
)
from golf_pickem.external_golf_api import get_leaderboard

logger = logging.getLogger('django')

@shared_task
def score_tournament_season(season_id: int|None = None, tournament_id: int = None):
    """Score the most recent round of the active tournament in the active season.
    """
    try:
        season: Season = Season.objects.get(id=season_id) if season_id is not None else Season.active_season()
        tournament: Tournament = Tournament.objects.get(id=tournament_id) if tournament_id is not None else Tournament.objects.get(id=season.active_tournament_id())
        tournament_season: TournamentSeason = TournamentSeason.objects.get(season_id=season.id, tournament_id=tournament.id)
    except Exception as e:
        logger.error(e)
        raise Exception('Problem gathering db objects')
    try:
        leaderboard_response = get_leaderboard(season.year, tournament.external_id)
        if leaderboard_response.status_code == 200:
            for player in leaderboard_response.json().get('leaderboardRows'):
                if player['isAmateur']:
                    continue
                golfer: Golfer = Golfer.objects.filter(external_id=player['playerId']).first()
                if golfer is None:
                    golfer: Golfer = Golfer.create_from_external_data(player)
                golfer_season, _ = GolferSeason.objects.get_or_create(golfer=golfer, season=season)
                tournament_golfer, _ = TournamentGolfer.objects.get_or_create(tournament_season=tournament_season, golfer_season=golfer_season)
                tournament_golfer.update_scores_from_external_api(player)
        if datetime.now(timezone.utc) > tournament_season.end_date:
            tournament_season.finish_tournament_season()
    except TournamentSeason.DoesNotExist as dne:
        raise dne
    except Exception as e:
        logger.error(e)
        raise Exception('Problem gathering leaderboard data from external source')
