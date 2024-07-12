from django.test import TestCase
from django.db import IntegrityError
from pytest import raises

from core.models.user import User
from golf_pickem.models import (
    Pick,
    Season,
    Tournament,
    Golfer,
    TournamentSeason,
    GolferSeason,
    TournamentGolfer,
)

class TestPickModel(TestCase):
    """Tests for the pick model.
    """
    fixtures = [
        'user',
        'season',
        'tournament',
        'golfer',
        'pick',
        'tournament_season',
        'golfer_season',
        'tournament_golfer'
    ]

    def setUp(self) -> None:
        self.test_user: User = User.objects.get(id=1)
        self.test_season_1: Season = Season.objects.get(id=1)
        self.test_tournament_1: Tournament = Tournament.objects.get(id=1)
        self.test_tournament_2: Tournament = Tournament.objects.get(id=2)
        self.test_tournament_3: Tournament = Tournament.objects.get(id=3)
        self.test_golfer_1: Golfer = Golfer.objects.get(id=1)
        self.test_golfer_2: Golfer = Golfer.objects.get(id=2)
        self.test_golfer_3: Golfer = Golfer.objects.get(id=3)
        self.test_golfer_4: Golfer = Golfer.objects.get(id=4)
        self.test_pick_1: Pick = Pick.objects.get(id=1)
        self.test_pick_2: Pick = Pick.objects.get(id=2)
        return super().setUp()
    
    def test_create_valid_pick(self):
        """Test creating a valid pick. 
        """
        valid_pick: Pick = Pick.objects.create(
            user = self.test_user,
            season = self.test_season_1,
            tournament = self.test_tournament_3,
            primary_selection = self.test_golfer_3,
            backup_selection = self.test_golfer_4
        )
        self.assertEqual(self.test_user, valid_pick.user)
        self.assertEqual(self.test_tournament_3, valid_pick.tournament)
        self.assertEqual(self.test_golfer_3, valid_pick.primary_selection)
        self.assertEqual(self.test_golfer_4, valid_pick.backup_selection)

    def test_create_invalid_tournament_pick(self):
        """Test creating a pick for a tournament the user has already picked in
        for the season (should fail).
        """
        with self.assertRaises(IntegrityError) as error:
            Pick.objects.create(
                user = self.test_user,
                season = self.test_season_1,
                tournament = self.test_tournament_1,
                primary_selection = self.test_golfer_3,
                backup_selection = self.test_golfer_4
            )
            self.assertIn('unique_user_tournament_season', str(error.exception))

    def test_create_invalid_golfer_pick(self):
        """Test creating a pick for a golfer the user has already picked in the
        season (should fail).
        """
        # test case for a primary selection that has already been picked
        with self.assertRaises(IntegrityError) as error:
            Pick.objects.create(
                user = self.test_user,
                season = self.test_season_1,
                tournament = self.test_tournament_3,
                primary_selection = self.test_golfer_1,
                backup_selection = self.test_golfer_4,
                scored_golfer = self.test_golfer_1
            )
            self.assertIn('unique_user_golfer_season', str(error.exception))

    def test_valid_pick_update(self):
        """Test making a valid update to a pick.
        """
        # test the bulk update method
        self.assertTrue(Pick.objects.filter(id=2).update(
            primary_selection = self.test_golfer_3,
            backup_selection = self.test_golfer_4,
        ))

        # test the individual update method (changing the pick back to what it was)
        self.test_pick_2.primary_selection = self.test_golfer_2
        self.test_pick_2.backup_selection = self.test_golfer_3
        self.test_pick_2.save()

    def test_invalid_tournament_pick_update(self):
        """Test updating a pick (bulk method) so that the user has already picked in
        the tournament for the season (should fail).
        """
        with self.assertRaises(IntegrityError) as error:
            Pick.objects.filter(id=2).update(
                tournament = self.test_tournament_1
            )
            self.assertIn('unique_user_golfer_season', str(error.exception))

    def test_invalid_golfer_pick_update(self):
        """Test updating a pick (bulk method) so that the user has already picked
        the golfer in the season (should fail).
        """
        with self.assertRaises(IntegrityError) as error:
            Pick.objects.filter(id=2).update(
                primary_selection = self.test_golfer_1,
                backup_selection = self.test_golfer_4,
                scored_golfer = self.test_golfer_1
            )
            self.assertIn('unique_user_golfer_season', str(error.exception))

    def test_invalid_golfer_save(self):
        """Test updating a pick (individual method) so that the pick is invalid.
        """
        self.test_pick_2.scored_golfer = self.test_golfer_1
        with self.assertRaises(IntegrityError) as error:
            self.test_pick_2.save()
            self.assertIn('unique_user_golfer_season', str(error.exception))
    
    def test_get_prize_money(self):
        """Test the get_prize_money method of the Pick model.
        """
        # test getting the prize money for a pick that has not yet been scored
        self.assertEqual(0, self.test_pick_2.get_prize_money())

        # test getting the prize money for a pick that has been scored
        tournament_season = TournamentSeason.objects.get(tournament=self.test_pick_1.tournament.id ,season=self.test_pick_1.season.id)
        golfer_season = GolferSeason.objects.get(golfer=self.test_pick_1.scored_golfer.id, season=self.test_pick_1.season.id)
        tournament_golfer = TournamentGolfer.objects.get(tournament_season=tournament_season.id, golfer_season=golfer_season.id)
        self.assertEqual(tournament_golfer.prize_money, self.test_pick_1.get_prize_money())