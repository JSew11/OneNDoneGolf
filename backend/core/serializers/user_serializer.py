from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from ..models.user import User

class UserSerializer(ModelSerializer):
    """Serializer for the user model.
    """

    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['id']