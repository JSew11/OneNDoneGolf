from django.test import TestCase

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
        # TODO: test creating a user without a username
        assert False
        # TODO: test creating a user without an email
        assert False
        # TODO: test creating a user without a password
        assert False
        # TODO: test creating a user without a first name
        assert False
        # TODO: test creating a user without a last name
        assert False
        # TODO: test creating a user with all credentials
        assert False
