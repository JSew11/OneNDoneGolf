from rest_framework.serializers import ModelSerializer

from ..models import Pick

class PickSerializer(ModelSerializer):
    """Serializer for the pick model.
    """

    class Meta:
        model = Pick
        exclude = ['created', 'updated', 'deleted']
        read_only_fields = ['id']