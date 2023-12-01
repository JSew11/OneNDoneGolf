from django.test import TestCase

from core.models.user import User
from golf_pickem.models import Pick

class TestPickModel(TestCase):
    """Tests for the pick model.
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
        self.test_user: User = User.objects.get(id=1)
        return super().setUp()