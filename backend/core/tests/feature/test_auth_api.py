from rest_framework.test import APITestCase, APIClient
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from http.cookies import SimpleCookie

from core.models.user import User

class TestAuthApi(APITestCase):
    """Tests for the various authentication-based endpoints.
    """
    fixtures = ['user']

    def setUp(self) -> None:
        """Set up necessary objects for testing.
        """
        self.client = APIClient()
        self.test_user: User = User.objects.get(email='onendonedev@gmail.com')
        self.test_user_password = 'superbadtestpw'
        return super().setUp()
    
    def _authenticate_test_user(self) -> None:
        """Helper method to authenticate the test user.
        """
        self.client.force_authenticate(self.test_user)
        token = RefreshToken.for_user(self.test_user)
        self.client.cookies = SimpleCookie({'refresh_token': str(token)})
    
    def test_login(self):
        """Test the POST method for logging a user in.
        """
        # test logging in via the api endpoint
        response: Response = self.client.post('/api/login/', {
            'username': self.test_user.username,
            'password': self.test_user_password,
        }, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_logout(self):
        """Test the POST endpoint for logging a user out.
        """
        self._authenticate_test_user()
        # test logging out via the api endpoint
        response: Response = self.client.post('/api/logout/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
    
    def test_register_user(self):
        """Test the POST endpoint for registering a new user.
        """
        # test creating a valid user using the user registration api endpoint
        user_data = {
            'username': 'TestUser123',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test.user@email.com',
            'password': 'terriblePassword123'
        }
        response = self.client.post(path='/api/register/', data=user_data, format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        
    def test_refresh_token(self):
        """Test the POST endpoint for getting a new access token.
        """
        self._authenticate_test_user()
        # test getting the refresh token usng the refresh token api endpoint
        response: Response = self.client.post(path='/api/login/refresh/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertNotEqual('', response.data.get('access'))
