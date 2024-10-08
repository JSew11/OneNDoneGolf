from datetime import datetime
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import action
from rest_framework import status, permissions

from ..models import (
    Season,
    UserSeason,
    GolferSeason,
    Tournament,
    TournamentSeason,
    TournamentGolfer,
)
from ..serializers import (
    SeasonSerializer,
    UserSeasonSerialier,
    GolferSerializer,
    GolferSeasonSerialier,
    TournamentSerializer,
    TournamentSeasonSerializer,
    TournamentGolferSerializer,
    PickSerializer
)

class SeasonViewSet(ModelViewSet):
    """Viewset for the season model. Supports all functionality for creating,
    viewing (individually and in a list), updating, and deleting seasons.
    """
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
    permission_classes = [permissions.DjangoModelPermissions]

    def list(self, request: Request, *args, **kwargs) -> Response:
        """Get a list of seasons.
        """
        seasons = Season.objects.all()
        serializer: SeasonSerializer = self.serializer_class(seasons, many=True)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )
    
    def create(self, request: Request, *args, **kwargs) -> Response:
        """Create a season using the given information.
        """
        serializer: SeasonSerializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )
    
    def retrieve(self, request: Request, season_id: int, *args, **kwargs) -> Response:
        """Get the season with the given id.
        """
        try:
            season: Season = Season.objects.get(id=season_id)
            serializer: SeasonSerializer = self.serializer_class(season)
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK,
            )
        except Season.DoesNotExist:
            return Response(
                data={'status': f'Season with id \'{season_id}\' not found'},
                status=status.HTTP_404_NOT_FOUND, 
            )
    
    def partial_update(self, request: Request, season_id: int, *args, **kwargs) -> Response:
        """Update an individual season by its id.
        """
        try:
            season: Season = Season.objects.get(id=season_id)
            serializer: SeasonSerializer = self.serializer_class(season, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    data=serializer.data,
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    data=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Season.DoesNotExist:
            return Response(
                data={'status': f'Season with id \'{season_id}\' not found'},
                status=status.HTTP_404_NOT_FOUND, 
            )
    
    def destroy(self, request: Request, season_id: int, *args, **kwargs) -> Response:
        """Delete the season with the given id.
        """
        try:
            season: Season = Season.objects.get(id=season_id)
            season.delete()
            return Response(
                data={'message': 'Season deleted successfully'},
                status=status.HTTP_204_NO_CONTENT
            )
        except Season.DoesNotExist:
            return Response(
                data={'status': f'Season with id \'{season_id}\' not found'},
                status=status.HTTP_404_NOT_FOUND, 
            )
    
    @action(detail=True, methods=['GET'])
    def active_season(self, request: Request) -> Response:
        """Get the active season's details.
        """
        active_season: Season = Season.objects.filter(active=True).order_by('start_date').first()
        if active_season is None:
            return Response(
                data={'status': 'There is no current active season'},
                status=status.HTTP_204_NO_CONTENT,
            )
        serializer: SeasonSerializer = self.serializer_class(active_season)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['GET'])
    def next_tournament(self, request: Request, season_id: int) -> Response:
        """Get the next tournament in the given season's schedule.
        """
        after_date = request.query_params.get('after_date', None)
        if after_date is not None:
            after_date = datetime.strptime(after_date, '%Y-%m-%d')
        try:
            season: Season = Season.objects.get(id=season_id)
            tournament: Tournament = Tournament.objects.get(id=season.next_tournament_id(after_date=after_date))
            tournament_season: TournamentSeason = TournamentSeason.objects.get(tournament=tournament.id, season=season.id)
            tournament_serializer: TournamentSerializer = TournamentSerializer(tournament)
            next_tournament_pick = tournament_season.user_pick(request.user)
            next_tournament_pick_data = None
            if next_tournament_pick is not None:
                next_tournament_pick_data = PickSerializer(next_tournament_pick).data
            return Response(
                data={
                    'tournament': tournament_serializer.data,
                    'user_pick': next_tournament_pick_data
                },
                status=status.HTTP_200_OK,
            )
        except Season.DoesNotExist:
            return Response(
                data={'status': f'Season with id \'{season_id}\' not found'},
                status=status.HTTP_404_NOT_FOUND, 
            )
        except Tournament.DoesNotExist:
            return Response(
                data={'status': f'Could not find the next tournament for Season with id \'{season_id}\' '},
                status=status.HTTP_404_NOT_FOUND,
            )

