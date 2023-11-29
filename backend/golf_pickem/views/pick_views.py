from datetime import datetime
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status, permissions

from core.models.user import User
from ..models.pick import Pick
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