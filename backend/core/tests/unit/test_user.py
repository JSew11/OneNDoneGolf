from django.test import TestCase

from core.models.user import User

class TestUserModel(TestCase):
    """Tests for the user model.
    """

    def setUp(self) -> None:
        return super().setUp()
    
    def test_create_user(self):
        """Tests for creating a normal system user.
        """
        assert False
        # TODO: test creating a user without a username

        # TODO: test creating a user without an email

        # TODO: test creating a user without a password

        # TODO: test creating a user without a first name

        # TODO: test creating a user without a last name

        # TODO: test creating a user with all credentials
