from django.test import TestCase

from golf_pickem.models.tournament import Tournament

class TestTournamentModel(TestCase):
    """Tests for the tournament model.
    """
    fixtures = ['tournament']

    def setUp(self) -> None:
        return super().setUp()
    
    def test_create_tournament(self) -> None:
        """Tests for creating a tournament.
        """
        test_name = 'Test Tournament'
        test_course = 'Test Course'
        test_location = 'Location, Test'
        test_purse = 100
        test_year = 1

        # test creating a tournament with all fields
        test_tournament: Tournament = Tournament.objects.create(
            name=test_name,
            course=test_course,
            location=test_location,
            purse=test_purse,
            year=test_year
        )
        self.assertEqual(test_tournament.name, test_name)
        self.assertEqual(test_tournament.course, test_course)
        self.assertEqual(test_tournament.location, test_location)
        self.assertEqual(test_tournament.purse, test_purse)
        self.assertEqual(test_tournament.year, test_year)
