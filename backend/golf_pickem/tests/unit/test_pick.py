from django.test import TestCase
from pytest import raises

from core.models.user import User
from golf_pickem.models.tournament import Tournament
from golf_pickem.models.golfer import Golfer
from golf_pickem.models.tournament_golfer import TournamentGolfer
from golf_pickem.models.pick import Pick

class TestPickModel(TestCase):
    """Tests for the pick model.
    """
    fixtures = ['user', 'golfer', 'tournament', 'tournament_golfer', 'pick']

    def setUp(self) -> None:
        self.test_user: User = User.objects.get(id=1)
        self.test_tournament_golfer_2: TournamentGolfer = TournamentGolfer.objects.get(id=2)
        self.test_tournament_golfer_3: TournamentGolfer = TournamentGolfer.objects.get(id=3)
        self.test_tournament_golfer_4: TournamentGolfer = TournamentGolfer.objects.get(id=4)
        return super().setUp()

    def test_is_valid_pick(self):
        """Test the _is_valid_pick method that controls the golfer selection logic.
        """
        # test the case where this user has already picked this golfer this year (should return false)
        self.assertFalse(Pick.objects._is_valid_pick(self.test_user, self.test_tournament_golfer_3))

        # test the case where this user has already picked for this tournament (should return false)
        self.assertFalse(Pick.objects._is_valid_pick(self.test_user, self.test_tournament_golfer_2))

        # test the case where this user has made a valid pick
        self.assertTrue(Pick.objects._is_valid_pick(self.test_user, self.test_tournament_golfer_4))

    def test_create_pick(self):
        """Test creating a pick.
        """
        # test making a valid pick
        valid_pick: Pick = Pick.objects.create(self.test_user.id, self.test_tournament_golfer_4.id)
        self.assertEqual(valid_pick.tournament_golfer.id, self.test_tournament_golfer_4.id)

        # test making an invalid pick
        with raises(Exception, match=r'Invalid Pick'):
            Pick.objects.create(self.test_user.id, self.test_tournament_golfer_2.id)
