from django.test import TestCase

from golf_pickem.models import Tournament

class TestTournamentModel(TestCase):
    """Tests for the tournament model.
    """
    fixtures = ['tournament']

    def setUp(self) -> None:
        return super().setUp()
    
    def test_create_tournament(self) -> None:
        """Tests for creating a tournament.
        """
        test_name = 'Test Creating Tournament'
        test_course = 'Test Course'
        test_location = 'Location, Test'

        # test creating a tournament with all fields
        test_tournament: Tournament = Tournament.objects.create(
            name=test_name,
            course=test_course,
            location=test_location
        )
        self.assertEqual(test_tournament.name, test_name)
        self.assertEqual(test_tournament.course, test_course)
        self.assertEqual(test_tournament.location, test_location)

    def test_create_from_external_data(self) -> None:
        """Tests for creating a tournament from mocked external api data.
        """
        # test creating a tournament with one course
        sample_api_response = {
            'tournId': '123',
            'name': 'Test External Tournament',
            'courses': [
                {
                    'courseName': 'Test Course Name',
                    'location': {
                        'country': 'Test Country'
                    },
                }
            ]
        }
        created_tournament = Tournament.create_from_external_data(sample_api_response)
        self.assertEqual(created_tournament.name, 'Test External Tournament')
        self.assertEqual(created_tournament.external_id, '123')
        self.assertEqual(created_tournament.course, 'Test Course Name')
        self.assertEqual(created_tournament.location, 'Test Country')

        # test creating a tournament with multiple courses
        sample_api_response = {
            'tournId': '123',
            'name': 'Test External Tournament',
            'courses': [
                {
                    'courseName': 'Test Course Name',
                    'location': {
                        'country': 'Test Country'
                    },
                },
                {
                    'courseName': 'Test Course Name 2',
                    'location': {
                        'country': 'Test Country'
                    },
                }
            ]
        }
        created_tournament = Tournament.create_from_external_data(sample_api_response)
        self.assertEqual(created_tournament.course, 'Multiple')
        self.assertEqual(created_tournament.location, 'Earth')