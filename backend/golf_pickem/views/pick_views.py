from datetime import datetime
from django.db import IntegrityError
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from core.models.user import User
from ..models import (
    Pick,
    Season,
    UserSeason
)
from ..serializers import PickSerializer

class PickViewSet(ModelViewSet):
    """Viewset for the pick model. Supports all functionality for creating, 
    viewing (individually and in a list), updating, and deleting picks.
    """
    serializer_class = PickSerializer

    def list(self, request: Request, *args, **kwargs) -> Response:
        """Get a list of picks.

        Filterable by:
            - user (int id) => defaults to the user who made the request
            - season (int id)
        """
        user_id = request.query_params.get('user_id')
        season_id = request.query_params.get('season_id')
        error_messages = []
        if not season_id:
            error_messages.append('Field \'season_id\' is required')
        if len(error_messages) > 0: # return any missing field errors before validating the pick
            return Response(
                data={'errors': error_messages},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user: User = User.objects.get(id=user_id) if user_id else request.user
            user_season: UserSeason = UserSeason.objects.get(user=user.id, season=season_id)
            serializer: PickSerializer = self.serializer_class(user_season.pick_history.all(), many=True)
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                data={'message': f'User with id \'{user_id}\' not found'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Season.DoesNotExist:
            return Response(
                data={'message': f'Season with id \'{season_id}\' not found'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def create(self, request: Request, *args, **kwargs) -> Response:
        """Create a pick from the given tournament golfer and the user who made
        the request. Users CANNOT make picks for any user other than themselves.
        """
        tournament_id = request.data.get('tournament_id')
        primary_selection_id = request.data.get('primary_selection_golfer_id')
        backup_selection_id = request.data.get('backup_selection_golfer_id')
        season_id = request.data.get('season_id')
        # check for required fields
        error_messages = []
        if not tournament_id:
            error_messages.append('Field \'tournament_id\' is required')
        if not primary_selection_id:
            error_messages.append('Field \'primary_selection_golfer_id\' is required')
        if not backup_selection_id:
            error_messages.append('Field \'backup_selection_golfer_id\' is required')
        if not season_id:
            error_messages.append('Field \'season_id\' is required')
        if len(error_messages) > 0: # return any missing field errors before validating the pick
            return Response(
                data={'errors': error_messages},
                status=status.HTTP_400_BAD_REQUEST
            )
        error_messages.extend(self._validate_pick(user=request.user, season_id=season_id, primary_selection_id=primary_selection_id, backup_selection_id=backup_selection_id))
        # picked and cannot equal each other)
        if len(error_messages) > 0:
            return Response(
                data={'errors': error_messages},
                status=status.HTTP_400_BAD_REQUEST
            )
        # attempt to create the pick from the given data
        try:
            user_season: UserSeason = UserSeason.objects.get(user=request.user.id, season=season_id)
            pick_data = {
                'user_season': user_season.id,
                'tournament': tournament_id,
                'primary_selection': primary_selection_id,
                'backup_selection': backup_selection_id,
                'scored_golfer': None
            }
            serializer: PickSerializer = self.serializer_class(data=pick_data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    data=serializer.data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    data=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
        except UserSeason.DoesNotExist:
            return Response(
                data={'message': f'Current user not found in the season with id \'{season_id}\''},
                status=status.HTTP_400_BAD_REQUEST
            )
        except IntegrityError as error:
            error_string = str(error)
            if 'unique_user_tournament_season' in error_string:
                return Response(
                    data={'message': 'You have already picked in this tournament for this season'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if 'unique_user_golfer_season' in error_string:
                return Response(
                    data={'message': 'You have already picked this golfer in this season'},
                    status=status.HTTP_400_BAD_REQUEST
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

    def partial_update(self, request: Request, pick_id: int, *args, **kwargs) -> Response:
        """Update an individual pick by its id. Only allows a pick to be edited
        by the owner of the pick. Pick updates can only change the golfer being
        picked for the tournament.
        """
        primary_selection_id = request.data.get('primary_selection_golfer_id')
        backup_selection_id = request.data.get('backup_selection_golfer_id')
        # check for required fields
        error_messages = []
        if not primary_selection_id:
            error_messages.append('Field \'primary_selection_golfer_id\' is required')
        if not backup_selection_id:
            error_messages.append('Field \'backup_selection_golfer_id\' is required')
        # attempt to update the pick object's associated golfer season
        try:
            pick: Pick = Pick.objects.get(id=pick_id)
            error_messages.extend(self._validate_pick(user=request.user, season_id=pick.user_season.season.id, primary_selection_id=primary_selection_id, backup_selection_id=backup_selection_id))
            if len(error_messages) > 0:
                return Response(
                    data={'errors': error_messages},
                    status=status.HTTP_400_BAD_REQUEST
                )
            updated_data = {
                'primary_selection': primary_selection_id,
                'backup_selection': backup_selection_id,
                'updated': datetime.now()
            }
            serializer: PickSerializer = self.serializer_class(pick, data=updated_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    data=serializer.data,
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    data=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Pick.DoesNotExist:
            return Response(
                data={'status': f'Pick with id \'{pick_id}\' not found for the current user'},
                status=status.HTTP_404_NOT_FOUND, 
            )
        except IntegrityError as error:
            error_string = str(error)
            if 'unique_user_golfer_season' in error_string:
                return Response(
                    data={'message': 'You have already picked this golfer in this season'},
                    status=status.HTTP_400_BAD_REQUEST
                )
    
    def destroy(self, request: Request, pick_id: int, *args, **kwargs) -> Response:
        """Delete the player with the given id.
        """
        try:
            pick: Pick = Pick.objects.get(id=pick_id)
            pick.delete()
            return Response(
                data={'message': 'Pick deleted successfully'},
                status=status.HTTP_204_NO_CONTENT
            )
        except Pick.DoesNotExist:
            return Response(
                data={'message': f'Pick with id \'{pick_id}\' not found for the current user'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def _validate_pick(self, user: User, season_id: int, primary_selection_id: int, backup_selection_id: int):
        """Validate that the primary and backup selections are unique and have not been picked yet by
        the given user during the current season.
        """
        error_messages = []
        if primary_selection_id == backup_selection_id:
            error_messages.append('\'primary_selection_golfer_id\' and \'backup_selection_golfer_id\' must be unique')
        user_season: UserSeason = UserSeason.objects.get(user=user.id, season=season_id)
        previously_scored_golfer_ids = [str(pick.scored_golfer.id) for pick in user_season.pick_history.all() if pick.scored_golfer != None]
        if primary_selection_id in previously_scored_golfer_ids:
            error_messages.append('\'primary_selection_golfer_id\' has already been picked this season')
        if backup_selection_id in previously_scored_golfer_ids:
            error_messages.append('\'backup_selection_golfer_id\' has already been picked this season')
        return error_messages