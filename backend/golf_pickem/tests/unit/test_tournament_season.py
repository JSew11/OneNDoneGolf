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
        'user_season',
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
        self.test_tournament_season_2: TournamentSeason = TournamentSeason.objects.get(id=2)
        self.test_tournament_season_3: TournamentSeason = TournamentSeason.objects.get(id=3)
        self.test_pick: Pick = Pick.objects.get(id=1)
        return super().setUp()
    
    def test_user_pick(self):
        """Test the user_pick method of the tournament_season model.
        """
        # test the functionality for a tournament that has not yet been picked in
        self.assertIsNone(self.test_tournament_season_3.user_pick(self.test_user))

        # test the functionality for a tournament that has already been picked in
        self.assertEqual(self.test_pick.id, self.test_tournament_season_1.user_pick(self.test_user).id)
    
    def test_finish_tournament_season(self):
        """Test the finish_tournament_season method of the tournament_season model.
        """
        self.test_tournament_season_2.finish_tournament_season()

        # test that all picks for the tournament season have a scored golfer
        self.assertEqual(len(self.test_tournament_season_2.picked_golfers()), 2)

    def test_winning_users(self):
        """Test the winners property of the tournament_season model.
        """
        # test getting winning_users for an unfinished tournament_season
        self.assertIsNone(self.test_tournament_season_3.winning_user_ids())

        # test getting winning_users for a tournament_season with only one winner
        self.assertEqual(1, len(self.test_tournament_season_1.winning_user_ids()))

        # test getting winning_users for a tournament_season with multiple winners
        self.test_tournament_season_2.finish_tournament_season()
        self.assertGreater(len(self.test_tournament_season_2.winning_user_ids()), 1)