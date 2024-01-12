from rest_framework.serializers import ModelSerializer

from ..models import GolferSeason

class GolferSeasonSerialier(ModelSerializer):
    """Serializer for the golfer season model.
    """

    class Meta:
        model = GolferSeason
        exclude = ['created', 'updated', 'deleted']
        read_only_fields = ['id']