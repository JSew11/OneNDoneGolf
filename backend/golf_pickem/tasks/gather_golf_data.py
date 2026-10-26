import logging
from datetime import (
    datetime
)
from celery import shared_task

from golf_pickem.models import (
    TournamentSeason,
    Tournament
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