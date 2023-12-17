from rest_framework.test import APITestCase, APIClient
from rest_framework.response import Response
from rest_framework import status

from core.models import User
from golf_pickem.models import (
    Season
)

class TestSeasonsApi(APITestCase):
    """Tests for the seasons api endpoints.
    """
    fixtures = [
        'user',
        'season',
        'tournament',
        'tournament_season',
        'golfer',
        'golfer_season',
    ]

    def setUp(self) -> None:
        self.client: APIClient = APIClient()
        self.admin_user: User = User.objects.get(email='onendonedev@gmail.com')
        return super().setUp()
    
    def test_seasons_list_endpoint(self):
        """Test the GET endpoint for getting the list of seasons.
        """
        self.assertTrue(False)
    
    def test_create_season_endpoint(self):
        """Test the POST endpoint for creating a season.
        """
        self.assertTrue(False)
    
    def test_retrieve_season_endpoint(self):
        """Test the GET endpoint for retrieving a season by its id.
        """
        self.assertTrue(False)
    
    def test_partial_update_season_endpoint(self):
        """Test the PATCH endpoint for updating a season by its id.
        """
    
    def test_destroy_season_endpoint(self):
        """Test the DELETE endpoint for deleting a season by its id.
        """
        self.assertTrue(False)