from rest_framework.test import APITestCase, APIClient
from rest_framework.response import Response
from rest_framework import status

from core.models.user import User

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
        self.assertEqual(self.regular_user.username, response.data['username'])

        # as the test user test accessing the admin user with its uuid (should receive 403)
        response: Response = self.client.get(path=f'/api/users/{self.admin_user.id}/')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

        self.client.force_authenticate(self.admin_user)
        
        # as the admin user test accessing the admin user with its uuid (should receive 200)
        response: Response = self.client.get(path=f'/api/users/{self.admin_user.id}/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.admin_user.username, response.data['username'])

    def test_partial_update_user_endpoint(self):
        """Test the PATCH endpoint for partially updating a user by its associated uuid.
        """
        updated_fields = {
            'last_name': 'Usa'
        }

        self.client.force_authenticate(self.regular_user)

        # as the test user test updating the test user with its uuid (should receive 200)
        response: Response = self.client.patch(path=f'/api/users/{self.regular_user.id}/', data=updated_fields, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(updated_fields['last_name'], response.data['last_name'])

        # as the test user test updating the admin user with its uuid (should receive 403)
        response: Response = self.client.patch(path=f'/api/users/{self.admin_user.id}/', data=updated_fields, format='json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

        self.client.force_authenticate(self.admin_user)

        # as the admin user test updating the test user with its uuid (should receive 200)
        response: Response = self.client.patch(path=f'/api/users/{self.regular_user.id}/', data=updated_fields, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(updated_fields['last_name'], response.data['last_name'])