import requests
from celery import shared_task

from golf_pickem.constants import (
    API_BASE_URL,
    API_PGA_TOUR_LEAGUE_ID
)
from golf_pickem.models import (
    Season
)

@shared_task
def get_season_schedule(season_id) -> None:
    """Get the season schedule from the external golf data API and translate the
    data to the appropriate stored models.
    """
    season: Season = Season.objects.get(season_id)

    response = requests.get(
        API_BASE_URL + '/eventsseason.php',
        params={
            'id': API_PGA_TOUR_LEAGUE_ID,
            's': season.start_date.year
        }
    )
    if response.status_code == requests.codes.ok:
        # TODO - get data from api request and transform it into usable saved models
