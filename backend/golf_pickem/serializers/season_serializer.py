from rest_framework.serializers import ModelSerializer

from ..models import Season

class SeasonSerializer(ModelSerializer):
    """Serializer for the season model.
    """

    class Meta:
        model = Season
        exclude = ['created', 'updated', 'deleted']
        read_only_fields = ['id']