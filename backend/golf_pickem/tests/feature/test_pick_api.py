from rest_framework.test import APITestCase, APIClient
from rest_framework.response import Response
from rest_framework import status

from core.models.user import User
from golf_pickem.models import (
    Golfer,
    Tournament,
    Pick,
    Season,
    UserSeason,
)

class TestPickApi(APITestCase):
    """Tests for the pick api endpoints.
    """
    fixtures = [
        'user',
        'season',
        'user_season',
        'tournament',
        'tournament_season',
        'golfer',
        'golfer_season',
        'tournament_golfer',
        'pick'
    ]

    def setUp(self) -> None:
        self.client: APIClient = APIClient()
        self.admin_user: User = User.objects.get(email='onendonedev@gmail.com')
        self.regular_user: User = User.objects.get(email='regular.user@email.com')
        self.test_pick_1: Pick = Pick.objects.get(id=1)
        self.test_pick_2: Pick = Pick.objects.get(id=2)
        self.test_season: Season = Season.objects.get(id=1)
        self.test_golfer_3: Golfer = Golfer.objects.get(id=3)
        self.test_tournament_3: Tournament = Tournament.objects.get(id=3)
        return super().setUp()
    
    def test_pick_list_endpoint(self):
        """Test the GET endpoint for getting a list of picks.
        """
        # test hitting the endpoint as an unauthorized user
        response: Response = self.client.get(path='/api/golf-pickem/picks/')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

        self.client.force_authenticate(self.admin_user)

        # test getting all picks made by the user making the request for the given season
        filterData = {
            'season_id': self.test_season.id
        }
        response: Response = self.client.get(path='/api/golf-pickem/picks/', data=filterData)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, len(response.data))

        # test getting all picks for the user making the request without specifying a season
        response: Response = self.client.get(path='/api/golf-pickem/picks/')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(1, len(response.data['errors']))

        # test getting all picks made by a specific user
        filterData = {
            'season_id': self.test_season.id,
            'user_id': self.regular_user.id
        }
        response: Response = self.client.get(path='/api/golf-pickem/picks/', data=filterData)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(0, len(response.data))

    def test_create_pick_endpoint(self):
        """Test the POST endpoint for creating a new pick using a given tournament,
        golfer, and season.
        """
        # test hitting the endpoint as an unauthorized user
        response: Response = self.client.post(path='/api/golf-pickem/picks/', data={})
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

        self.client.force_authenticate(self.admin_user)

        # test creating a pick without providing the required fields
        response: Response = self.client.post(path='/api/golf-pickem/picks/', data={})
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertIn('Field \'tournament_id\' is required', response.data['errors'])
        self.assertIn('Field \'primary_selection_golfer_id\' is required', response.data['errors'])
        self.assertIn('Field \'backup_selection_golfer_id\' is required', response.data['errors'])
        self.assertIn('Field \'season_id\' is required', response.data['errors'])

        # test creating a pick for an invalid tournament season
        invalid_tournament_pick_data = {
            'tournament_id': 100,
            'primary_selection_golfer_id': 1,
            'backup_selection_golfer_id': 4,
            'season_id': 1,
        }
        response: Response = self.client.post(path='/api/golf-pickem/picks/', data=invalid_tournament_pick_data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

        # test creating a pick for an invalid primary selection golfer season
        invalid_primary_golfer_pick_data = {
            'tournament_id': 3,
            'primary_selection_golfer_id': 100,
            'backup_selection_golfer_id': 2, 
            'season_id': 1,
        }
        response: Response = self.client.post(path='/api/golf-pickem/picks/', data=invalid_primary_golfer_pick_data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

        # test creating a pick for an invalid backup selection golfer season
        invalid_backup_golfer_pick_data = {
            'tournament_id': 3,
            'primary_selection_golfer_id': 3,
            'backup_selection_golfer_id': 200, 
            'season_id': 1,
        }
        response: Response = self.client.post(path='/api/golf-pickem/picks/', data=invalid_backup_golfer_pick_data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

        # test creating a pick with an invalid primary selection golfer
        non_unique_primary_golfer_pick_data = {
            'tournament_id': 3,
            'primary_selection_golfer_id': 1,
            'backup_selection_golfer_id': 4, 
            'season_id': 1,
        }
        response: Response = self.client.post(path='/api/golf-pickem/picks/', data=non_unique_primary_golfer_pick_data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

        # test creating a pick with an invalid backup selection golfer
        non_unique_backup_golfer_pick_data = {
            'tournament_id': 3,
            'primary_selection_golfer_id': 3,
            'backup_selection_golfer_id': 1, 
            'season_id': 1,
        }
        response: Response = self.client.post(path='/api/golf-pickem/picks/', data=non_unique_backup_golfer_pick_data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

        # test creating a pick with the same primary and backup selection golfer
        same_primary_backup_golfer_pick_data = {
            'tournament_id': 3,
            'primary_selection_golfer_id': 3,
            'backup_selection_golfer_id': 3, 
            'season_id': 1,
        }
        response: Response = self.client.post(path='/api/golf-pickem/picks/', data=same_primary_backup_golfer_pick_data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

        # test creating a valid pick
        valid_pick_data = {
            'tournament_id': 3,
            'primary_selection_golfer_id': 3,
            'backup_selection_golfer_id': 4, 
            'season_id': 1,
        }
        response: Response = self.client.post(path='/api/golf-pickem/picks/', data=valid_pick_data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        # test creating a pick with an invalid tournament season
        invalid_pick_data = {
            'tournament_id': 2,
            'primary_selection_golfer_id': 3,
            'backup_selection_golfer_id': 4, 
            'season_id': 1,
        }
        response: Response = self.client.post(path='/api/golf-pickem/picks/', data=invalid_pick_data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_retrieve_pick_endpoint(self):
        """Test the GET endpoint for getting a specific pick by its id.
        """
        # test hitting the endpoint as an unauthorized user
        response: Response = self.client.get(path=f'/api/golf-pickem/picks/{self.test_pick_1.id}/')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

        self.client.force_authenticate(self.admin_user)

        # test getting the test pick by its id
        response: Response = self.client.get(path=f'/api/golf-pickem/picks/{self.test_pick_1.id}/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.test_pick_1.id, response.data['id'])
    
    def test_partial_update_pick_endpoint(self):
        """Test the PATCH update for updating the golfer a pick is selecting.
        """
        # test hitting the endpoint as an unauthorized user
        response: Response = self.client.patch(path=f'/api/golf-pickem/picks/{self.test_pick_2.id}/')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

        self.client.force_authenticate(self.admin_user)

        # test updating a pick without providiing the required 'golfer_id' field
        response: Response = self.client.patch(path=f'/api/golf-pickem/picks/{self.test_pick_2.id}/', data={})
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertIn('Field \'primary_selection_golfer_id\' is required', response.data['errors'])
        self.assertIn('Field \'backup_selection_golfer_id\' is required', response.data['errors'])

        # test updating a pick with an invalid primary selection golfer season
        invalid_golfer_pick_data = {
            'primary_selection_golfer_id': 100,
            'backup_selection_golfer_id': 4
        }
        response: Response = self.client.patch(path=f'/api/golf-pickem/picks/{self.test_pick_2.id}/', data=invalid_golfer_pick_data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

        # test updating a pick with an invalid backup selection golfer season
        invalid_golfer_pick_data = {
            'primary_selection_golfer_id': 3,
            'backup_selection_golfer_id': 400
        }
        response: Response = self.client.patch(path=f'/api/golf-pickem/picks/{self.test_pick_2.id}/', data=invalid_golfer_pick_data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

        # test updating a pick with valid data
        valid_update_data = {
            'primary_selection_golfer_id': 3,
            'backup_selection_golfer_id': 4
        }
        response: Response = self.client.patch(path=f'/api/golf-pickem/picks/{self.test_pick_2.id}/', data=valid_update_data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # test updating a pick with a primary selection golfer the user has already selected this season
        invalid_golfer_pick_data = {
            'primary_selection_golfer_id': 1,
            'backup_selection_golfer_id': 3
        }
        response: Response = self.client.patch(path=f'/api/golf-pickem/picks/{self.test_pick_2.id}/', data=invalid_golfer_pick_data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        
        # test updating a pick with a backup selection goler the user has already selected
        invalid_golfer_pick_data = {
            'primary_selection_golfer_id': 3,
            'backup_selection_golfer_id': 1
        }
        response: Response = self.client.patch(path=f'/api/golf-pickem/picks/{self.test_pick_2.id}/', data=invalid_golfer_pick_data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        
        # test updating a pick with the same primary and backup selection golfers
        invalid_golfer_pick_data = {
            'primary_selection_golfer_id': 3,
            'backup_selection_golfer_id': 3
        }
        response: Response = self.client.patch(path=f'/api/golf-pickem/picks/{self.test_pick_2.id}/', data=invalid_golfer_pick_data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
    
    def test_destroy_pick_endpoint(self):
        """Test the DELETE endpoint for deleting a pick by its id.
        """
        # test hitting the endpoint as an unauthorized user
        response: Response = self.client.delete(path=f'/api/golf-pickem/picks/{self.test_pick_2.id}/')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

        self.client.force_authenticate(self.admin_user)

        # test deleting a pick that does not exist
        response: Response = self.client.delete(path=f'/api/golf-pickem/picks/{999}/')
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

        # test deleting a pick that does exist
        response: Response = self.client.delete(path=f'/api/golf-pickem/picks/{self.test_pick_2.id}/')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)