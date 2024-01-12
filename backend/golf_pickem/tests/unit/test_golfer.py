from django.test import TestCase

from golf_pickem.models import Golfer

class TestGolferModel(TestCase):
    """Tests for the golfer model.
    """
    fixtures = ['golfer']

    def setUp(self) -> None:
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