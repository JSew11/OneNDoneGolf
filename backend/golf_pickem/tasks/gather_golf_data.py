from celery import shared_task

from golf_pickem.models import (
    Tournament
)
from golf_pickem.external_golf_api import get_schedule

@shared_task
def get_season_schedule(year: int) -> None:
    """Get the season schedule from the external golf data API and translate the
    data to the appropriate stored models.
    """
    response = get_schedule(year)
    if (response.status_code == 200):
        tournament_external_ids = [tourn.get('tournId') for tourn in response.json().get('schedule')]
        # TODO - call the tournaments api for each id in the response
