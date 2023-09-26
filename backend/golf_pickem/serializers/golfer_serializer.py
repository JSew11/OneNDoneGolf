from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from ..models.golfer import Golfer

class GolferSerializer(ModelSerializer):
    """Serializer for the golfer model.
    """
    tournaments = PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Golfer
        exclude = ['created', 'updated', 'deleted']
        read_only_fields = ['id', 'player_id']