from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from ..models.golfer import Golfer

class GolferSerializer(ModelSerializer):
    """Serializer for the golfer model.
    """

    class Meta:
        model = Golfer
        exclude = ['created', 'updated', 'deleted']
        read_only_fields = ['id']