from django.test import TestCase

from golf_pickem.models import UserSeason

class TestUserSeasonModel(TestCase):
    """Tests for the UserSeason model.
    """
    fixtures = [
        'user',
        'season',
        'user_season',
        'tournament',
        'tournament_season',
        'golfer',
        'golfer_season',
        'tournament_golfer',
        'pick'
    ]

    def setUp(self) -> None:
        self.test_user_season: UserSeason = UserSeason.objects.get(id=1)
        return super().setUp()

    def test_pick_history(self):
        """Test the pick_history method in the user season model.
        """
        season_1_pick_history = self.test_user_season.pick_history()
        self.assertEqual(len(season_1_pick_history), 2)
    
    def test_prize_money(self):
        """Test the prize_money method in the user season model.
        """
        season_1_prize_money = self.test_user_season.prize_money()
        self.assertEqual(8000, season_1_prize_money)

    def test_tournaments_won(self):
        """Test the tournaments_won method in the user season model.
        """
        season_1_tournaments_won = self.test_user_season.tournaments_won()
        self.assertEqual(1, season_1_tournaments_won)
