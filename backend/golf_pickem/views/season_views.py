from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

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
        return super().create(request, *args, **kwargs)
    
    def retrieve(self, request: Request, season_id: int, *args, **kwargs) -> Response:
        """Get the season with the given id.
        """
        return super().retrieve(request *args, **kwargs)
    
    def partial_update(self, request: Request, season_id: int, *args, **kwargs) -> Response:
        """Update an individual season by its id.
        """
        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request: Request, season_id: int, *args, **kwargs) -> Response:
        """Delete the season with the given id.
        """
        return super().destroy(request, *args, **kwargs)