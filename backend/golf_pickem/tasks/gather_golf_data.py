import logging
from datetime import (
    datetime,
    timedelta
)
from celery import shared_task

from golf_pickem.models import (
    Season,
    TournamentSeason,
    Tournament,
    Golfer,
    GolferSeason,
    TournamentGolfer
)
from golf_pickem.external_golf_api import (
    get_schedule,
    get_tournament
)

logger = logging.getLogger('django')

@shared_task
def get_season_schedule(year: int, start_from_current_date: bool = False) -> None:
    """Get the season schedule from the external golf data API and translate the
    data to the appropriate stored models. (Called by the Season model)
    """
    schedule_response = get_schedule(year)
    if (schedule_response.status_code == 200):
        failed_external_ids = list()
        for tourn in schedule_response.json().get('schedule'):
            if (
                start_from_current_date and
                datetime.fromtimestamp(int(tourn['date']['start']['$date']['$numberLong'])/1e3) < datetime.now()
            ):
                logger.info(f'skipping tournament id {tourn['tournId']}')
                continue
            try:
                logger.info(f'gathering data for tournament with external id {tourn['tournId']}')
                tournament: Tournament = Tournament.objects.filter(external_id=tourn['tournId']).first()
                if (tournament is None):
                    tournament_response = get_tournament(year, tourn['tournId'])
                    if (tournament_response.status_code == 200) :
                        tournament = Tournament.create_from_external_data(tournament_response.json())
                TournamentSeason.create_from_external_data(year, tournament.id, tourn)
            except Exception as e:
                logger.info(f'failed to gather tournament id {tourn['tournId']} - {e}')
                failed_external_ids.append(tourn['tournId'])
                continue
        # todo - find a better way to log failed data imports
    else :
        raise Exception(f'Problem gathering the schedule from external source {schedule_response.status_code}')

@shared_task
def get_tournament_field(force: bool = False, tournament_id: int = None):
    """Get the participating golfers for the next upcoming tournament in the active season.
    """
    active_season: Season = Season.active_season()
    if tournament_id is None: # default to getting the next tournament if none is provided
        tournament: Tournament = Tournament.objects.get(active_season.next_tournament_id(after_date=datetime.now() + timedelta(days=1)))
    else:
        tournament: Tournament = Tournament.objects.get(tournament_id)
    tournament_season: TournamentSeason = TournamentSeason.objects.get(season_id=active_season.id, tournament_id=tournament.id)
    if (not force and tournament_season.field.count() > 0):
        return # do not want to get the field if it has already been gathered for the next tournament
    tournament_response = get_tournament(active_season.year, tournament.external_id)
    if (tournament_response.status_code == 200):
        failed_external_ids = list()
        for player in tournament_response.json().get('players'):
            if player['isAmateur']:
                continue  # amateurs do not win prize money - they should not be included in the field
            try:
                golfer: Golfer = Golfer.objects.filter(external_id=player['playerId']).first()
                if golfer is None:
                    golfer: Golfer = Golfer.create_from_external_data(external_api_data=player)
                golfer_season: GolferSeason = GolferSeason.objects.filter(golfer_id=golfer.id, season_id=active_season.id).first()
                if golfer_season is None:
                    golfer_season: GolferSeason = GolferSeason.objects.create(season=active_season, golfer=golfer)
                TournamentGolfer.objects.get_or_create(tournament_season=tournament_season, golfer_season=golfer_season)
            except Exception as e:
                logger.info(f'failed to gather golfer id {player['playerId']} - {e}')
                failed_external_ids.append(player['playerId'])
                continue
    else:
        raise Exception(f'Problem gathering the field from external source {tournament_response.status_code}')
        # todo - find a better way to log failed data imports