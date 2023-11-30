from datetime import datetime
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from core.models.user import User
from ..models.pick import Pick
from ..models.tournament_golfer import TournamentGolfer
from ..serializers.pick_serializer import PickSerializer

class PickViewSet(ModelViewSet):
    """Viewset for the pick model. Supports all functionality for making, 
    editing, viewing and deleting picks.
    """
    serializer_class = PickSerializer

    def list(self, request: Request, *args, **kwargs) -> Response:
        """Get a list of picks.

        Filterable by:
            - user (int id) => defaults to the user who made the request
            - year (int)
        """
        user: User = User.objects.get(id=request.data.get('user')) if request.data.get('user') else request.user
        if year := request.data.get('year'):
            data = user.pick_history_by_year(year=year)
        else:
            data = user.pick_history
        serializer: PickSerializer = self.serializer_class(data, many=True)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )
    
    def create(self, request: Request, *args, **kwargs) -> Response:
        """Create a pick from the given tournament golfer and the user who made
        the request.
        """
        try:
            tournament_golfer: TournamentGolfer = TournamentGolfer.objects.get()
            user: User = request.user
            pick: Pick = Pick.objects.create(
                user_id=user.id, 
                tournament_golfer_id=tournament_golfer.id
            )
        except TournamentGolfer.DoesNotExist:
            return Response(
                data={'status': f'Tournament Golfer with id \'\' not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def retrieve(self, request: Request, pick_id: int, *args, **kwargs) -> Response:
        """Get an individual pick by its id.
        """
        try:
            pick: Pick = Pick.objects.get(id=pick_id)
            serializer: PickSerializer = self.serializer_class(pick)
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK,
            )
        except Pick.DoesNotExist:
            return Response(
                data={'status': f'Pick with id \'{pick_id}\' not found'},
                status=status.HTTP_404_NOT_FOUND, 
            )