from datetime import datetime
from rest_framework.test import APITestCase, APIClient
from rest_framework.response import Response
from rest_framework import status

from core.models import User
from golf_pickem.models import (
    Season,
    Golfer,
    Tournament
)

class TestSeasonViewSet(APITestCase):
    """Tests for the season viewset endpoints.
    """
    fixtures = [
        'user',
        'season',
        'tournament',
        'tournament_season',
    ]

    def setUp(self) -> None:
        self.client: APIClient = APIClient()
        self.admin_user: User = User.objects.get(email='onendonedev@gmail.com')
        self.test_season: Season = Season.objects.get(id=1)
        self.test_tournament_3: Tournament = Tournament.objects.get(id=3)
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
        self.assertEqual(1, len(response.data))
    
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
    
    def test_active_season_endpoint(self):
        """Test the GET endpoint for getting the active season's details.
        """
        # test hitting the endpoint as an unauthorized user
        response: Response = self.client.get(path=f'/api/golf-pickem/seasons/active/')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

        self.client.force_authenticate(self.admin_user)
        
        # test getting the active season
        response: Response = self.client.get(path=f'/api/golf-pickem/seasons/active/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.test_season.id, response.data['id'])
        self.assertTrue(response.data['active'])
        
        # test getting the active season when there are no active seasons
        self.test_season.active = False
        self.test_season.save()
        response: Response = self.client.get(path=f'/api/golf-pickem/seasons/active/')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
    
    def test_next_tournament_endpoint(self):
        """Test the GET endpoint for getting the next tournament for the given
        season.
        """
        after_date_data = {
            'after_date': datetime(2024, 2, 1).strftime('%Y-%m-%d')
        }

        # test hitting the endpoint as an unauthorized user
        response: Response = self.client.get(path=f'/api/golf-pickem/seasons/{self.test_season.id}/next-tournament/', data=after_date_data)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

        self.client.force_authenticate(self.admin_user)

        # test getting the next tournament for the test season
        response: Response = self.client.get(path=f'/api/golf-pickem/seasons/{self.test_season.id}/next-tournament/', data=after_date_data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.test_tournament_3.id, response.data['tournament']['id'])
        self.assertIsNone(response.data['user_pick'])

class TestSeasonGolfersViewSet(APITestCase):
    """Tests for the season golfers viewset endpoints.
    """
    fixtures = [
        'user',
        'season',
        'golfer',
        'golfer_season'
    ]

    def setUp(self) -> None:
        self.client: APIClient = APIClient()
        self.admin_user: User = User.objects.get(email='onendonedev@gmail.com')
        self.test_season: Season = Season.objects.get(id=1)
        self.test_golfer: Golfer = Golfer.objects.get(id=1)
        return super().setUp()
    
    def test_season_golfers_list_endpoint(self):
        """Test the GET endpoint for getting the list of golfers participating in
        a given season.
        """
        # test hitting the endpoint as an unauthorized user
        response: Response = self.client.get(path=f'/api/golf-pickem/seasons/{self.test_season.id}/golfers/')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        
        self.client.force_authenticate(self.admin_user)

        # test getting the list of season golfers
        response: Response = self.client.get(path=f'/api/golf-pickem/seasons/{self.test_season.id}/golfers/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(3, len(response.data))
    
    def test_retrieve_season_golfer_endpoint(self):
        """Test the GET endpoint for retrieving an individual golfer participating 
        in a given season.
        """
        # test hitting the endpoint as an unauthorized user
        response: Response = self.client.get(path=f'/api/golf-pickem/seasons/{self.test_season.id}/golfers/{self.test_golfer.id}/')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        
        self.client.force_authenticate(self.admin_user)

        # test getting the season golfer by the season id and golfer id
        response: Response = self.client.get(path=f'/api/golf-pickem/seasons/{self.test_season.id}/golfers/{self.test_golfer.id}/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.test_season.id, response.data['season'])
        self.assertEqual(self.test_golfer.id, response.data['golfer'])

class TestSeasonTournamentsViewSet(APITestCase):
    """Tests for the season tournaments viewset endpoints.
    """
    fixtures = [
        'user',
        'season',
        'tournament',
        'golfer',
        'tournament_season',
        'golfer_season',
        'tournament_golfer',
        'pick'
    ]

    def setUp(self) -> None:
        self.client: APIClient = APIClient()
        self.admin_user: User = User.objects.get(email='onendonedev@gmail.com')
        self.test_season: Season = Season.objects.get(id=1)
        self.test_tournament_1: Tournament = Tournament.objects.get(id=1)
        self.test_tournament_3: Tournament = Tournament.objects.get(id=3)
        return super().setUp()
    
    def test_season_tournaments_list_endpoint(self):
        """Test the GET endpoint for getting the list of tournaments for a given
        season.
        """
        # test hitting the endpoint as an unauthorized user
        response: Response = self.client.get(path=f'/api/golf-pickem/seasons/{self.test_season.id}/tournaments/')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        
        self.client.force_authenticate(self.admin_user)

        # test getting the list of season tournaments
        response: Response = self.client.get(path=f'/api/golf-pickem/seasons/{self.test_season.id}/tournaments/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(3, len(response.data))
    
    def test_retrieve_season_tournament_endpoint(self):
        """Test the GET endpoint for retrieving an individual tournament for a given
        season.
        """
        # test hitting the endpoint as an unauthorized user
        response: Response = self.client.get(path=f'/api/golf-pickem/seasons/{self.test_season.id}/tournaments/{self.test_tournament_1.id}/')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        
        self.client.force_authenticate(self.admin_user)

        # test getting the season tournament by the season id and tournament id
        response: Response = self.client.get(path=f'/api/golf-pickem/seasons/{self.test_season.id}/tournaments/{self.test_tournament_1.id}/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.test_season.id, response.data['season'])
        self.assertEqual(self.test_tournament_1.id, response.data['tournament']) 

    def test_available_golfers_endpoint(self):
        """Test the GET endpoint for getting a list of available golfers.
        """
        # test hitting the endpoint as an unauthorized user
        response: Response = self.client.get(path=f'/api/golf-pickem/seasons/{self.test_season.id}/tournaments/{self.test_tournament_3.id}/available-golfers/')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

        self.client.force_authenticate(self.admin_user)

        # test getting the list of available golfers
        response: Response = self.client.get(path=f'/api/golf-pickem/seasons/{self.test_season.id}/tournaments/{self.test_tournament_3.id}/available-golfers/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertEqual(3, response.data[0]['id'])

class TestSeasonTournamentGolfersViewSet(APITestCase):
    """Tests for the season tournament golfers viewset endpoints.
    """
    fixtures = [
        'user',
        'season',
        'tournament',
        'golfer',
        'tournament_season',
        'golfer_season',
        'tournament_golfer'
    ]

    def setUp(self) -> None:
        self.client: APIClient = APIClient()
        self.admin_user: User = User.objects.get(email='onendonedev@gmail.com')
        self.test_season: Season = Season.objects.get(id=1)
        self.test_tournament: Tournament = Tournament.objects.get(id=1)
        self.test_golfer: Golfer = Golfer.objects.get(id=1)
        return super().setUp()
    
    def test_season_tournament_golfers_list_endpoint(self):
        """Test the GET endpoint for getting the list of golfers for a given
        tournament that takes place during a given season.
        """
        # test hitting the endpoint as an unauthorized user
        response: Response = self.client.get(path=f'/api/golf-pickem/seasons/{self.test_season.id}/tournaments/{self.test_tournament.id}/golfers/')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        
        self.client.force_authenticate(self.admin_user)

        # test getting the list of tournament golfers
        response: Response = self.client.get(path=f'/api/golf-pickem/seasons/{self.test_season.id}/tournaments/{self.test_tournament.id}/golfers/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(3, len(response.data))
    
    def test_retrieve_season_tournament_golfer_endpoint(self):
        """Test the GET endpoint for retrieving an individual golfer for a given
        tournament that takes place during the given season.
        """
        # test hitting the endpoint as an unauthorized user
        response: Response = self.client.get(path=f'/api/golf-pickem/seasons/{self.test_season.id}/tournaments/{self.test_tournament.id}/golfers/{self.test_golfer.id}/')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        
        self.client.force_authenticate(self.admin_user)

        # test getting the tournament golfer by the season id, tournament id, and golfer id
        response: Response = self.client.get(path=f'/api/golf-pickem/seasons/{self.test_season.id}/tournaments/{self.test_tournament.id}/golfers/{self.test_golfer.id}/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)