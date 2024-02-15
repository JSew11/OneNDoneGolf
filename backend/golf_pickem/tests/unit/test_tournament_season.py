from django.test import TestCase

from core.models import User
from golf_pickem.models import (
    Season,
    TournamentSeason,
    Pick,
)

class TestTournamentSeasonModel(TestCase):
    """Tests for the tournament season model.
    """
    fixtures = [
        'user',
        'season',
        'tournament',
        'tournament_season',
        'golfer',
        'golfer_season',
        'tournament_golfer',
        'pick',
    ]

    def setUp(self) -> None:
        self.test_user: User = User.objects.get(id=1)
        self.test_season: Season = Season.objects.get(id=1)
        self.test_tournament_season_1: TournamentSeason = TournamentSeason.objects.get(id=1)
        self.test_tournament_season_3: TournamentSeason = TournamentSeason.objects.get(id=3)
        self.test_pick: Pick = Pick.objects.get(id=1)
        return super().setUp()
    
    def test_available_golfer_ids(self):
        """Test the available_golfer_ids method of the tournament_season model.
        """
        # test the functionality for a tournament that has not yet been picked in
        available_golfer_ids = self.test_tournament_season_3.available_golfer_ids(self.test_user)
        self.assertEqual(1, len(available_golfer_ids))
        self.assertIn(3, available_golfer_ids)

        # test the functionality for a tournament that has already been picked in
        available_golfer_ids = self.test_tournament_season_1.available_golfer_ids(self.test_user)
        self.assertEqual(2, len(available_golfer_ids))
        self.assertIn(1, available_golfer_ids)
        self.assertIn(3, available_golfer_ids)
    
    def test_user_pick(self):
        """Test the user_pick method of the tournament_season model.
        """
        # test the functionality for a tournament that has not yet been picked in
        self.assertIsNone(self.test_tournament_season_3.user_pick(self.test_user))

        # test the functionality for a tournament that has already been picked in
        self.assertEqual(self.test_pick.id, self.test_tournament_season_1.user_pick(self.test_user).id)