class SeasonUsersViewset(ModelViewSet):
    """Viewset for the users participating in a season. Supports creating and viewing
    either as a list o individually.
    """
    queryset = UserSeason.objects.all()
    serializer_class = UserSeasonSerialier
    permission_classes = [permissions.DjangoModelPermissions]

    def list(self, request: Request, season_id: int, *args, **kwargs) -> Response:
        """List the users who participated in the season with the given id.
        """
        try:
            season: Season = Season.objects.get(id=season_id)
            sorted_users = sorted(season.users.all(), key=lambda user: user.prize_money, reverse=True)
            serializer: UserSeasonSerialier = self.serializer_class(sorted_users, many=True)
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK,
            )
        except Season.DoesNotExist:
            return Response(
                data={'status': f'Season with id \'{season_id}\' not found'},
                status=status.HTTP_404_NOT_FOUND, 
            )
    
    def create(self, request: Request, season_id: int, *args, **kwargs) -> Response:
        """Create a user season using the given information.
        """
        user_registration_data = {
            'season': season_id,
            'user': request.user.id
        }
        user_id = request.data.get('user', default=None)
        if request.user.has_perm('core.create_user') and user_id!= None: # only want admin to be able to do this
            user_registration_data['user'] = user_id
        serializer: UserSeasonSerialier = self.serializer_class(data=user_registration_data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

class SeasonGolfersViewset(ModelViewSet):
    """Viewset for the golfers participating in a season. Supports viewing either
    as a list or individually.
    """
    queryset = GolferSeason.objects.all()
    serializer_class = GolferSeasonSerialier
    permission_classes = [permissions.DjangoModelPermissions]

    def list(self, request: Request, season_id: int, *args, **kwargs) -> Response:
        """List the golfers who participated in the season with the given id.
        """
        try:
            season: Season = Season.objects.get(id=season_id)
            serializer: GolferSeasonSerialier = self.serializer_class(season.golfers, many=True)
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK,
            )
        except Season.DoesNotExist:
            return Response(
                data={'status': f'Season with id \'{season_id}\' not found'},
                status=status.HTTP_404_NOT_FOUND, 
            )
    
    def retrieve(self, request: Request, season_id: int, golfer_id: int, *args, **kwargs) -> Response:
        """Get an individual golfer with the given id who participated in the season
        with the given id.
        """
        try:
            golfer_season = GolferSeason.objects.get(golfer=golfer_id, season=season_id)
            serializer: GolferSeasonSerialier = self.serializer_class(golfer_season)
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        except GolferSeason.DoesNotExist:
            return Response(
                data={'status': f'Golfer with id \'{golfer_id}\' not found as a participant of Season with id \'{season_id}\''},
                status=status.HTTP_404_NOT_FOUND, 
            )

