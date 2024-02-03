from datetime import datetime
from django.test import TestCase

from golf_pickem.models import (
    Season,
    Tournament,
)

class TestSeasonModel(TestCase):
    """Tests for the season model.
    """
    fixtures = [
        'season',
        'tournament',
        'tournament_season',
    ]

    def setUp(self) -> None:
        self.test_season: Season = Season.objects.get(id=1)
        self.test_tournament_1: Tournament = Tournament.objects.get(id=1)
        self.test_tournament_3: Tournament = Tournament.objects.get(id=3)
        return super().setUp()

    def test_next_tournament_id(self):
        """Test the next_tournament method of the season model.
        """
        # test with only one tournament after the given date
        after_date = datetime(2024, 2, 1)
        next_tournament_id = self.test_season.next_tournament_id(after_date=after_date)
        self.assertEqual(next_tournament_id, self.test_tournament_3.id)

        # test with multiple tournaments after the given date
        after_date = datetime(2024, 1, 1)
        next_tournament_id = self.test_season.next_tournament_id(after_date=after_date)
        self.assertEqual(next_tournament_id, self.test_tournament_1.id)