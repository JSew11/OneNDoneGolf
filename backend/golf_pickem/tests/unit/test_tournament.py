from django.test import TestCase

from golf_pickem.models.tournament import Tournament

class TestTournamentModel(TestCase):
    """Tests for the tournament model.
    """

    def setUp(self) -> None:
        return super().setUp()
    
    def test_create_tournament(self) -> None:
        """Tests for creating a tournament.
        """
        assert False