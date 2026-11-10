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
    return requests.get(url, headers=_headers(), params=queryParams)

def get_tournament(year: int, tournament_external_id: str):
    """Get a tournament's info from the external golf api.
    """
    url = API_BASE_URL + '/tournament'
    queryParams = {
        'orgId': PGA_TOUR_LEAGUE_ID,
        'tournId': tournament_external_id,
        'year': year
    }
    return requests.get(url, headers=_headers(), params=queryParams)

def get_leaderboard(year: int, tournament_external_id: str):
    """Get the leaderboard for a given tournament in a given year from the external golf api.
    """
    url = API_BASE_URL + '/leaderboard'
    queryParams = {
        'orgId': PGA_TOUR_LEAGUE_ID,
        'tournId': tournament_external_id,
        'year': year
    }
    return requests.get(url, headers=_headers(), params=queryParams)

def get_earnings(year: int, tournament_external_id: str):
    """Get the leaderboard for a given tournament in a given year from the external golf api.
    """
    url = API_BASE_URL + '/earnings'
    queryParams = {
        'tournId': tournament_external_id,
        'year': year
    }
    return requests.get(url, headers=_headers(), params=queryParams)

def get_owgr(year: int):
    """Get the owgr for the given year from the external golf api.
    """
    url = API_BASE_URL + '/owgr'
    queryParams = {
        'year': year
    }
    return requests.get(url, headers=_headers(), params=queryParams)

def _headers() -> dict:
    """Returns the headers dict used for all external api requests.
    """
    return {
        'x-rapidapi-key': API_KEY,
        'Content-Type': 'application/json'
    }