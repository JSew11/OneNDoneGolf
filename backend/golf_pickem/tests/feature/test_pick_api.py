from rest_framework.test import APITestCase, APIClient
from rest_framework.response import Response
from rest_framework import status

from core.models.user import User
from golf_pickem.models.pick import Pick
from golf_pickem.models.tournament_golfer import TournamentGolfer

class TestPickApi(APITestCase):
    """Tests for the pick api endpoints.
    """
    fixtures = ['user', 'tournament', 'golfer', 'tournament_golfer', 'pick']

    def setUp(self) -> None:
        self.client: APIClient = APIClient()
        self.admin_user: User = User.objects.get(email='onendonedev@gmail.com')
        self.test_pick: Pick = Pick.objects.get(id=1)
        self.test_tournament_golfer: TournamentGolfer = TournamentGolfer.objects.get(id=4)
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
        self.assertEqual(1, len(response.data))

        # test getting all picks made by the user making the request (filtered by year)
        filterData = {
            'year': 2023
        }
        response: Response = self.client.get(path='/api/golf-pickem/picks/', data=filterData)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, len(response.data))

        # test getting all picks made by a specific user
        filterData = {
            'user': self.admin_user.id
        }
        response: Response = self.client.get(path='/api/golf-pickem/picks/', data=filterData)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, len(response.data))

    def test_create_pick_endpoint(self):
        """Test the POST endpoint for creating a new pick using a given tournament
        golfer.
        """
        data = {
            'tournament_golfer': self.test_tournament_golfer.id
        }

        # test hitting the endpoint as an unauthorized user
        response: Response = self.client.post(path='/api/golf-pickem/picks/', data=data, format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

        self.client.force_authenticate(self.admin_user)
        
        # test making a valid pick
        response: Response = self.client.post(path='/api/golf-pickem/picks/', data=data, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # test making an invalid pick
        response: Response = self.client.post(path='/api/golf-pickem/picks/', data=data, format='json')
        self.assertEqual(status.HTTP_409_CONFLICT, response.status_code)


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