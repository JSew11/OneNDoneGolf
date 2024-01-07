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
        self.test_season: Season = Season.objects.get(id=1)
        return super().setUp()
    
    def test_seasons_list_endpoint(self):
        """Test the GET endpoint for getting the list of seasons.
        """
        # test hitting the endpoint as an unauthorized user
        response: Response = self.client.get(path='/api/golf-pickem/seasons/')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        
        self.client.force_authenticate(self.admin_user)

        # test getting the list of seasons
        response: Response = self.client.get(path='/api/golf-pickem/seasons/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, len(response.data))
    
    def test_create_season_endpoint(self):
        """Test the POST endpoint for creating a season.
        """
        # test hitting the endpoint as an unauthorized user
        response: Response = self.client.post(path='/api/golf-pickem/seasons/')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

        self.client.force_authenticate(self.admin_user)
        
        # test creating a new season with no data
        response: Response = self.client.post(path='/api/golf-pickem/seasons/', data={})
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

        # test creating a valid new season
        new_season_data = {
            'year': 2002,
            'name': 'Test Golf League',
            'alias': 'TGL'
        }
        response: Response = self.client.post(path='/api/golf-pickem/seasons/', data=new_season_data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
    
    def test_retrieve_season_endpoint(self):
        """Test the GET endpoint for retrieving a season by its id.
        """
        # test hitting the endpoint as an unauthorized user
        response: Response = self.client.get(path=f'/api/golf-pickem/seasons/{self.test_season.id}/')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

        self.client.force_authenticate(self.admin_user)

        # test getting the test season by its id
        response: Response = self.client.get(path=f'/api/golf-pickem/seasons/{self.test_season.id}/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.test_season.id, response.data['id'])
    
    def test_partial_update_season_endpoint(self):
        """Test the PATCH endpoint for updating a season by its id.
        """
        # test hitting the endpoint as an unauthorized user
        response: Response = self.client.patch(path=f'/api/golf-pickem/seasons/{self.test_season.id}/', data={})
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

        self.client.force_authenticate(self.admin_user)

        # test updating the test season with no data
        response: Response = self.client.patch(path=f'/api/golf-pickem/seasons/{self.test_season.id}/', data={})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.test_season.id, response.data['id'])

        # test updating the test season with an invalid year
        invalid_year_data = {
            'year': -12
        }
        response: Response = self.client.patch(path=f'/api/golf-pickem/seasons/{self.test_season.id}/', data=invalid_year_data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

        # test updating the season successfully
        updated_season_data = {
            'name': 'Fake Golf League',
            'alias': 'FGL'
        }
        response: Response = self.client.patch(path=f'/api/golf-pickem/seasons/{self.test_season.id}/', data=updated_season_data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(updated_season_data['name'], response.data['name'])
    
    def test_destroy_season_endpoint(self):
        """Test the DELETE endpoint for deleting a season by its id.
        """
        # test hitting the endpoint as an unauthorized user
        response: Response = self.client.delete(path=f'/api/golf-pickem/seasons/{self.test_season.id}/')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

        self.client.force_authenticate(self.admin_user)

        # test deleting a pick that does not exist
        response: Response = self.client.delete(path=f'/api/golf-pickem/seasons/{999}/')
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

        # test deleting a pick that does exist
        response: Response = self.client.delete(path=f'/api/golf-pickem/seasons/{self.test_season.id}/')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)