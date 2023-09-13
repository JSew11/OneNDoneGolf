from django.test import TestCase

from golf_pickem.models.golfer import Golfer

class TestGolferModel(TestCase):
    """Tests for the golfer model.
    """

    def setUp(self) -> None:
        return super().setUp()