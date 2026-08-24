from celery import shared_task

from golf_pickem.models import (
    TournamentSeason,
    Tournament
)
from golf_pickem.external_golf_api import (
    get_schedule,
    get_tournament
)

@shared_task
def get_season_schedule(year: int) -> None:
    """Get the season schedule from the external golf data API and translate the
    data to the appropriate stored models. (Called by the Season model)
    """
    schedule_response = get_schedule(year)
    if (schedule_response.status_code == 200):
        failed_external_ids = list()
        for tourn in schedule_response.json().get('schedule'):
            try:
                tournament: Tournament = Tournament.objects.filter(external_id=tourn['tournId']).first()
                if (tournament is None):
                    tournament_response = get_tournament(year, tourn['tournId'])
                    if (tournament_response.status_code == 200) :
                        Tournament.create_from_external_data(tournament_response.json())
                else:
                    failed_external_ids.push(tourn['tournId'])
                    continue
                TournamentSeason.create_from_external_data(year, tournament.id, tourn)
            except Exception:
                failed_external_ids.push(tourn['tournId'])
                continue
        # TODO - log the failed external ids somewhere