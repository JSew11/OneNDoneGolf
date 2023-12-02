from rest_framework.test import APITestCase, APIClient
from rest_framework.response import Response
from rest_framework import status

from core.models.user import User
from golf_pickem.models.pick import Pick

class TestPickApi(APITestCase):
    """Tests for the pick api endpoints.
    """
    fixtures = [
        'user',
        'season',
        'tournament',
        'tournament_season',
        'golfer',
        'golfer_season',
        'pick'
    ]

    def setUp(self) -> None:
        self.client: APIClient = APIClient()
        self.admin_user: User = User.objects.get(email='onendonedev@gmail.com')
        self.test_pick: Pick = Pick.objects.get(id=1)
        return super().setUp()
    
    def test_pick_list_endpoint(self):
        """Test the GET endpoint for getting a list of picks.
        """
        # test hitting the endpoint as an unauthorized user
        response: Response = self.client.get(path='/api/golf-pickem/picks/')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

        self.client.force_authenticate(self.admin_user)

        # test getting all picks for the user making the request
        response: Response = self.client.get(path='/api/golf-pickem/picks/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, len(response.data))

        # test getting all picks made by the user making the request (filtered by year)
        filterData = {
            'season_id': 1
        }
        response: Response = self.client.get(path='/api/golf-pickem/picks/', data=filterData)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(0, len(response.data))

        # test getting all picks made by a specific user
        filterData = {
            'user': self.admin_user.id
        }
        response: Response = self.client.get(path='/api/golf-pickem/picks/', data=filterData)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, len(response.data))

    def test_create_pick_endpoint(self):
        """Test the POST endpoint for creating a new pick using a given tournament,
        golfer, and season.
        """
        # test hitting the endpoint as an unauthorized user
        response: Response = self.client.post(path='/api/golf-pickem/picks/', data={})
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

        self.client.force_authenticate(self.admin_user)

        # test creating a pick without providiing the required fields
        response: Response = self.client.post(path='/api/golf-pickem/picks/', data={})
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertIn('Field \'tournament_id\' is required', response.data['errors'])
        self.assertIn('Field \'golfer_id\' is required', response.data['errors'])
        self.assertIn('Field \'season_id\' is required', response.data['errors'])

        # test creating a pick for an invalid tournament season
        invalid_tournament_season_pick_data = {
            'tournament_id': 100,
            'golfer_id': 1,
            'season_id': 2,
        }
        response: Response = self.client.post(path='/api/golf-pickem/picks/', data=invalid_tournament_season_pick_data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertIn('Tournament', response.data['message'])
        self.assertIn('Season', response.data['message'])

        # test creating a pick for an invalid golfer season
        invalid_golfer_season_pick_data = {
            'tournament_id': 3,
            'golfer_id': 100,
            'season_id': 2,
        }
        response: Response = self.client.post(path='/api/golf-pickem/picks/', data=invalid_golfer_season_pick_data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertIn('Golfer', response.data['message'])
        self.assertIn('Season', response.data['message'])

        # test creating a valid pick
        valid_pick_data = {
            'tournament_id': 3,
            'golfer_id': 3,
            'season_id': 2,
        }
        response: Response = self.client.post(path='/api/golf-pickem/picks/', data=valid_pick_data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        # test creating an invalid pick
        invalid_pick_data = {
            'tournament_id': 3,
            'golfer_id': 2,
            'season_id': 2,
        }
        response: Response = self.client.post(path='/api/golf-pickem/picks/', data=invalid_pick_data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('You have already picked in this tournament for this season', response.data['message'])

    def test_retrieve_pick_endpoint(self):
        """Test the GET endpoint for getting a specific pick by its id.
        """
        # test hitting the endpoint as an unauthorized user.
        response: Response = self.client.get(path=f'/api/golf-pickem/picks/{self.test_pick.id}/')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

        self.client.force_authenticate(self.admin_user)

        # test getting the test pick by its id
        response: Response = self.client.get(path=f'/api/golf-pickem/picks/{self.test_pick.id}/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.test_pick.id, response.data['id'])