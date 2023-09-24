from django.test import TestCase

from golf_pickem.models.tournament import Tournament
from golf_pickem.models.golfer import Golfer
from golf_pickem.models.tournament_golfer import TournamentGolfer

class TestTournamentGolferModel(TestCase):
    """Tests for the tournament golfer model.
    """
    fixtures = ['golfer', 'tournament', 'tournament_golfer']

    def setUp(self) -> None:
        self.test_golfer_1: Golfer = Golfer.objects.get(id=1)
        self.test_golfer_2: Golfer = Golfer.objects.get(id=2)
        self.test_tournament: Tournament = Tournament.objects.get(id=1)
        self.test_tournament_golfer_1: TournamentGolfer = TournamentGolfer.objects.get(id=1)
        self.test_tournament_golfer_2: TournamentGolfer = TournamentGolfer.objects.get(id=2)
        return super().setUp()