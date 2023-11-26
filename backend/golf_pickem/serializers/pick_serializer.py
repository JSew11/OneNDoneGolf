from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from ..models.pick import Pick

class PickSerializer(ModelSerializer):
    """Serializer for the pick model.
    """

    class Meta:
        model = Pick
        exclude = ['created', 'updated', 'deleted']
        read_only_fields = ['id']