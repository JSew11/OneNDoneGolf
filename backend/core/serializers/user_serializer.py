from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from ..models.user import User

class UserSerializer(ModelSerializer):
    """Serializer for the user model.
    """
    pick_history = PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        exclude = ['created', 'updated', 'deleted', 'password']
        read_only_fields = ['id']