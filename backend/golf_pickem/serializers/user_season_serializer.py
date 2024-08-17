from rest_framework.serializers import ModelSerializer

from ..models import UserSeason

class UserSeasonSerialier(ModelSerializer):
    """Serializer for the golfer season model.
    """

    class Meta:
        model = UserSeason
        exclude = ['created', 'updated', 'deleted']
        read_only_fields = ['id']