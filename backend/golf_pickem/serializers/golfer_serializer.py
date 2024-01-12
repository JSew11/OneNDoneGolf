from rest_framework.serializers import ModelSerializer

from ..models import Golfer

class GolferSerializer(ModelSerializer):
    """Serializer for the golfer model.
    """

    class Meta:
        model = Golfer
        exclude = ['created', 'updated', 'deleted']
        read_only_fields = ['id']