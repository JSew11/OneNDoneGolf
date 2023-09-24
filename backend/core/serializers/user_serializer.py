from rest_framework.serializers import ModelSerializer

from ..models.user import User

class UserSerializer(ModelSerializer):
    """Serializer for the user model.
    """

    class Meta:
        model = User
        exclude = ['created', 'updated', 'deleted', 'password']
        read_only_fields = ['id']