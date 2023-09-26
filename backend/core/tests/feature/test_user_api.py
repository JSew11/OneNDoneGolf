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

class TestUserApi(APITestCase):
    """Tests for the user api endpoints.
    """
    fixtures = ['user']

    def setUp(self) -> None:
        self.admin_user: User = User.objects.get(email='onendonedev@gmail.com')
        self.regular_user: User = User.objects.get(email='regular.user@email.com')
        self.client: APIClient = APIClient()
        return super().setUp()
    
    def test_users_list_endpoint(self):
        """Test the GET endpoint for getting a list of users in the system.
        """
        # test as unauthenticated user
        response: Response = self.client.get(path='/api/users/')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

        # test as non-admin user
        self.client.force_authenticate(self.regular_user)
        response: Response = self.client.get(path='/api/users/')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

        # test as admin user
        self.client.force_authenticate(self.admin_user)
        response: Response = self.client.get(path='/api/users/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_retrieve_user_endpoint(self):
        """Test the GET endpoint for retrieving a user by its associated uuid.
        """
        self.client.force_authenticate(self.regular_user)
        # as the test user test accessing the test user with its uuid (should receive 200)
        response: Response = self.client.get(path=f'/api/users/{self.regular_user.id}/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.regular_user.first_name, response.data['first_name'])

        # as the test user test accessing the admin user with its uuid (should receive 403)
        response: Response = self.client.get(path=f'/api/users/{self.admin_user.id}/')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

        self.client.force_authenticate(self.admin_user)
        # as the admin user test accessing the admin user with its uuid (should receive 200)
        response: Response = self.client.get(path=f'/api/users/{self.admin_user.id}/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.admin_user.first_name, response.data['first_name'])

    def test_partial_update_user_endpoint(self):
        """Test the PATCH endpoint for partially updating a user by its associated uuid.
        """
        regular_user_updated_fields = {
            'last_name': 'Usa'
        }
        admin_user_updated_fields = {
            'last_name': 'Usa'
        }

        self.client.force_authenticate(self.regular_user)
        # as the test user test updating the test user with its uuid (should receive 200)
        response: Response = self.client.patch(path=f'/api/users/{self.regular_user.id}/', data=regular_user_updated_fields, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(regular_user_updated_fields['last_name'], response.data['last_name'])

        # as the test user test updating the admin user with its uuid (should receive 403)
        response: Response = self.client.patch(path=f'/api/users/{self.admin_user.id}/', data=admin_user_updated_fields, format='json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

        self.client.force_authenticate(self.admin_user)
        # as the admin user test accessing the admin user with its uuid (should receive 200)
        response: Response = self.client.get(path=f'/api/users/{self.regular_user.id}/', data=regular_user_updated_fields, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(regular_user_updated_fields['last_name'], response.data['last_name'])