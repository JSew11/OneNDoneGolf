from django.test import TestCase
from django.db.utils import IntegrityError
from django.db.transaction import atomic
from pytest import raises

from core.models.user import User

class TestUserModel(TestCase):
    """Tests for the user model.
    """
    fixtures = ['user']

    def setUp(self) -> None:
        self.test_user: User = User.objects.get(username='OneNDoneDev')
        return super().setUp()
    
    def test_create_user(self) -> None:
        """Tests for creating a normal system user.
        """
        test_username = 'OneNDonePlayer'
        test_email = 'onendoneplayer@email.com'
        test_first_name = 'Test'
        test_last_name = 'Player'
        test_password = 'badpassword'

        # test creating a user without an email
        with raises(ValueError, match=r'No email provided - this field is required.'):
                    User.objects.create_user(
                        username=test_username,
                        first_name=test_first_name,
                        last_name=test_last_name,
                        password=test_password
                    )

        # test creating a user without a username
        with raises(ValueError, match=r'No username provided - this field is required.'):
                    User.objects.create_user(
                        email=test_email,
                        first_name=test_first_name,
                        last_name=test_last_name,
                        password=test_password
                    )

        # test creating a user without a password
        with raises(ValueError, match=r'No password provided - this field is required.'):
                    User.objects.create_user(
                        username=test_username,
                        email=test_email,
                        first_name=test_first_name,
                        last_name=test_last_name,
                    )

        # test creating a user without a first or last name
        test_user_nameless: User = User.objects.create_user(
            username=test_username,
            email=test_email,
            password=test_password
        )
        self.assertEqual(test_user_nameless.first_name, '')
        self.assertEqual(test_user_nameless.last_name, '')

        # test creating a duplicate user
        with atomic(): # need this to allow the db query to run so this is caught
            with raises(IntegrityError):
                    User.objects.create_user(
                        username=test_username,
                        email=test_email,
                        first_name=test_first_name,
                        last_name=test_last_name,
                        password=test_password
                    )

        # test creating a user with all fields
        test_user_complete: User = User.objects.create_user(
                    username='CompleteUser',
                    email='completeuser@email.com',
                    first_name='Complete',
                    last_name='User',
                    password=test_password
                )
        self.assertEqual(test_user_complete.username, 'CompleteUser')
        self.assertEqual(test_user_complete.email, 'completeuser@email.com')
        self.assertEqual(test_user_complete.first_name, 'Complete')
        self.assertEqual(test_user_complete.last_name, 'User')
