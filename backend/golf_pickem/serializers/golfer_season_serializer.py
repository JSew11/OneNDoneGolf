from rest_framework.serializers import ModelSerializer

from ..models import GolferSeason
from ..serializers import GolferSerializer

class GolferSeasonSerializer(ModelSerializer):
    """Serializer for the golfer season model.
    """
    golfer = GolferSerializer(many=False, read_only=True)

    class Meta:
        model = GolferSeason
        exclude = ['created', 'updated', 'deleted']
        read_only_fields = ['id']