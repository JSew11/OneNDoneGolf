from django.test import TestCase

from golf_pickem.models import Golfer, Season

class TestGolferModel(TestCase):
    """Tests for the golfer model.
    """
    fixtures = [
        'user',
        'season',
        'user_season',
        'tournament',
        'golfer',
        'pick',
        'tournament_season',
        'golfer_season',
        'tournament_golfer'
    ]

    def setUp(self) -> None:
        self.test_season = Season.objects.get(id=1)
        self.test_golfer_1 = Golfer.objects.get(id=1)
        return super().setUp()
    
    def test_create_golfer(self) -> None:
        """Tests for creating a golfer.
        """
        test_first_name = 'Test'
        test_last_name = 'Name'
        test_country = 'COUNTRY'

        # test creating a golfer with all fields
        test_golfer: Golfer = Golfer.objects.create(
            first_name=test_first_name,
            last_name=test_last_name,
            country=test_country
        )
        self.assertEqual(test_golfer.first_name, test_first_name)
        self.assertEqual(test_golfer.last_name, test_last_name)
        self.assertEqual(test_golfer.country, test_country)
    
    def test_times_picked(self) -> None:
        """Test the times_picked method for a golfer.
        """
        self.assertEqual(1, self.test_golfer_1.times_picked(self.test_season.id))

    def test_times_picked_as_winner(self) -> None:
        """Test the times_picked_as_winner method for a golfer.
        """
        self.assertEqual(1, self.test_golfer_1.times_picked_as_winner(self.test_season.id))
    
    def test_remaining_available_picks(self) -> None:
        """Test the remaining_available_picks method for a golfer.
        """
        self.assertEqual(1, self.test_golfer_1.remaining_available_picks(self.test_season.id))