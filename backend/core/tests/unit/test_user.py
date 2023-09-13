from django.test import TestCase
from pytest import raises

from core.models.user import User

class TestUserModel(TestCase):
    """Tests for the user model.
    """
    fixtures = ['user']

    def setUp(self) -> None:
        self.test_user: User = User.objects.get(username='OneNDoneDev')
        return super().setUp()
    
    def test_create_user(self):
        """Tests for creating a normal system user.
        """
        test_username = 'OneNDonePlayer'
        test_email = 'onendoneplayer@email.com'
        test_first_name = 'Test'
        test_last_name = 'Player'
        password = 'badpassword'

        # test creating a user without a username
        with raises(ValueError, match=r'No username provided - this field is required.'):
                    User.objects.create(
                        email=test_email,
                        first_name=test_first_name,
                        last_name=test_last_name,
                        password=password
                    )
        
        # TODO: test creating a user without an email
        with raises(ValueError, match=r'No email provided - this field is required.'):
                    User.objects.create(
                        username=test_username,
                        first_name=test_first_name,
                        last_name=test_last_name,
                        password=password
                    )

        # TODO: test creating a user without a password

        # TODO: test creating a user without a first name

        # TODO: test creating a user without a last name

        # TODO: test creating a user with all credentials
