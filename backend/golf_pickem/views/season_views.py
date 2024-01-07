from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status, permissions

from ..models import (
    Season
)
from ..serializers import SeasonSerializer

class SeasonViewSet(ModelViewSet):
    """Viewset for the season model. Supports all functionality for creating,
    viewing (individually and in a list), updating, and deleting seasons.
    """
    serializer_class = SeasonSerializer

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
                data={'status': f'Pick with id \'{season_id}\' not found'},
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
                data={'status': f'Pick with id \'{season_id}\' not found'},
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
                data={'status': f'Pick with id \'{season_id}\' not found'},
                status=status.HTTP_404_NOT_FOUND, 
            )