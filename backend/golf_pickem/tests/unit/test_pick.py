from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from pytest import raises

from core.models.user import User
from golf_pickem.models import (
    Pick,
    TournamentSeason,
    GolferSeason
)

class TestPickModel(TestCase):
    """Tests for the pick model.
    """
    fixtures = [
        'user',
        'season',
        'tournament',
        'tournament_season',
        'golfer',
        'golfer_season',
        'pick'
    ]

    def setUp(self) -> None:
        self.test_user: User = User.objects.get(id=1)
        self.test_tournament_1_season_1: TournamentSeason = TournamentSeason.objects.get(id=1)
        self.test_tournament_1_season_2: TournamentSeason = TournamentSeason.objects.get(id=4)
        self.test_tournament_2_season_2: TournamentSeason = TournamentSeason.objects.get(id=5)
        self.test_tournament_3_season_2: TournamentSeason = TournamentSeason.objects.get(id=6)
        self.test_golfer_1_season_2: GolferSeason = GolferSeason.objects.get(id=4)
        self.test_golfer_2_season_2: GolferSeason = GolferSeason.objects.get(id=5)
        self.test_golfer_3_season_2: GolferSeason = GolferSeason.objects.get(id=6)
        return super().setUp()
    
    def test_create_valid_pick(self):
        """Test creating a valid pick. 
        """
        valid_pick: Pick = Pick.objects.create(
            user = self.test_user,
            tournament_season = self.test_tournament_3_season_2,
            golfer_season = self.test_golfer_3_season_2
        )
        self.assertEqual(self.test_user, valid_pick.user)
        self.assertEqual(self.test_tournament_3_season_2, valid_pick.tournament_season)
        self.assertEqual(self.test_golfer_3_season_2, valid_pick.golfer_season)

    def test_create_invalid_tournament_pick(self):
        """Test creating a pick for a tournament the user has already picked in
        for the season (should fail).
        """
        with self.assertRaises(IntegrityError) as error:
            Pick.objects.create(
                user = self.test_user,
                tournament_season = self.test_tournament_2_season_2,
                golfer_season = self.test_golfer_3_season_2
            )
            self.assertIn('unique_user_tournament_season', str(error.exception))

    def test_create_invalid_golfer_pick(self):
        """Test creating a pick for a golfer the user has already picked in the
        season (should fail).
        """
        with self.assertRaises(IntegrityError) as error:
            Pick.objects.create(
                user = self.test_user,
                tournament_season = self.test_tournament_3_season_2,
                golfer_season = self.test_golfer_2_season_2
            )
            self.assertIn('unique_user_golfer_season', str(error.exception))

    def test_valid_pick_update(self):
        """Test making a valid update to a pick.
        """
        # test the bulk update method
        self.assertTrue(Pick.objects.filter(id=2).update(
            golfer_season = self.test_golfer_3_season_2
        ))

        # test the individual update method (changing the pick back to what it was)
        test_pick: Pick = Pick.objects.get(id=2)
        test_pick.golfer_season = self.test_golfer_2_season_2
        test_pick.save()

    def test_invalid_tournament_pick_update(self):
        """Test updating a pick (bulk method) so that the user has already picked in
        the tournament for the season (should fail).
        """
        with self.assertRaises(IntegrityError) as error:
            Pick.objects.filter(id=2).update(
                tournament_season = self.test_tournament_1_season_2
            )
            self.assertIn('unique_user_golfer_season', str(error.exception))

    def test_invalid_golfer_pick_update(self):
        """Test updating a pick (bulk method) so that the user has already picked
        the golfer in the season (should fail).
        """
        with self.assertRaises(IntegrityError) as error:
            Pick.objects.filter(id=2).update(
                golfer_season = self.test_golfer_1_season_2
            )
            self.assertIn('unique_user_golfer_season', str(error.exception))

    def test_invalid_golfer_save(self):
        """Test updating a pick (individual method) so that the pick is invalid.
        """
        test_pick: Pick = Pick.objects.get(id=2)
        test_pick.golfer_season = self.test_golfer_1_season_2
        with self.assertRaises(IntegrityError) as error:
            test_pick.save()
            self.assertIn('unique_user_golfer_season', str(error.exception))