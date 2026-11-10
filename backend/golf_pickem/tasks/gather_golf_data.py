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
    try:
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
    except Exception as e:
        logger.info(e)
        raise Exception(f'Problem gathering the schedule from external source {schedule_response.status_code}')

@shared_task
def get_tournament_field(force: bool = False, tournament_id: int|None = None, season_id: int|None = None):
    """Get the participating golfers for the next upcoming tournament in the active season.
    """
    try:
        season: Season = Season.objects.get(id=season_id) if season_id is not None else Season.active_season()
        tournament: Tournament = Tournament.objects.get(id=tournament_id) if tournament_id is not None else Tournament.objects.get(id=season.next_tournament_id(after_date=(datetime.now() + timedelta(days=1))))
        tournament_season: TournamentSeason = TournamentSeason.objects.filter(season_id=season_id, tournament_id=tournament_id).first()
    except Exception as e:
        logger.info(e);
        raise Exception('Problem gathering db objects')
    if (not force and tournament_season.field.count() > 0):
        logger.info('skipping - a field already exists for the given tournament season')
        return # do not want to get the field if it has already been gathered for the next tournament
    try:
        tournament_response = get_tournament(season.year, tournament.external_id)
        if (tournament_response.status_code == 200):
            for player in tournament_response.json().get('players'):
                if player['isAmateur']:
                    logger.info(f'skipping player {player['playerId']} - amateur')
                    continue  # amateurs do not win prize money - they should not be included in the field
                golfer: Golfer = Golfer.objects.filter(external_id=player['playerId']).first()
                if golfer is None:
                    golfer: Golfer = Golfer.create_from_external_data(external_api_data=player)
                golfer_season: GolferSeason = GolferSeason.objects.get_or_create(golfer_id=golfer.id, season_id=season.id)
                TournamentGolfer.objects.get_or_create(tournament_season=tournament_season, golfer_season=golfer_season)
    except Exception as e:
        logger.info(e)
        raise Exception(f'Problem gathering the field from external source {tournament_response.status_code}')
        # todo - find a better way to log failed data imports