class SeasonTournamentsViewSet(ModelViewSet):
    """Viewset for the tournaments in a season. Supports viewing either as a list
    or individually.
    """
    queryset = TournamentSeason.objects.all()
    serializer_class = TournamentSeasonSerializer
    permission_classes = [permissions.DjangoModelPermissions]

    def list(self, request: Request, season_id: int, *args, **kwargs) -> Response:
        """List the tournaments that were a part of the season with the given id.
        """
        try:
            season: Season = Season.objects.get(id=season_id)
            serializer: TournamentSeasonSerializer = self.serializer_class(season.schedule, many=True)
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK,
            )
        except Season.DoesNotExist:
            return Response(
                data={'status': f'Season with id \'{season_id}\' not found'},
                status=status.HTTP_404_NOT_FOUND, 
            )
    
    def retrieve(self, request: Request, season_id: int, tournament_id: int, *args, **kwargs) -> Response:
        """Get an individual tournament with the given id who participated in the
        season with the given id.
        """
        try:
            tournament_season = TournamentSeason.objects.get(tournament=tournament_id, season=season_id)
            serializer: TournamentSeasonSerializer = self.serializer_class(tournament_season)
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        except TournamentSeason.DoesNotExist:
            return Response(
                data={'status': f'Tournament with id \'{tournament_id}\' not found for Season with id \'{season_id}\''},
                status=status.HTTP_404_NOT_FOUND, 
            )
    
    @action(detail=False, methods=['GET'])
    def field(self, request: Request, season_id: int, tournament_id: int) -> Response:
        """Get a list of the golfers who are participating in the tournament with 
        the given id during the season with the given id.
        """
        try:
            tournament_season: TournamentSeason = TournamentSeason.objects.get(season=season_id, tournament=tournament_id)
            field = [tournament_golfer.golfer_season.golfer for tournament_golfer in tournament_season.field.all()]
            serializer = GolferSerializer(
                field,
                context={'user': request.user, 'season_id': season_id},
                many=True
            )
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        except TournamentSeason.DoesNotExist:
            return Response(
                data={'message': f'Tournament with id \'{tournament_id}\' not found for the Season with id \'{season_id}\''},
                status=status.HTTP_400_BAD_REQUEST,
            )

class SeasonTournamentGolferViewSet(ModelViewSet):
    """Viewset for the golfers who participate in specific tournaments throughout
    a season. Supports viewing as either a list or individually.
    """
    queryset = TournamentGolfer.objects.all()
    serializer_class = TournamentGolferSerializer
    permission_classes = [permissions.DjangoModelPermissions]

    def list(self, request: Request, season_id: int, tournament_id: int, *args, **kwargs) -> Response:
        """List the golfers who participated in the tournament with the given id
        during the season with the given id.
        """
        try:
            tournament_season: TournamentSeason = TournamentSeason.objects.get(season=season_id, tournament=tournament_id)
            serialzier: TournamentGolferSerializer = self.serializer_class(tournament_season.field, many=True)
            return Response(
                data=serialzier.data,
                status=status.HTTP_200_OK
            )
        except TournamentSeason.DoesNotExist:
            return Response(
                data={'status': f'Tournament with id \'{tournament_id}\' not found for Season with the id \'{season_id}\''},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def retrieve(self, request: Request, season_id: int, tournament_id: int, golfer_id: int, *args, **kwargs):
        """Get an individual golfer with the given id who participated in the
        tournament with the given id during the season with the given id.
        """
        try:
            tournament_season: TournamentSeason = TournamentSeason.objects.get(season=season_id, tournament=tournament_id)
            golfer_season: GolferSeason = GolferSeason.objects.get(season=season_id, golfer=golfer_id)
            tournament_golfer: TournamentGolfer = TournamentGolfer.objects.get(tournament_season=tournament_season, golfer_season=golfer_season)
            serializer: TournamentGolferSerializer = self.serializer_class(tournament_golfer)
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        except TournamentSeason.DoesNotExist:
            return Response(
                data={'status': f'Tournament with id \'{tournament_id}\' not found for Season with the id \'{season_id}\''},
                status=status.HTTP_404_NOT_FOUND
            )
        except GolferSeason.DoesNotExist:
            return Response(
                data={'status': f'Golfer with id \'{golfer_id}\' not found as a participant of Season with id \'{season_id}\''},
                status=status.HTTP_404_NOT_FOUND, 
            )
        except TournamentGolfer.DoesNotExist:
            return Response(
                data={'status': f'Golfer with id \'{golfer_id}\' did not participate in the Tournament with id \'{tournament_id}\' during the Season with id\'{season_id}\''},
                status=status.HTTP_404_NOT_FOUND
            )