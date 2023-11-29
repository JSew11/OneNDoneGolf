from rest_framework.test import APITestCase, APIClient
from rest_framework.response import Response
from rest_framework import status

from core.models.user import User
from golf_pickem.models.pick import Pick

class TestPickApi(APITestCase):
    """Tests for the pick api endpoints.
    """
    fixtures = ['user', 'tournament', 'golfer', 'tournament_golfer', 'pick']

    def setUp(self) -> None:
        self.client: APIClient = APIClient()
        self.test_user: User = User.objects.get(email='onendonedev@gmail.com')
        return super().setUp()
    
    def test_pick_list_endpoint(self):
        """Test the GET endpoint for getting a list of picks the API call.
        """
        # test hitting the endpoint as an unauthorized user
        response: Response = self.client.get(path='/api/golf-pickem/picks/')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

        self.client.force_authenticate(self.test_user)

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
            'user': self.test_user.id
        }
        response: Response = self.client.get(path='/api/golf-pickem/picks/', data=filterData)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, len(response.data))