from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status, permissions

from ..models import (
    Season,
    GolferSeason,
    TournamentSeason,
    TournamentGolfer,
)
from ..serializers import (
    SeasonSerializer,
    GolferSeasonSerialier,
    TournamentSeasonSerializer,
    TournamentGolferSerializer,
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
            serialzier: TournamentGolferSerializer = self.serializer_class(tournament_season)
            return Response(
                data=serialzier.data,
                status=status.HTTP_200_OK
            )
        except TournamentSeason.DoesNotExist:
            return Response(
                data={'status': f'Tournament with id \'{tournament_id}\' not found for Season with the id \'{season_id}\''},
                status=status.HTTP_404_NOT_FOUND
            )