from django.test import TestCase

from core.models import User
from golf_pickem.models import (
    Season,
    TournamentSeason,
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
        self.test_tournament_season: TournamentSeason = TournamentSeason.objects.get(id=3)
        return super().setUp()
    
    def test_available_golfer_ids(self):
        """Test the available_golfer_ids method of the tournament_season model.
        """
        available_golfer_ids = self.test_tournament_season.available_golfer_ids(self.test_user, self.test_season.id)
        self.assertEqual(1, len(available_golfer_ids))
        self.assertEqual(3, available_golfer_ids[0])