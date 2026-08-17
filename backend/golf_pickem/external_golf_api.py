import requests
from golf_pickem.constants import (
    API_BASE_URL,
    API_KEY,
    PGA_TOUR_LEAGUE_ID
)

def get_schedule(year: int):
    """Get the tournament schedule for a given year from the external golf api.
    """
    url = API_BASE_URL + '/schedule'
    queryParams = {
        'orgId': PGA_TOUR_LEAGUE_ID,
        'year': year
    }
    return requests.get(url, headers=_headers(), params=params)

def _headers() -> dict:
    """Returns the headers dict used for all external api requests.
    """
    return {
        'x-rapidapi-key': API_KEY,
        'Content-Type': 'application/json'
    }